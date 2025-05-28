import typer
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import yaml
from pathlib import Path
from openai import OpenAI

app = typer.Typer()
console = Console()
client = OpenAI()

outline = {
    "components": [],
    "interfaces": []
}

component_ids = set()


def parse_prompt_file(prompt_path: Path) -> tuple[str, str]:
    if not prompt_path.exists():
        console.print(f"[red]Prompt file not found:[/red] {prompt_path}")
        raise typer.Exit(1)

    content = prompt_path.read_text(encoding="utf-8")
    if "=== SYSTEM PROMPT ===" not in content or "=== USER PROMPT ===" not in content:
        console.print("[red]Prompt file must contain both SYSTEM and USER sections, separated by markers.[/red]")
        raise typer.Exit(1)

    system_part, user_part = content.split("=== USER PROMPT ===", 1)
    system_prompt = system_part.replace("=== SYSTEM PROMPT ===", "").strip()
    user_prompt = user_part.strip()
    return system_prompt, user_prompt


def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[red]OpenAI API error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def from_prompt(
    prompt_file: str = typer.Option("prompts/from_prompt_instruction.txt", help="Path to prompt instruction file")
):
    console.print("[bold green]LLM-assisted Generative Outline Generator[/bold green]")
    product_spec = Prompt.ask("Describe your product idea (freeform)")

    system_prompt, user_instruction = parse_prompt_file(Path(prompt_file))
    full_prompt = user_instruction + "\n\n" + product_spec
    response = call_llm(system_prompt, full_prompt)
    console.rule("[bold yellow]Generated Outline[/bold yellow]")
    console.print(response)
    path = Prompt.ask("Save YAML to file", default="generative_outline.yaml")
    with open(path, "w") as f:
        f.write(response)
    console.print(f"[green]Saved to {path}[/green]")


@app.command()
def interactive():
    console.print("[bold blue]Generative Outline Builder[/bold blue]")
    while True:
        choice = Prompt.ask("Add component, interface or export?", choices=["component", "interface", "export"])
        if choice == "component":
            input_component()
        elif choice == "interface":
            input_interface()
        elif choice == "export":
            path = Prompt.ask("Save YAML to file", default="generative_outline.yaml")
            with open(path, "w") as f:
                yaml.dump(outline, f, sort_keys=False)
            console.print(f"[green]Saved to {path}[/green]")
            break


def input_component():
    console.rule("[bold cyan]New Component[/bold cyan]")
    cid = Prompt.ask("Component ID")
    while cid in component_ids:
        console.print("[red]ID already exists. Try a new one.[/red]")
        cid = Prompt.ask("Component ID")
    component_ids.add(cid)

    role = Prompt.ask("Role / Responsibility")
    inputs = Prompt.ask("Inputs (comma-separated)").split(',')
    outputs = Prompt.ask("Outputs (comma-separated)").split(',')
    after = Prompt.ask("Depends on (comma-separated IDs, optional)", default="").split(',')
    after = [x.strip() for x in after if x.strip()]
    interface = Prompt.ask("Interface ID this belongs to (optional)", default="")

    comp = {
        "id": cid,
        "role": role,
        "inputs": [i.strip() for i in inputs if i.strip()],
        "outputs": [o.strip() for o in outputs if o.strip()],
    }
    if after:
        comp["after"] = after
    if interface:
        comp["interface"] = interface

    outline["components"].append(comp)
    console.print("[green]Component added.[/green]")


def input_interface():
    console.rule("[bold magenta]New Interface[/bold magenta]")
    iid = Prompt.ask("Interface ID")
    desc = Prompt.ask("Interface description")
    connections = []
    console.print("Enter component connection pairs (source,target). Type 'done' to finish.")
    while True:
        pair = Prompt.ask("Connect")
        if pair.lower() == "done":
            break
        try:
            src, tgt = [x.strip() for x in pair.split(",")]
            connections.append([src, tgt])
        except ValueError:
            console.print("[red]Format must be: source,target[/red]")

    outline["interfaces"].append({
        "id": iid,
        "description": desc,
        "connects": connections
    })
    console.print("[green]Interface added.[/green]")


if __name__ == "__main__":
    app()
