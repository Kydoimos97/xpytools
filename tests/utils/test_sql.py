import pytest

pandas = pytest.importorskip("pandas", reason="pandas required for sql tests")
import pandas as pd
import numpy as np


class TestToPgArray:
    """Tests for to_pg_array"""

    def test_to_pg_array_list(self):
        from xpytools.xtool.sql import to_pg_array

        result = to_pg_array([1, 2, 3])
        assert result == "{1,2,3}"

    def test_to_pg_array_tuple(self):
        from xpytools.xtool.sql import to_pg_array

        result = to_pg_array((4, 5, 6))
        assert result == "{4,5,6}"

    def test_to_pg_array_empty(self):
        from xpytools.xtool.sql import to_pg_array

        result = to_pg_array([])
        assert result == "{}"

    def test_to_pg_array_none(self):
        from xpytools.xtool.sql import to_pg_array

        result = to_pg_array(None)
        assert result is None

    def test_to_pg_array_scalar(self):
        from xpytools.xtool.sql import to_pg_array

        result = to_pg_array(42)
        assert result == 42

    def test_to_pg_array_string(self):
        from xpytools.xtool.sql import to_pg_array

        result = to_pg_array("hello")
        assert result == "hello"


class TestPrepareDataframe:
    """Tests for prepare_dataframe"""

    def test_prepare_dataframe_basic(self):
        from xpytools.xtool.sql import prepare_dataframe

        df = pd.DataFrame({
                "tags": [[1, 2], [3, 4]],
                "value": [10, 20]
                })
        result = prepare_dataframe(df)
        assert result["tags"].iloc[0] == "{1,2}"
        assert result["tags"].iloc[1] == "{3,4}"

    def test_prepare_dataframe_none_handling(self):
        from xpytools.xtool.sql import prepare_dataframe

        df = pd.DataFrame({
                "a": [1, None, 3],
                "b": [None, "test", np.nan]
                })
        result = prepare_dataframe(df)
        assert result["a"].iloc[1] is None
        assert result["b"].iloc[0] is None
        assert result["b"].iloc[2] is None

    def test_prepare_dataframe_empty_lists(self):
        from xpytools.xtool.sql import prepare_dataframe

        df = pd.DataFrame({
                "items": [[], [1, 2], None]
                })
        result = prepare_dataframe(df)
        assert result["items"].iloc[0] == "{}"
        assert result["items"].iloc[1] == "{1,2}"
        assert result["items"].iloc[2] is None

    def test_prepare_dataframe_not_inplace(self):
        from xpytools.xtool.sql import prepare_dataframe

        df = pd.DataFrame({"tags": [[1, 2]]})
        original_value = df["tags"].iloc[0]
        result = prepare_dataframe(df)
        # Original should be unchanged
        assert df["tags"].iloc[0] == original_value
        assert result["tags"].iloc[0] == "{1,2}"

    def test_prepare_dataframe_invalid_input(self):
        from xpytools.xtool.sql import prepare_dataframe

        result = prepare_dataframe("not a df")
        assert result is None

    def test_prepare_dataframe_nested_objects(self):
        from xpytools.xtool.sql import prepare_dataframe
        from dataclasses import dataclass

        @dataclass
        class Item:
            name: str
            value: int

        df = pd.DataFrame({
                "items": [Item("a", 1), Item("b", 2)]
                })
        result = prepare_dataframe(df)
        # Should convert to primitives
        assert isinstance(result["items"].iloc[0], dict)
        assert result["items"].iloc[0]["name"] == "a"
