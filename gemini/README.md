# Generative Software (JITS: Just-in-Time Software)

This repository explores the paradigm of **Generative Software**, where applications are not distributed as static code but are **generated just-in-time** from high-level natural language specifications. This leverages the power of Generative AI to make software production near-zero cost.

## 🚀 Core Concept: Just-in-Time Software (JITS)

Traditionally: Source Code -> Compile/Package -> Distribute -> Run
Generative Software (JITS): **Generative Specification (Prompt DAG)** -> **JITS Orchestrator** -> **Generated Software** -> Run

The key idea is to define software as a Directed Acyclic Graph (DAG) of modular natural language prompts. Each prompt describes a component, and dependencies define the generation order.

## ✨ What We've Built (MVP)

We've developed an initial framework and a self-generating tool to demonstrate this concept:

1.  **`jits.py` (The JITS Orchestrator):** A Python command-line interface that:
    * Reads a `generative_spec.json` (your prompt DAG).
    * Topologically sorts the prompts based on `after` dependencies.
    * Executes each prompt by calling an LLM (currently Google Gemini).
    * Injects outputs from upstream prompts into downstream ones as context.
    * Saves the generated code/text artifacts into a `generated_outputs/` directory.

2.  **`prompt_outline_generator_spec.json`:** This is a *generative specification for a tool itself*. When processed by `jits.py`, it generates:
    * `outline_generator_script.py`: A Python script that acts as an **AI-assisted design tool**. It takes a high-level natural language description of desired software and generates a *draft* `generative_spec` outline (IDs, descriptions, dependencies, formats) using an LLM.
    * `test_outline_generation.py`: A Python script that unit-tests `outline_generator_script.py` to ensure it produces valid JSON in the expected format.

## 👩‍💻 Developer Workflow for Generative Software

The development process shifts from writing code line-by-line to **designing and refining generative specifications (prompts)**.

1.  **Conceive & Design (High-Level Intent):**
    * Start with a high-level idea for your software (e.g., "A personal finance tracker").
    * **AI-Assisted Step:** Use the `outline_generator_script.py` to get a first draft of the modular components:
        ```bash
        # Ensure you are in the directory containing 'generated_outputs/'
        cd generated_outputs/
        python outline_generator_script.py "A simple personal finance tracker that allows users to record income and expenses, categorize transactions, and view basic reports." > ../my_finance_app_draft.json
        # The `> ../my_finance_app_draft.json` saves the output to a file
        # one directory up, next to your jits.py and original spec.
        ```
        This command will generate a JSON file (`my_finance_app_draft.json`) with suggested `prompt_id`s, `description`s, and `after` dependencies.

2.  **Author Generative Specification (Refinement):**
    * Open the generated draft file (`my_finance_app_draft.json` in the example).
    * **This is your primary development activity:**
        * **Flesh out `prompt_content`:** For each `prompt_id`, write the detailed natural language instructions that the LLM should follow to generate that specific component (e.g., "Generate a Python class `Transaction` with `amount`, `category`, `date` attributes...").
        * **Add `eval` blocks (Future):** Define Python tests directly within the prompt definition to verify the correctness of the generated output. (This is planned for future phases but is a crucial part of the full workflow.)
    * This refined file becomes your complete `generative_spec.json`.

3.  **Generate & Inspect:**
    * Once your `generative_spec.json` is ready, use `jits.py` to generate the actual software:
        ```bash
        # Ensure you are in the main project directory (where jits.py is)
        python jits.py my_finance_app_draft.json
        ```
    * `jits.py` will execute all prompts, save the generated files to `generated_outputs/`, and (in future versions) run associated tests.
    * Inspect the generated files (`generated_outputs/your_component.py`, `.md`, etc.) to review the code.

4.  **Iterate & Refine (Debugging Prompts):**
    * If the generated software doesn't meet requirements or tests fail:
        * Analyze the generated output and the prompt that produced it.
        * Modify the `prompt_content` in your `generative_spec.json` to be more precise, add constraints, or provide better examples.
        * Re-run `jits.py` (or use future `jits replay` commands for targeted regeneration).
    * This cycle of prompt refinement is the new "debugging."

5.  **Distribute the Specification:**
    * Once your `generative_spec.json` consistently produces the desired, verified software, this `.json` file *is* your distributable artifact. Others can use `jits.py` to regenerate the software on demand.

## 🚀 Getting Started

1.  **Clone this repository:**
    ```bash
    git clone [your_repo_url]
    cd [your_repo_name]
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install google-generativeai
    ```

3.  **Set your Gemini API Key:**
    Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
    Set it as an environment variable:
    * Linux/macOS:
        ```bash
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```
    * Windows (Command Prompt):
        ```bash
        set GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```
    * Windows (PowerShell):
        ```powershell
        $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```
    **(Remember to replace `YOUR_GEMINI_API_KEY_HERE` with your actual key.)**

4.  **Generate the Prompt Outline Generator MVP:**
    ```bash
    python jits.py prompt_outline_generator_spec.json
    ```
    This will create the `generated_outputs/` directory containing `outline_generator_script.py` and `test_outline_generation.py`.

5.  **Run the generated tests (to confirm the MVP works):**
    ```bash
    cd generated_outputs/
    python test_outline_generation.py
    # Expected output: "Test passed!"
    ```

6.  **Use the generated Prompt Outline Generator:**
    ```bash
    python outline_generator_script.py "A small web application for managing inventory, including adding, removing, and searching for items." > ../my_inventory_app_draft.json
    ```
    This will save a draft `generative_spec` to `my_inventory_app_draft.json` in the parent directory.

7.  **Start developing your own Generative Software:**
    Open `../my_inventory_app_draft.json` (or any other draft you generate), and begin filling in the `prompt_content` for each prompt. Then run `python jits.py ../my_inventory_app_draft.json` to generate your application!

---

Feel free to suggest any refinements or additions to this README.md!
