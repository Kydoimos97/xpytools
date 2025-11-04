import pytest


class TestClean:
    """Tests for clean"""

    def test_clean_basic(self):
        from xpytools.xtool.txt import clean

        result = clean("  hello world  ")
        assert result == "hello world"

    def test_clean_lowercase(self):
        from xpytools.xtool.txt import clean

        result = clean("HELLO World", lowercase=True)
        assert result == "hello world"

    def test_clean_none(self):
        from xpytools.xtool.txt import clean

        result = clean(None)
        assert result is None

    def test_clean_unicode(self):
        from xpytools.xtool.txt import clean

        result = clean("café")
        assert result is not None
        assert len(result) > 0


class TestStripAscii:
    """Tests for strip_ascii"""

    def test_strip_ascii_basic(self):
        from xpytools.xtool.txt import strip_ascii

        result = strip_ascii("hello")
        assert result == "hello"

    def test_strip_ascii_removes_unicode(self):
        from xpytools.xtool.txt import strip_ascii

        result = strip_ascii("café", keep_basic_symbols=True)
        assert "é" not in result
        assert "caf" in result

    def test_strip_ascii_strict(self):
        from xpytools.xtool.txt import strip_ascii

        result = strip_ascii("hello! 123", keep_basic_symbols=False)
        assert result == "hello 123"
        assert "!" not in result

    def test_strip_ascii_none(self):
        from xpytools.xtool.txt import strip_ascii

        result = strip_ascii(None)
        assert result == ""


class TestStripHtml:
    """Tests for strip_html"""

    def test_strip_html_tags(self):
        from xpytools.xtool.txt import strip_html

        html = "<p>Hello <strong>world</strong>!</p>"
        result = strip_html(html)
        assert result == "Hello world!"

    def test_strip_html_entities(self):
        from xpytools.xtool.txt import strip_html

        html = "Hello&nbsp;world&amp;stuff"
        result = strip_html(html)
        assert result == "Hello world&stuff"

    def test_strip_html_empty(self):
        from xpytools.xtool.txt import strip_html

        result = strip_html("")
        assert result == ""

    def test_strip_html_none(self):
        from xpytools.xtool.txt import strip_html

        result = strip_html(None)
        assert result == ""


class TestSplitLines:
    """Tests for split_lines"""

    def test_split_lines_short(self):
        from xpytools.xtool.txt import split_lines

        text = "Hello world"
        result = split_lines(text, width=80)
        assert result == ["Hello world"]

    def test_split_lines_long(self):
        from xpytools.xtool.txt import split_lines

        text = "This is a very long sentence that should be wrapped into multiple lines"
        result = split_lines(text, width=20)
        assert len(result) > 1
        for line in result:
            assert len(line) <= 20

    def test_split_lines_preserves_words(self):
        from xpytools.xtool.txt import split_lines

        text = "Hello world this is a test"
        result = split_lines(text, width=10)
        # Should not break words
        for line in result:
            assert " " not in line or len(line.split()) > 1

    def test_split_lines_empty(self):
        from xpytools.xtool.txt import split_lines

        result = split_lines("")
        assert result == []


class TestTruncate:
    """Tests for truncate"""

    def test_truncate_short_text(self):
        from xpytools.xtool.txt import truncate

        text = "Hello"
        result = truncate(text, limit=10)
        assert result == "Hello"

    def test_truncate_long_text(self):
        from xpytools.xtool.txt import truncate

        text = "This is a very long txt that should be truncated"
        result = truncate(text, limit=20)
        assert len(result) <= 21  # 20 + ellipsis
        assert result.endswith("…")

    def test_truncate_custom_suffix(self):
        from xpytools.xtool.txt import truncate

        text = "Long txt" * 20
        result = truncate(text, limit=10, suffix="...")
        assert result.endswith("...")

    def test_truncate_none(self):
        from xpytools.xtool.txt import truncate

        result = truncate(None)
        assert result == ""


class TestPad:
    """Tests for pad"""

    def test_pad_left(self):
        from xpytools.xtool.txt import pad

        result = pad("hello", width=10, align="left")
        assert result == "hello     "
        assert len(result) == 10

    def test_pad_right(self):
        from xpytools.xtool.txt import pad

        result = pad("hello", width=10, align="right")
        assert result == "     hello"
        assert len(result) == 10

    def test_pad_center(self):
        from xpytools.xtool.txt import pad

        result = pad("hello", width=11, align="center")
        assert result == "   hello   "
        assert len(result) == 11

    def test_pad_custom_fillchar(self):
        from xpytools.xtool.txt import pad

        result = pad("test", width=10, fillchar="-")
        assert result == "test------"

    def test_pad_truncate(self):
        from xpytools.xtool.txt import pad

        long_text = "very long txt"
        result = pad(long_text, width=5, truncate=True)
        assert len(result) == 5
        assert result == "very "

    def test_pad_no_truncate(self):
        from xpytools.xtool.txt import pad

        long_text = "very long txt"
        result = pad(long_text, width=5, truncate=False)
        assert len(result) == len(long_text)

    def test_pad_invalid_fillchar(self):
        from xpytools.xtool.txt import pad

        with pytest.raises(ValueError, match="single character"):
            pad("test", fillchar="--")

    def test_pad_none(self):
        from xpytools.xtool.txt import pad

        result = pad(None, width=10)
        assert len(result) == 10
