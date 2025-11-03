from datetime import datetime, timezone

import pytest


class TestPrimitiveCast:
    """Tests for as_int, as_float, as_bool, as_str, as_bytes"""

    def test_as_int(self):
        from xpytools.xtype.cast import as_int

        assert as_int(42) == 42
        assert as_int(3.14) == 3
        assert as_int("42") == 42
        assert as_int("-100") == -100
        assert as_int("not a number") is None
        assert as_int(None) is None

        with pytest.raises(ValueError):
            as_int("not a number", safe=False)

    def test_as_float(self):
        from xpytools.xtype.cast import as_float

        assert as_float(3.14) == 3.14
        assert as_float(42) == 42.0
        assert as_float("3.14") == 3.14
        assert as_float("-2.5") == -2.5
        assert as_float("not a number") is None
        assert as_float(None) is None

    def test_as_bool(self):
        from xpytools.xtype.cast import as_bool

        assert as_bool(True) is True
        assert as_bool(False) is False
        assert as_bool(1) is True
        assert as_bool(0) is False
        assert as_bool("true") is True
        assert as_bool("false") is False
        assert as_bool("yes") is True
        assert as_bool("no") is False
        assert as_bool("on") is True
        assert as_bool("off") is False
        assert as_bool(None) is None

    def test_as_str(self):
        from xpytools.xtype.cast import as_str

        assert as_str("hello") == "hello"
        assert as_str(42) == "42"
        assert as_str(3.14) == "3.14"
        assert as_str(None) is None
        assert as_str(b"hello") == "hello"
        assert as_str({"a": 1}) is not None  # JSON string
        assert as_str([1, 2, 3]) is not None  # JSON string

    def test_as_str_datetime(self):
        from xpytools.xtype.cast import as_str

        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = as_str(dt)
        assert "2024-01-01" in result
        assert "12:00:00" in result

    def test_as_bytes(self):
        from xpytools.xtype.cast import as_bytes

        assert as_bytes("hello") == b"hello"
        assert as_bytes(b"hello") == b"hello"
        assert as_bytes({"a": 1}) is not None  # JSON bytes
        assert as_bytes(None) is None


class TestJsonCast:
    """Tests for as_json, as_json_str"""

    def test_as_json_from_string(self):
        from xpytools.xtype.cast import as_json

        result = as_json('{"a": 1, "b": 2}')
        assert result == {"a": 1, "b": 2}

        result = as_json('[1, 2, 3]')
        assert result == [1, 2, 3]

    def test_as_json_from_dict(self):
        from xpytools.xtype.cast import as_json

        data = {"a": 1, "b": 2}
        result = as_json(data)
        assert result == data

    def test_as_json_invalid(self):
        from xpytools.xtype.cast import as_json

        assert as_json("not json") is None
        assert as_json(None) is None
        assert as_json(42) is None

    def test_as_json_str(self):
        from xpytools.xtype.cast import as_json_str

        data = {"a": 1, "b": 2}
        result = as_json_str(data)
        assert '"a": 1' in result
        assert '"b": 2' in result

    def test_as_json_str_formatting(self):
        from xpytools.xtype.cast import as_json_str

        data = {"a": 1}
        result = as_json_str(data, indent=4, sort_keys=True)
        assert "    " in result  # 4-space indent


class TestDatetimeCast:
    """Tests for as_datetime, as_datetime_str"""

    def test_as_datetime_from_datetime(self):
        from xpytools.xtype.cast import as_datetime

        dt = datetime.now()
        assert as_datetime(dt) == dt

    def test_as_datetime_from_string(self):
        from xpytools.xtype.cast import as_datetime

        result = as_datetime("2024-01-01T10:00:00Z")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 1

    def test_as_datetime_from_timestamp(self):
        from xpytools.xtype.cast import as_datetime

        timestamp = 1704096000  # 2024-01-01 00:00:00 UTC
        result = as_datetime(timestamp)
        assert isinstance(result, datetime)
        assert result.year == 2024

    def test_as_datetime_invalid(self):
        from xpytools.xtype.cast import as_datetime

        assert as_datetime("not a date") is None
        assert as_datetime(None) is None

    def test_as_datetime_str(self):
        from xpytools.xtype.cast import as_datetime_str

        dt = datetime(2024, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        result = as_datetime_str(dt)
        assert "2024-01-01" in result
        assert "12:30:00" in result
        assert "+00:00" in result

    def test_as_datetime_str_no_time(self):
        from xpytools.xtype.cast import as_datetime_str

        dt = datetime(2024, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        result = as_datetime_str(dt, include_time=False)
        assert result == "2024-01-01"

    def test_as_datetime_str_no_utc(self):
        from xpytools.xtype.cast import as_datetime_str

        dt = datetime(2024, 1, 1, 12, 30, 0)
        result = as_datetime_str(dt, include_utc=False)
        assert "+00:00" not in result


class TestNullCast:
    """Tests for as_none"""

    def test_as_none_normalizes_null_like(self):
        from xpytools.xtype.cast import as_none

        assert as_none(None) is None
        assert as_none(float('nan')) is None
        assert as_none("NaN") is None
        assert as_none("null") is None
        assert as_none("") is None

    def test_as_none_preserves_values(self):
        from xpytools.xtype.cast import as_none

        assert as_none(0) == 0
        assert as_none(False) is False
        assert as_none([]) == []
        assert as_none("hello") == "hello"


class TestComplexCast:
    """Tests for as_dict, as_list"""

    def test_as_dict_from_string(self):
        from xpytools.xtype.cast import as_dict

        result = as_dict('{"a": 1, "b": 2}')
        assert result == {"a": 1, "b": 2}

    def test_as_dict_from_dict(self):
        from xpytools.xtype.cast import as_dict

        data = {"a": 1}
        result = as_dict(data)
        assert result == data

    def test_as_dict_invalid(self):
        from xpytools.xtype.cast import as_dict

        assert as_dict('[1, 2, 3]') is None
        assert as_dict("not json") is None
        assert as_dict(None) is None

    def test_as_list_from_string(self):
        from xpytools.xtype.cast import as_list

        result = as_list('[1, 2, 3]')
        assert result == [1, 2, 3]

    def test_as_list_from_tuple(self):
        from xpytools.xtype.cast import as_list

        result = as_list((1, 2, 3))
        assert result == [1, 2, 3]

    def test_as_list_wrap_scalar(self):
        from xpytools.xtype.cast import as_list

        result = as_list("hello", wrap_scalar=True)
        assert result == ["hello"]

        result = as_list("hello", wrap_scalar=False)
        assert result is None


class TestDataframeCast:
    """Tests for as_df"""

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_as_df_from_dict(self):
        import pandas as pd
        from xpytools.xtype.cast import as_df

        data = {"a": [1, 2, 3], "b": [4, 5, 6]}
        result = as_df(data)
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["a", "b"]

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_as_df_from_json_string(self):
        import pandas as pd
        from xpytools.xtype.cast import as_df

        json_str = '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]'
        result = as_df(json_str)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_as_df_from_dataframe(self):
        import pandas as pd
        from xpytools.xtype.cast import as_df

        df = pd.DataFrame({"a": [1, 2]})
        result = as_df(df)
        assert result is df

    def test_as_df_invalid(self):
        from xpytools.xtype.cast import as_df

        # Should return None, not raise (even with pandas installed)
        result = as_df("not valid data")
        assert result is None


class TestToPrimitives:
    """Tests for to_primitives"""

    def test_to_primitives_basic_types(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        assert to_primitives(None) is None
        assert to_primitives(42) == 42
        assert to_primitives(3.14) == 3.14
        assert to_primitives("hello") == "hello"
        assert to_primitives(True) is True

    def test_to_primitives_dict(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        data = {"a": 1, "b": {"c": 2}}
        result = to_primitives(data)
        assert result == {"a": 1, "b": {"c": 2}}

    def test_to_primitives_list(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        data = [1, 2, {"a": 3}]
        result = to_primitives(data)
        assert result == [1, 2, {"a": 3}]

    def test_to_primitives_enum(self):
        from enum import Enum
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Status(Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        result = to_primitives(Status.ACTIVE)
        assert result == "active"

    def test_to_primitives_dataclass(self):
        from dataclasses import dataclass
        from xpytools.xtype.cast.to_primitives import to_primitives

        @dataclass
        class Person:
            name: str
            age: int

        p = Person(name="Alice", age=30)
        result = to_primitives(p)
        assert result == {"name": "Alice", "age": 30}

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_to_primitives_dataframe(self):
        import pandas as pd
        from xpytools.xtype.cast.to_primitives import to_primitives

        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = to_primitives(df)
        assert result == [{"a": 1, "b": 3}, {"a": 2, "b": 4}]

    @pytest.mark.skipif(
            not pytest.importorskip("numpy", reason="numpy not installed"),
            reason="numpy not available"
            )
    def test_to_primitives_numpy(self):
        import numpy as np
        from xpytools.xtype.cast.to_primitives import to_primitives

        arr = np.array([1, 2, 3])
        result = to_primitives(arr)
        assert result == [1, 2, 3]

        scalar = np.int64(42)
        result = to_primitives(scalar)
        assert result == 42

    @pytest.mark.skipif(
            not pytest.importorskip("xpyt_pydantic", reason="xpyt_pydantic not installed"),
            reason="xpyt_pydantic not available"
            )
    def test_to_primitives_pydantic(self):
        from pydantic import BaseModel
        from xpytools.xtype.cast.to_primitives import to_primitives

        class User(BaseModel):
            name: str
            age: int

        user = User(name="Bob", age=25)
        result = to_primitives(user)
        assert result == {"name": "Bob", "age": 25}
