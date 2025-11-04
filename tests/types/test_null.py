"""Comprehensive tests for xpytools.xtype.xcheck.null"""
import pytest


class TestIsNoneComprehensive:
    """Exhaustive tests for is_none"""

    def test_python_none(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none(None) is True

    def test_float_nan(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none(float('nan')) is True

    def test_string_variants_exact(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["None", "none", "NONE"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_null_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["null", "NULL", "Null"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_nan_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["nan", "NaN", "NAN", "nann", "NANN"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_na_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["na", "NA", "n/a", "N/A", "n.a", "N.A", "n a", "N A", "n-a", "N-A", "n.a.", "N.A."]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_nil_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["nil", "NIL", "Nil"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_missing_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["missing", "MISSING", "Missing"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_void_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["void", "VOID", "Void"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_string_not_applicable_variants(self):
        from xpytools.xtype.xcheck import is_none
        for val in ["notapplicable", "NOTAPPLICABLE", "NotApplicable"]:
            assert is_none(val) is True, f"Failed for {val!r}"

    def test_empty_string(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none("") is True

    def test_whitespace_only(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none("   ") is True
        assert is_none("\t") is True
        assert is_none("\n") is True
        assert is_none("  \t\n  ") is True

    def test_non_null_strings(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none("hello") is False
        assert is_none("0") is False
        assert is_none("false") is False

    def test_non_null_numbers(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none(0) is False
        assert is_none(0.0) is False
        assert is_none(1) is False
        assert is_none(-1) is False

    def test_non_null_booleans(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none(False) is False
        assert is_none(True) is False

    def test_non_null_collections(self):
        from xpytools.xtype.xcheck import is_none
        assert is_none([]) is False
        assert is_none({}) is False
        assert is_none(set()) is False
        assert is_none(()) is False

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_nan(self):
        import numpy as np
        from xpytools.xtype.xcheck import is_none
        assert is_none(np.nan) is True

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_float_nan(self):
        import numpy as np
        from xpytools.xtype.xcheck import is_none
        assert is_none(np.float64('nan')) is True
        assert is_none(np.float32('nan')) is True

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_valid_numbers(self):
        import numpy as np
        from xpytools.xtype.xcheck import is_none
        assert is_none(np.int64(0)) is False
        assert is_none(np.float64(0.0)) is False
        assert is_none(np.float64(1.5)) is False

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_na(self):
        import pandas as pd
        from xpytools.xtype.xcheck import is_none
        assert is_none(pd.NA) is True

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_nat(self):
        import pandas as pd
        from xpytools.xtype.xcheck import is_none
        assert is_none(pd.NaT) is True

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_valid_values(self):
        import pandas as pd
        from xpytools.xtype.xcheck import is_none
        assert is_none(pd.Timestamp("2024-01-01")) is False

    def test_self_not_equal(self):
        from xpytools.xtype.xcheck import is_none
        # Test NaN-like behavior where value != value
        # This is already covered by float('nan'), but test edge cases

        class WeirdObject:
            def __ne__(self, other):
                return True  # Always not equal to itself
            def __eq__(self, other):
                return False

        obj = WeirdObject()
        # This might be detected as None-like due to != behavior
        result = is_none(obj)
        # Result depends on implementation details, just verify no crash
        assert isinstance(result, bool)

    def test_exception_during_comparison(self):
        from xpytools.xtype.xcheck import is_none

        class BadComparison:
            def __eq__(self, other):
                raise RuntimeError("Cannot compare")
            def __ne__(self, other):
                raise RuntimeError("Cannot compare")

        obj = BadComparison()
        # Should handle exception gracefully
        result = is_none(obj)
        assert isinstance(result, bool)