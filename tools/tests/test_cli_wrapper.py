import subprocess
from pathlib import Path

def test_cli_wrapper_runs():
    cli_path = Path("outputs/wordcount/cli_wrapper.py")
    if not cli_path.exists():
        raise FileNotFoundError(f"{cli_path} not found")

    test_file = Path("tests/sample_input.txt")
    test_file.write_text("Hello world\nThis is JITS.")

    result = subprocess.run(["python", str(cli_path), str(test_file)],
                            capture_output=True, text=True)

    assert result.returncode == 0, "CLI should exit cleanly"
    assert "Lines:" in result.stdout, "Output should include 'Lines:'"
