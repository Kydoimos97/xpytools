"""
Smoke tests for xpytools.xtype.common type aliases.

These don't increase coverage % (type aliases aren't executable),
but they verify the module structure and catch import errors.
"""
import pytest


class TestTypeAliasesImport:
    """Verify all type aliases import without errors"""

    def test_all_imports(self):
        """Import all exported type aliases"""
        from xpytools.xtype.common import (
            T, K, V,
            PathLike, OptPath, OptStr,
            DictStrAny, DictAny, DictStrStr, DictStrT,
            ListStr, ListAny, TupleStr, IterableStr, SequenceStr,
            Func, OptFunc,
            Number, OptNumber, NumericIterable,
            JSONPrimitive, JSONArray, JSONObject, JSONValue,
        )

        # Just verify they exist
        assert T is not None
        assert PathLike is not None
        assert DictStrAny is not None

    def test_pathlike_accepts_str_and_path(self):
        """PathLike should work with isinstance checks"""
        from pathlib import Path
        from xpytools.xtype.common import PathLike
        from typing import get_args

        # PathLike = Union[str, Path]
        args = get_args(PathLike)
        assert str in args
        assert Path in args

    def test_generic_type_vars(self):
        """Generic TypeVars should be reusable"""
        from typing import Dict
        from xpytools.xtype.common import T, K, V

        # Should be able to use in annotations
        def example(data: Dict[K, V]) -> V:
            pass

        # TypeVars should have no constraints
        assert T.__constraints__ == ()
        assert K.__constraints__ == ()
        assert V.__constraints__ == ()

    def test_json_type_structure(self):
        """JSONValue should be properly recursive"""
        from xpytools.xtype.common import JSONValue, JSONPrimitive, JSONArray, JSONObject
        from typing import get_args

        # JSONValue = Union[JSONPrimitive, JSONArray, JSONObject]
        args = get_args(JSONValue)
        assert len(args) == 7

    def test_usage_in_function_signature(self):
        """Type aliases should work in real function signatures"""
        from xpytools.xtype.common import DictStrAny, PathLike, OptStr

        def save_config(data: DictStrAny, path: PathLike, encoding: OptStr = None) -> bool:
            """Example function using type aliases"""
            return True

        # Function should be callable
        result = save_config({"key": "value"}, "/tmp/test.json")
        assert result is True


class TestNumberTypeAlias:
    """Number = Union[int, float] should work for numeric checks"""

    def test_number_type_annotation(self):
        from xpytools.xtype.common import Number
        from typing import get_args

        # Number = Union[int, float]
        args = get_args(Number)
        assert int in args
        assert float in args
        assert len(args) == 2