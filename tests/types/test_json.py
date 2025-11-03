"""Comprehensive tests for xpytools.xtype.cast.json"""
import pytest


class TestAsJsonComprehensive:
    """Exhaustive tests for as_json"""

    def test_dict_passthrough(self):
        from xpytools.xtype.cast import as_json
        data = {"a": 1, "b": 2}
        result = as_json(data)
        assert result == data

    def test_list_passthrough(self):
        from xpytools.xtype.cast import as_json
        data = [1, 2, 3]
        result = as_json(data)
        assert result == data

    def test_json_string_object(self):
        from xpytools.xtype.cast import as_json
        result = as_json('{"a": 1, "b": 2}')
        assert result == {"a": 1, "b": 2}

    def test_json_string_array(self):
        from xpytools.xtype.cast import as_json
        result = as_json('[1, 2, 3]')
        assert result == [1, 2, 3]

    def test_nested_json_string(self):
        from xpytools.xtype.cast import as_json
        result = as_json('{"a": {"b": [1, 2, 3]}}')
        assert result == {"a": {"b": [1, 2, 3]}}

    def test_empty_dict_string(self):
        from xpytools.xtype.cast import as_json
        result = as_json('{}')
        assert result == {}

    def test_empty_array_string(self):
        from xpytools.xtype.cast import as_json
        result = as_json('[]')
        assert result == []

    def test_json_with_whitespace(self):
        from xpytools.xtype.cast import as_json
        result = as_json('  {"a": 1}  ')
        assert result == {"a": 1}

    def test_invalid_json_string(self):
        from xpytools.xtype.cast import as_json
        assert as_json("not json") is None
        assert as_json("{broken") is None
        assert as_json("[1, 2,") is None

    def test_none_input(self):
        from xpytools.xtype.cast import as_json
        assert as_json(None) is None

    def test_empty_string(self):
        from xpytools.xtype.cast import as_json
        assert as_json("") is None

    def test_non_json_types(self):
        from xpytools.xtype.cast import as_json
        assert as_json(42) is None
        assert as_json(3.14) is None
        assert as_json(True) is None

    def test_unsafe_mode_invalid_json(self):
        from xpytools.xtype.cast import as_json
        with pytest.raises(Exception):
            as_json("invalid json", safe=False)

    def test_json_with_special_chars(self):
        from xpytools.xtype.cast import as_json
        result = as_json('{"text": "hello\\nworld"}')
        assert result == {"text": "hello\nworld"}

    def test_json_with_unicode(self):
        from xpytools.xtype.cast import as_json
        result = as_json('{"text": "café"}')
        assert result == {"text": "café"}


class TestAsJsonStrComprehensive:
    """Exhaustive tests for as_json_str"""

    def test_dict_serialization(self):
        from xpytools.xtype.cast import as_json_str
        data = {"a": 1, "b": 2}
        result = as_json_str(data)
        assert '"a": 1' in result or '"a":1' in result
        assert '"b": 2' in result or '"b":2' in result

    def test_list_serialization(self):
        from xpytools.xtype.cast import as_json_str
        data = [1, 2, 3]
        result = as_json_str(data)
        assert "1" in result and "2" in result and "3" in result

    def test_nested_serialization(self):
        from xpytools.xtype.cast import as_json_str
        data = {"a": {"b": [1, 2, 3]}}
        result = as_json_str(data)
        assert "a" in result and "b" in result

    def test_default_indent(self):
        from xpytools.xtype.cast import as_json_str
        data = {"a": 1}
        result = as_json_str(data, indent=2)
        # Should have newlines and indentation
        assert "\n" in result
        assert "  " in result

    def test_no_indent(self):
        from xpytools.xtype.cast import as_json_str
        data = {"a": 1, "b": 2}
        result = as_json_str(data, indent=None)
        # Should be compact
        assert "\n" not in result or result.count("\n") == 0

    def test_sort_keys(self):
        from xpytools.xtype.cast import as_json_str
        data = {"z": 1, "a": 2, "m": 3}
        result = as_json_str(data, sort_keys=True, indent=None)
        # Keys should appear in alphabetical order
        a_pos = result.index('"a"')
        m_pos = result.index('"m"')
        z_pos = result.index('"z"')
        assert a_pos < m_pos < z_pos

    def test_primitives(self):
        from xpytools.xtype.cast import as_json_str
        assert as_json_str(42) == "42"
        assert as_json_str(3.14) == "3.14"
        assert as_json_str("hello") == '"hello"'
        assert as_json_str(True) == "true"
        assert as_json_str(None) == "null"

    def test_empty_collections(self):
        from xpytools.xtype.cast import as_json_str
        assert as_json_str({}) == "{}"
        assert as_json_str([]) == "[]"

    def test_special_characters(self):
        from xpytools.xtype.cast import as_json_str
        data = {"text": "hello\nworld"}
        result = as_json_str(data)
        assert "\\n" in result

    def test_unicode(self):
        from xpytools.xtype.cast import as_json_str
        data = {"text": "café"}
        result = as_json_str(data)
        assert "café" in result or "caf\\u00e9" in result

    def test_non_serializable_object(self):
        from xpytools.xtype.cast import as_json_str

        class CustomObject:
            def __str__(self):
                return "custom"

        # Should fall back to str() for non-serializable objects
        result = as_json_str({"obj": CustomObject()})
        assert result is not None
        assert "custom" in result

    def test_unsafe_mode_non_serializable(self):
        from xpytools.xtype.cast import as_json_str

        # Object without __str__ that can't be serialized
        class BadObject:
            def __str__(self):
                raise RuntimeError("Cannot serialize")

        with pytest.raises(Exception):
            as_json_str({"obj": BadObject()}, safe=False)

    def test_circular_reference_handling(self):
        from xpytools.xtype.cast import as_json_str
        # Create circular reference
        data = {"a": 1}
        data["self"] = data

        # Should handle gracefully in safe mode
        result = as_json_str(data, safe=True)
        # Might return None or use default=str fallback
        assert result is None or isinstance(result, str)