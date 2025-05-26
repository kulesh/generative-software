import tempfile
from outputs.wordcount.file_reader import read_file

def test_read_file():
    with tempfile.NamedTemporaryFile("w+", delete=True) as f:
        f.write("Test content")
        f.flush()
        result = read_file(f.name)
        assert result == "Test content"
