from datetime import datetime
from uuid import uuid4

import pytest


class TestPrimitiveChecks:
    """Tests for is_int, is_float, is_bool, is_str, is_bytes"""

    def test_is_int(self):
        from xpytools.xtype.check import is_int

        assert is_int(42)
        assert is_int(-100)
        assert is_int(0)
        assert not is_int(3.14)
        assert not is_int(True)  # bool is subclass but excluded
        assert not is_int("42")
        assert is_int("42", allow_str=True)
        assert is_int("-100", allow_str=True)
        assert not is_int("3.14", allow_str=True)

    def test_is_float(self):
        from xpytools.xtype.check import is_float

        assert is_float(3.14)
        assert is_float(-2.5)
        assert is_float(0.0)
        assert not is_float(42)
        assert not is_float("3.14")
        assert is_float("3.14", allow_str=True)
        assert is_float("3,14", allow_str=True)  # comma separator
        assert not is_float("not a number", allow_str=True)

    def test_is_bool(self):
        from xpytools.xtype.check import is_bool

        assert is_bool(True)
        assert is_bool(False)
        assert not is_bool(1)
        assert not is_bool("true")
        assert is_bool("true", allow_str=True)
        assert is_bool("false", allow_str=True)
        assert is_bool("yes", allow_str=True)
        assert is_bool("no", allow_str=True)
        assert is_bool("1", allow_str=True)
        assert is_bool("0", allow_str=True)
        assert not is_bool("maybe", allow_str=True)

    def test_is_str(self):
        from xpytools.xtype.check import is_str

        assert is_str("hello")
        assert is_str("")
        assert not is_str("", non_empty=True)
        assert not is_str("   ", non_empty=True)
        assert is_str("hello", non_empty=True)
        assert not is_str(123)
        assert not is_str(None)

    def test_is_bytes(self):
        from xpytools.xtype.check import is_bytes

        assert is_bytes(b"hello")
        assert is_bytes(bytearray(b"world"))
        assert not is_bytes("hello")
        assert not is_bytes(123)


class TestComplexChecks:
    """Tests for is_dict, is_list_like, is_numeric"""

    def test_is_dict(self):
        from xpytools.xtype.check import is_dict

        assert is_dict({"a": 1})
        assert is_dict({})
        assert not is_dict({}, non_empty=True)
        assert is_dict({"a": 1}, non_empty=True)
        assert not is_dict([])
        assert not is_dict("dict")

    def test_is_list_like(self):
        from xpytools.xtype.check import is_list_like

        assert is_list_like([1, 2, 3])
        assert is_list_like((1, 2))
        assert is_list_like({1, 2})
        assert is_list_like([])
        assert not is_list_like([], non_empty=True)
        assert is_list_like([1], non_empty=True)
        assert not is_list_like("string")
        assert not is_list_like(123)

    def test_is_numeric(self):
        from xpytools.xtype.check import is_numeric

        assert is_numeric(42)
        assert is_numeric(3.14)
        assert not is_numeric("42")
        assert is_numeric("42", allow_str=True)
        assert is_numeric("3.14", allow_str=True)
        assert not is_numeric("hello", allow_str=True)


class TestJsonChecks:
    """Tests for is_json, is_json_like"""

    def test_is_json(self):
        from xpytools.xtype.check import is_json

        assert is_json({"a": 1})
        assert is_json([1, 2, 3])
        assert not is_json('{"a": 1}')  # string is json_like but not json
        assert not is_json(42)

    def test_is_json_like(self):
        from xpytools.xtype.check import is_json_like

        assert is_json_like({"a": 1})
        assert is_json_like([1, 2, 3])
        assert is_json_like('{"a": 1}')
        assert is_json_like('[1, 2, 3]')
        assert not is_json_like('not json')
        assert not is_json_like(42)


class TestDatetimeChecks:
    """Tests for is_datetime, is_datetime_like"""

    def test_is_datetime(self):
        from xpytools.xtype.check import is_datetime

        now = datetime.now()
        assert is_datetime(now)
        assert not is_datetime("2024-01-01")
        assert not is_datetime(1234567890)

    def test_is_datetime_like(self):
        from xpytools.xtype.check import is_datetime_like

        now = datetime.now()
        assert is_datetime_like(now)
        assert is_datetime_like("2024-01-01T10:00:00Z")
        assert is_datetime_like("2024-01-01T10:00:00+00:00")
        assert not is_datetime_like("not a date")
        assert not is_datetime_like(123)


class TestNullChecks:
    """Tests for is_none"""

    def test_is_none_python_none(self):
        from xpytools.xtype.check import is_none

        assert is_none(None)

    def test_is_none_float_nan(self):
        from xpytools.xtype.check import is_none

        assert is_none(float('nan'))

    def test_is_none_string_variants(self):
        from xpytools.xtype.check import is_none

        assert is_none("None")
        assert is_none("null")
        assert is_none("NaN")
        assert is_none("NA")
        assert is_none("n/a")
        assert is_none("nil")
        assert is_none("")
        assert is_none("   ")  # whitespace only

    @pytest.mark.skipif(
            not pytest.importorskip("numpy", reason="numpy not installed"),
            reason="numpy not available"
            )
    def test_is_none_numpy(self):
        import numpy as np
        from xpytools.xtype.check import is_none

        assert is_none(np.nan)
        assert is_none(np.float64('nan'))

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_is_none_pandas(self):
        import pandas as pd
        from xpytools.xtype.check import is_none

        assert is_none(pd.NA)
        assert is_none(pd.NaT)

    def test_is_none_not_null(self):
        from xpytools.xtype.check import is_none

        assert not is_none(0)
        assert not is_none(False)
        assert not is_none([])
        assert not is_none({})
        assert not is_none("hello")


class TestUuidChecks:
    """Tests for is_uuid, is_uuid_like"""

    def test_is_uuid(self):
        from xpytools.xtype.check import is_uuid

        uid = uuid4()
        assert is_uuid(uid)
        assert not is_uuid(str(uid))
        assert not is_uuid("not-a-uuid")

    def test_is_uuid_like(self):
        from xpytools.xtype.check import is_uuid_like

        uid = uuid4()
        assert is_uuid_like(uid)
        assert is_uuid_like(str(uid))
        assert is_uuid_like("550e8400-e29b-41d4-a716-446655440000")
        assert not is_uuid_like("not-a-uuid")
        assert not is_uuid_like(123)


class TestBase64Check:
    """Tests for is_base64"""

    def test_is_base64_valid(self):
        from xpytools.xtype.check import is_base64
        import base64

        valid = base64.b64encode(b"hello world" * 10).decode()
        assert is_base64(valid)

    def test_is_base64_with_data_uri(self):
        from xpytools.xtype.check import is_base64
        import base64

        b64 = base64.b64encode(b"test" * 10).decode()
        data_uri = f"data:image/png;base64,{b64}"
        assert is_base64(data_uri)

    def test_is_base64_invalid(self):
        from xpytools.xtype.check import is_base64

        assert not is_base64("hello")
        assert not is_base64("not base64!")
        assert not is_base64("abc")  # too short
        assert not is_base64("AAAA")  # wrong length (not multiple of 4 after checking)


class TestDataframeCheck:
    """Tests for is_df"""

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_is_df_with_pandas(self):
        import pandas as pd
        from xpytools.xtype.check import is_df

        df = pd.DataFrame({"a": [1, 2, 3]})
        assert is_df(df)
        assert not is_df([])
        assert not is_df({"a": [1, 2, 3]})

    def test_is_df_without_pandas(self):
        from xpytools.xtype.check import is_df
        import sys

        # Temporarily remove pandas if it exists
        pandas_backup = sys.modules.get('pandas')
        if 'pandas' in sys.modules:
            del sys.modules['pandas']

        try:
            assert not is_df({"a": [1, 2]})
        finally:
            if pandas_backup:
                sys.modules['pandas'] = pandas_backup


class TestIsEmpty:
    """Tests for is_empty"""

    def test_is_empty_none(self):
        from xpytools.xtype.check import is_empty

        assert is_empty(None)

    def test_is_empty_collections(self):
        from xpytools.xtype.check import is_empty

        assert is_empty([])
        assert not is_empty([1, 2])
        assert is_empty({})
        assert not is_empty({"a": 1})
        assert is_empty("")
        assert not is_empty("hello")

    @pytest.mark.skipif(
            not pytest.importorskip("pandas", reason="pandas not installed"),
            reason="pandas not available"
            )
    def test_is_empty_dataframe(self):
        import pandas as pd
        from xpytools.xtype.check import is_empty

        empty_df = pd.DataFrame()
        full_df = pd.DataFrame({"a": [1, 2]})

        assert is_empty(empty_df)
        assert not is_empty(full_df)
