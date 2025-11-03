import pytest

pandas = pytest.importorskip("pandas", reason="pandas required for df tests")
import pandas as pd
import numpy as np


class TestLookup:
    """Tests for lookup"""

    def test_lookup_simple(self):
        from xpytools.xtool.df import lookup

        df = pd.DataFrame({
                "user_id": [1, 2, 3],
                "email": ["a@test.com", "b@test.com", "c@test.com"]
                })
        result = lookup(df, "user_id", 2, "email")
        assert result == "b@test.com"

    def test_lookup_not_found(self):
        from xpytools.xtool.df import lookup

        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = lookup(df, "a", 99, "b")
        assert result is None

    def test_lookup_with_index(self):
        from xpytools.xtool.df import lookup

        df = pd.DataFrame({
                "category": ["A", "A", "B"],
                "value": [10, 20, 30]
                })
        result = lookup(df, "category", "A", "value", index=1)
        assert result == 20

    def test_lookup_safe_mode(self):
        from xpytools.xtool.df import lookup

        df = pd.DataFrame({"a": [1, 2]})
        # Column doesn't exist
        result = lookup(df, "missing_col", 1, "a", safe=True)
        assert result is None


class TestMergeFill:
    """Tests for merge_fill"""

    def test_merge_fill_simple(self):
        from xpytools.xtool.df import merge_fill

        left = pd.DataFrame({"id": [1, 2], "value": [None, 20]})
        right = pd.DataFrame({"id": [1, 2], "value": [10, 25]})
        result = merge_fill(left, right, on="id")
        assert result["value"].tolist() == [10, 20]

    def test_merge_fill_no_duplicates(self):
        from xpytools.xtool.df import merge_fill

        left = pd.DataFrame({"id": [1], "a": [None], "b": [2]})
        right = pd.DataFrame({"id": [1], "a": [10], "b": [3]})
        result = merge_fill(left, right, on="id")
        # Should not have _x or _y columns
        assert "_x" not in str(result.columns)
        assert "_y" not in str(result.columns)
        assert "_right" not in str(result.columns)

    def test_merge_fill_prefer_right(self):
        from xpytools.xtool.df import merge_fill

        left = pd.DataFrame({"id": [1], "val": [10]})
        right = pd.DataFrame({"id": [1], "val": [20]})
        result = merge_fill(left, right, on="id", prefer_right=True, fill_only_if_none=False)
        assert result["val"].iloc[0] == 20


class TestNormalizeColumnNames:
    """Tests for normalize_column_names"""

    def test_normalize_basic(self):
        from xpytools.xtool.df import normalize_column_names

        df = pd.DataFrame(columns=["User ID", "Email-Address", "Total Score"])
        result = normalize_column_names(df.copy())
        assert list(result.columns) == ["user_id", "email_address", "total_score"]

    def test_normalize_special_chars(self):
        from xpytools.xtool.df import normalize_column_names

        df = pd.DataFrame(columns=["(name)", "value$", "count%"])
        result = normalize_column_names(df.copy())
        assert "name" in result.columns
        assert "value" in result.columns
        assert "count" in result.columns

    def test_normalize_preserves_numeric_suffix(self):
        from xpytools.xtool.df import normalize_column_names

        df = pd.DataFrame(columns=["Score.1", "Score.2"])
        result = normalize_column_names(df.copy())
        assert "score_1" in result.columns
        assert "score_2" in result.columns

    def test_normalize_duplicate_handling(self):
        from xpytools.xtool.df import normalize_column_names

        df = pd.DataFrame(columns=["Name", "name", "NAME"])
        result = normalize_column_names(df.copy())
        cols = list(result.columns)
        assert len(cols) == 3
        assert len(set(cols)) == 3  # all unique

    def test_normalize_inplace(self):
        from xpytools.xtool.df import normalize_column_names

        df = pd.DataFrame(columns=["User Name"])
        normalize_column_names(df, inplace=True)
        assert list(df.columns) == ["user_name"]


class TestReplaceNoneLike:
    """Tests for replace_none_like"""

    def test_replace_none_like_basic(self):
        from xpytools.xtool.df import replace_none_like

        df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "null", "z"]})
        result = replace_none_like(df, force=True)
        assert result["a"].iloc[1] is None
        assert result["b"].iloc[1] is None

    def test_replace_none_like_nan(self):
        from xpytools.xtool.df import replace_none_like

        df = pd.DataFrame({"a": [1, np.nan, 3]})
        result = replace_none_like(df, force=True)
        assert result["a"].iloc[1] is None

    def test_replace_none_like_empty_df(self):
        from xpytools.xtool.df import replace_none_like

        df = pd.DataFrame()
        with pytest.raises(ValueError, match="Invalid DataFrame"):
            replace_none_like(df)
