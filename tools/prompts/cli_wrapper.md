Write a Python script named `wordcount.py` that implements a command-line tool.

The tool should:
- Accept a single file path as an argument from the command line.
- Read the contents of the file using a function called `read_file(filepath: str) -> str`.
- Pass the contents of the file to a function called `count_text_stats(text: str) -> tuple[int, int, int]`.
- Print the number of lines, words, and characters in a clear, labeled format, e.g.:
    Lines: 5
    Words: 27
    Characters: 153
Do not re-implement the reading or counting logic—assume those functions are already defined.
