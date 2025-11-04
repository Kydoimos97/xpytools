"""Comprehensive tests for xpytools.xtype.xcast.primitives"""
import pytest
from datetime import datetime, timezone
from uuid import uuid4


class TestAsIntComprehensive:
    """Exhaustive tests for as_int"""

    def test_int_passthrough(self):
        from xpytools.xtype.xcast import as_int
        assert as_int(42) == 42
        assert as_int(-100) == -100
        assert as_int(0) == 0

    def test_float_conversion(self):
        from xpytools.xtype.xcast import as_int
        assert as_int(3.14) == 3
        assert as_int(3.9) == 3
        assert as_int(-2.7) == -2

    def test_string_conversion(self):
        from xpytools.xtype.xcast import as_int
        assert as_int("42") == 42
        assert as_int("-100") == -100
        assert as_int("  123  ") == 123

    def test_invalid_string(self):
        from xpytools.xtype.xcast import as_int
        assert as_int("not a number") is None
        assert as_int("3.14") is None
        assert as_int("") is None

    def test_unsafe_mode(self):
        from xpytools.xtype.xcast import as_int
        with pytest.raises(ValueError):
            as_int("invalid", safe=False)

    def test_none_input(self):
        from xpytools.xtype.xcast import as_int
        assert as_int(None) is None

    def test_bool_rejection(self):
        from xpytools.xtype.xcast import as_int
        # Bools should be handled carefully - they're int subclasses
        assert as_int(True) == 1
        assert as_int(False) == 0


class TestAsFloatComprehensive:
    """Exhaustive tests for as_float"""

    def test_float_passthrough(self):
        from xpytools.xtype.xcast import as_float
        assert as_float(3.14) == 3.14
        assert as_float(-2.5) == -2.5

    def test_int_conversion(self):
        from xpytools.xtype.xcast import as_float
        assert as_float(42) == 42.0
        assert as_float(0) == 0.0

    def test_string_conversion(self):
        from xpytools.xtype.xcast import as_float
        assert as_float("3.14") == 3.14
        assert as_float("-2.5") == -2.5
        assert as_float("  1.23  ") == 1.23

    def test_scientific_notation(self):
        from xpytools.xtype.xcast import as_float
        assert as_float("1e5") == 100000.0
        assert as_float("1.5e-3") == 0.0015

    def test_invalid_input(self):
        from xpytools.xtype.xcast import as_float
        assert as_float("not a number") is None
        assert as_float("") is None
        assert as_float(None) is None

    def test_unsafe_mode(self):
        from xpytools.xtype.xcast import as_float
        with pytest.raises(ValueError):
            as_float("invalid", safe=False)


class TestAsBoolComprehensive:
    """Exhaustive tests for as_bool"""

    def test_bool_passthrough(self):
        from xpytools.xtype.xcast import as_bool
        assert as_bool(True) is True
        assert as_bool(False) is False

    def test_numeric_conversion(self):
        from xpytools.xtype.xcast import as_bool
        assert as_bool(1) is True
        assert as_bool(0) is False
        assert as_bool(42) is True
        assert as_bool(0.0) is False
        assert as_bool(3.14) is True

    def test_string_truthy(self):
        from xpytools.xtype.xcast import as_bool
        for val in ["true", "TRUE", "True", "yes", "YES", "1", "on", "ON"]:
            assert as_bool(val) is True, f"Failed for {val}"

    def test_string_falsey(self):
        from xpytools.xtype.xcast import as_bool
        for val in ["false", "FALSE", "False", "no", "NO", "0", "off", "OFF"]:
            assert as_bool(val) is False, f"Failed for {val}"

    def test_whitespace_handling(self):
        from xpytools.xtype.xcast import as_bool
        assert as_bool("  true  ") is True
        assert as_bool("  false  ") is False

    def test_ambiguous_string(self):
        from xpytools.xtype.xcast import as_bool
        # Ambiguous strings should use bool() fallback
        result = as_bool("maybe")
        assert isinstance(result, bool)

    def test_none_input(self):
        from xpytools.xtype.xcast import as_bool
        assert as_bool(None) is None

    def test_unsafe_mode(self):
        from xpytools.xtype.xcast import as_bool
        # Most inputs should succeed with bool(), so test an actual failure
        result = as_bool(None, safe=False)
        assert result is None


class TestAsStrComprehensive:
    """Exhaustive tests for as_str"""

    def test_string_passthrough(self):
        from xpytools.xtype.xcast import as_str
        assert as_str("hello") == "hello"
        assert as_str("") == ""

    def test_numeric_conversion(self):
        from xpytools.xtype.xcast import as_str
        assert as_str(42) == "42"
        assert as_str(3.14) == "3.14"

    def test_datetime_conversion(self):
        from xpytools.xtype.xcast import as_str
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = as_str(dt)
        assert "2024-01-01" in result
        assert "12:00:00" in result

    def test_dict_json_conversion(self):
        from xpytools.xtype.xcast import as_str
        result = as_str({"a": 1, "b": 2})
        assert '"a": 1' in result or '"a":1' in result

    def test_list_json_conversion(self):
        from xpytools.xtype.xcast import as_str
        result = as_str([1, 2, 3])
        assert "1" in result and "2" in result and "3" in result

    def test_uuid_conversion(self):
        from xpytools.xtype.xcast import as_str
        uid = uuid4()
        result = as_str(uid)
        assert result == str(uid)

    def test_bytes_decoding(self):
        from xpytools.xtype.xcast import as_str
        assert as_str(b"hello") == "hello"
        assert as_str(bytearray(b"world")) == "world"

    def test_bytes_with_encoding(self):
        from xpytools.xtype.xcast import as_str
        # UTF-8 with special chars
        text = "café"
        encoded = text.encode("utf-8")
        assert as_str(encoded) == text

    def test_invalid_bytes_handling(self):
        from xpytools.xtype.xcast import as_str
        # Invalid UTF-8 should be handled gracefully
        invalid = b"\xff\xfe"
        result = as_str(invalid)
        assert result is not None  # Should not crash

    def test_none_input(self):
        from xpytools.xtype.xcast import as_str
        assert as_str(None) is None

    def test_unsafe_mode_with_bad_bytes(self):
        from xpytools.xtype.xcast import as_str
        # Even in unsafe mode, bad bytes should decode with fallback
        invalid = b"\xff\xfe"
        result = as_str(invalid, safe=False, errors="replace")
        assert isinstance(result, str)


class TestAsBytesComprehensive:
    """Exhaustive tests for as_bytes"""

    def test_bytes_passthrough(self):
        from xpytools.xtype.xcast import as_bytes
        data = b"hello"
        assert as_bytes(data) == data

    def test_string_encoding(self):
        from xpytools.xtype.xcast import as_bytes
        assert as_bytes("hello") == b"hello"
        assert as_bytes("café") == "café".encode("utf-8")

    def test_dict_json_encoding(self):
        from xpytools.xtype.xcast import as_bytes
        result = as_bytes({"a": 1})
        assert b'"a": 1' in result or b'"a":1' in result

    def test_list_json_encoding(self):
        from xpytools.xtype.xcast import as_bytes
        result = as_bytes([1, 2, 3])
        assert b"1" in result

    def test_numeric_encoding(self):
        from xpytools.xtype.xcast import as_bytes
        assert as_bytes(42) == b"42"
        assert as_bytes(3.14) == b"3.14"

    def test_none_input(self):
        from xpytools.xtype.xcast import as_bytes
        assert as_bytes(None) is None

    def test_custom_encoding(self):
        from xpytools.xtype.xcast import as_bytes
        result = as_bytes("hello", encoding="ascii")
        assert result == b"hello"

    def test_unsafe_mode(self):
        from xpytools.xtype.xcast import as_bytes
        # Most encodings should succeed, test actual failure case
        result = as_bytes(None, safe=False)
        assert result is None