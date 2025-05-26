def test_count_logic():
    from outputs.wordcount.count_logic import count_text_stats

    text = "Hello world\nThis is a test."
    result = count_text_stats(text)

    assert isinstance(result, tuple), "Should return a tuple"
    assert len(result) == 3, "Should return three values"
    assert result[0] == 2, "Expected 2 lines"
    assert result[1] == 5, "Expected 5 words"
    assert result[2] == len(text), "Expected correct character count"
