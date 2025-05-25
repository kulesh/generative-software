from pathlib import Path
import typer
from typing import Optional
from rich import print
from rich.console import Console
from rich.markdown import Markdown
import yaml
from collections import defaultdict, deque
from datetime import datetime
from openai import OpenAI

app = typer.Typer()
console = Console()
client = OpenAI()


def resolve_order(prompts: dict, flow: list[str]) -> list[str]:
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for node in flow:
        node_id = node['id']
        if node_id not in prompts:
            raise ValueError(f"Prompt ID '{node_id}' in flow not defined in prompts")
        for dep in node.get('after', []):
            graph[dep].append(node_id)
            in_degree[node_id] += 1
        if node_id not in in_degree:
            in_degree[node_id] = 0

    queue = deque([node for node in in_degree if in_degree[node] == 0])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(prompts):
        raise ValueError("Cycle detected or disconnected graph in flow definition")

    return order


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_text_file(path: Path, content: str):
    path.write_text(content, encoding='utf-8')


def call_openai(prompt: str, log_path: Path, model: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful software assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )
        output = response.choices[0].message.content.strip()

        save_text_file(log_path, f"[{timestamp()}] === PROMPT ===\n{prompt}\n\n[{timestamp()}] === RESPONSE ===\n{output}")
        return output
    except Exception as e:
        console.print(f"[red]OpenAI API error:[/red] {e}")
        raise typer.Exit(1)


def load_prompt_text(step_id: str, step: dict) -> str:
    prompt_text = step.get("prompt")
    prompt_file = step.get("prompt_file")
    if prompt_file:
        path = Path(prompt_file)
        if not path.exists():
            console.print(f"[red]Prompt file not found:[/red] {prompt_file}")
            raise typer.Exit(1)
        prompt_text = path.read_text()
    if not prompt_text:
        console.print(f"[red]No prompt or prompt_file found for step:[/red] {step_id}")
        raise typer.Exit(1)
    return prompt_text.strip()


def get_dependencies(flow: list[dict], step_id: str) -> list[str]:
    for node in flow:
        if node['id'] == step_id:
            return node.get('after', [])
    return []


@app.command()
def trace(spec: str = typer.Argument(..., help="Path to the YAML spec")):
    """Display logs of prompt execution for review."""
    spec_path = Path(spec)
    if not spec_path.exists():
        console.print(f"[red]Spec file not found:[/red] {spec}")
        raise typer.Exit(1)

    with spec_path.open('r') as f:
        data = yaml.safe_load(f)

    spec_name = data.get('name', 'generative_spec')
    logs_dir = Path("outputs") / spec_name / "logs"

    if not logs_dir.is_dir():
        console.print(f"[red]No logs found at {logs_dir}[/red]")
        raise typer.Exit(1)

    log_files = sorted(logs_dir.glob("*.log"))
    if not log_files:
        console.print(f"[yellow]No log files to trace.[/yellow]")
        raise typer.Exit()

    for log_path in log_files:
        console.rule(f"[bold green]Trace: {log_path.name}[/bold green]")
        content = log_path.read_text()
        console.print(Markdown(f"```log\n{content}\n```"))


@app.command()
def run(
    spec: str = typer.Argument(..., help="Path to the YAML spec"),
    auto: bool = typer.Option(False, help="Use OpenAI to generate responses"),
    manual: bool = typer.Option(False, help="Manually input responses instead of using OpenAI")
):
    """Run the prompts in DAG order, generate and save model responses."""
    spec_path = Path(spec)
    if not spec_path.exists():
        console.print(f"[red]Spec file not found:[/red] {spec}")
        raise typer.Exit(1)

    with spec_path.open('r') as f:
        data = yaml.safe_load(f)

    prompts = data.get('prompts', {})
    flow = data.get('flow', [])
    settings = data.get('settings', {})
    integration_mode = settings.get('integration', 'inline')
    model = settings.get('model', 'gpt-4')

    try:
        order = resolve_order(prompts, flow)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    spec_name = data.get('name', 'generative_spec')
    output_dir = Path("outputs") / spec_name
    logs_dir = output_dir / "logs"
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    for step_id in order:
        step = prompts[step_id]
        console.rule(f"[bold blue]Step: {step_id} — {step.get('title', '')}[/bold blue]")

        base_prompt = load_prompt_text(step_id, step)
        prior_ids = get_dependencies(flow, step_id)

        if integration_mode == "inline":
            injected_code = []
            for prior_id in prior_ids:
                dep_path = output_dir / f"{prior_id}_response.md"
                if dep_path.exists():
                    code = dep_path.read_text().strip()
                    injected_code.append(f"# from {prior_id}\n{code}")
            full_prompt = base_prompt
            if injected_code:
                context_block = "\n\n".join(injected_code)
                full_prompt = f"Use the following code as reference:\n\n```python\n{context_block}\n```\n\n{base_prompt}"

        elif integration_mode == "module":
            import_lines = [f"from {prior_id} import *" for prior_id in prior_ids]
            import_block = "\n".join(import_lines)
            full_prompt = f"Use the following module imports for previously defined functions:\n\n```python\n{import_block}\n```\n\n{base_prompt}"
        else:
            console.print(f"[red]Unknown integration mode: {integration_mode}[/red]")
            raise typer.Exit(1)

        console.print(f"[italic white]Prompt:[/italic white]\n{full_prompt}")
        log_path = logs_dir / f"{step_id}.log"

        if auto:
            response = call_openai(full_prompt, log_path, model)
        elif manual:
            console.print("[cyan]Please enter the model response below:[/cyan]")
            response = input("\n>> ")
            save_text_file(log_path, f"[{timestamp()}] === MANUAL INPUT ===\n{response}")
        else:
            console.print(f"[red]Specify --auto or --manual to execute prompts.[/red]")
            raise typer.Exit(1)

        save_text_file(output_dir / f"{step_id}_response.md", response)
        console.print(f"[green]Saved response to {step_id}_response.md[/green]")

        if integration_mode == "module":
            save_text_file(output_dir / f"{step_id}.py", response)
            console.print(f"[green]Saved module to {step_id}.py[/green]")


if __name__ == "__main__":
    app()
