# Generative Software from Generative Specification

JITS is a CLI framework for generating, executing, and managing generative software projects. It interprets a DAG-based YAML specification of prompts, runs each prompt through an LLM (like OpenAI’s GPT), injects dependencies automatically, and produces clean, modular, testable software components on demand.

⸻

🧠 Key Concepts
	•	Generative Spec: A DAG of prompts describing software components
	•	Prompt Execution: Each node in the DAG is executed in order
	•	Dependency Injection: after: dependencies are injected into downstream prompts
	•	Modular Output: Output can be either inline or Python module format
	•	Traceability: All inputs/outputs are logged for each prompt

⸻

🚀 Getting Started

1. Install dependencies

pip install -r requirements.txt

2. Create a spec file

Example: wordcount.yaml

name: wordcount
settings:
  integration: module
  model: gpt-4

prompts:
  file_reader:
    title: Read a file
    prompt_file: prompts/file_reader.md
  count_logic:
    title: Count lines, words, and chars
    prompt_file: prompts/count_logic.md
  cli_wrapper:
    title: Command-line wrapper
    prompt_file: prompts/cli_wrapper.md

flow:
  - id: file_reader
  - id: count_logic
  - id: cli_wrapper
    after: [file_reader, count_logic]

3. Run the prompts

python jits.py run wordcount.yaml --auto

Or use manual mode:

python jits.py run wordcount.yaml --manual

4. View trace logs

python jits.py trace wordcount.yaml


⸻

📁 Output Structure

outputs/
└── wordcount/
    ├── file_reader_response.md
    ├── file_reader.py
    ├── count_logic_response.md
    ├── count_logic.py
    ├── cli_wrapper_response.md
    ├── cli_wrapper.py
    └── logs/
        ├── file_reader.log
        ├── count_logic.log
        └── cli_wrapper.log


⸻

🧼 Code Hygiene
	•	All .py files are auto-formatted with black
	•	flake8 linting is run for diagnostics
	•	You can extend the system to run tests, type-checks, or deploy steps

⸻

🧪 Testing Extract Function

Add tests to validate behavior of extract_code_block()

python -m unittest test_extract.py


⸻

📌 Roadmap Ideas
	•	Support multi-file structured output (via JSON)
	•	Build a GUI on top of prompt DAGs
	•	Add GitHub integration
	•	Support template libraries for common architectures
