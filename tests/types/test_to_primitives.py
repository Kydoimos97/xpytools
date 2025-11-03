"""Comprehensive tests for xpytools.xtype.cast.to_primitives"""
import pytest
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone


class TestToPrimitivesComprehensive:
    """Exhaustive tests for to_primitives"""

    def test_none(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        assert to_primitives(None) is None

    def test_primitives_passthrough(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        assert to_primitives(42) == 42
        assert to_primitives(3.14) == 3.14
        assert to_primitives("hello") == "hello"
        assert to_primitives(True) is True
        assert to_primitives(False) is False

    def test_dict(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = {"a": 1, "b": 2}
        result = to_primitives(data)
        assert result == {"a": 1, "b": 2}

    def test_nested_dict(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = {"a": {"b": {"c": 3}}}
        result = to_primitives(data)
        assert result == {"a": {"b": {"c": 3}}}

    def test_list(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = [1, 2, 3]
        result = to_primitives(data)
        assert result == [1, 2, 3]

    def test_nested_list(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = [[1, 2], [3, 4]]
        result = to_primitives(data)
        assert result == [[1, 2], [3, 4]]

    def test_tuple(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = (1, 2, 3)
        result = to_primitives(data)
        assert result == [1, 2, 3]  # Converts to list

    def test_set(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = {1, 2, 3}
        result = to_primitives(data)
        assert isinstance(result, list)
        assert set(result) == {1, 2, 3}

    def test_enum(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Status(Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        result = to_primitives(Status.ACTIVE)
        assert result == "active"

    def test_enum_in_dict(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Status(Enum):
            ACTIVE = "active"

        data = {"status": Status.ACTIVE}
        result = to_primitives(data)
        assert result == {"status": "active"}

    def test_enum_in_list(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Status(Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        data = [Status.ACTIVE, Status.INACTIVE]
        result = to_primitives(data)
        assert result == ["active", "inactive"]

    def test_dataclass(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        @dataclass
        class Person:
            name: str
            age: int

        person = Person(name="Alice", age=30)
        result = to_primitives(person)
        assert result == {"name": "Alice", "age": 30}

    def test_nested_dataclass(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        @dataclass
        class Address:
            city: str

        @dataclass
        class Person:
            name: str
            address: Address

        person = Person(name="Bob", address=Address(city="NYC"))
        result = to_primitives(person)
        assert result == {"name": "Bob", "address": {"city": "NYC"}}

    def test_dataclass_with_enum(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Status(Enum):
            ACTIVE = "active"

        @dataclass
        class Record:
            id: int
            status: Status

        record = Record(id=1, status=Status.ACTIVE)
        result = to_primitives(record)
        assert result == {"id": 1, "status": "active"}

    def test_float_nan(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        result = to_primitives(float('nan'))
        assert result is None

    def test_dict_with_nan_value(self):
        from xpytools.xtype.cast.to_primitives import to_primitives
        data = {"a": 1, "b": float('nan')}
        result = to_primitives(data)
        assert result == {"a": 1, "b": None}

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_scalar(self):
        import numpy as np
        from xpytools.xtype.cast.to_primitives import to_primitives

        assert to_primitives(np.int64(42)) == 42
        assert to_primitives(np.float64(3.14)) == 3.14
        assert to_primitives(np.bool_(True)) is True

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_array(self):
        import numpy as np
        from xpytools.xtype.cast.to_primitives import to_primitives

        arr = np.array([1, 2, 3])
        result = to_primitives(arr)
        assert result == [1, 2, 3]

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_nan(self):
        import numpy as np
        from xpytools.xtype.cast.to_primitives import to_primitives

        result = to_primitives(np.nan)
        assert result is None

    @pytest.mark.skipif(
        not pytest.importorskip("numpy", reason="numpy not installed"),
        reason="numpy not available"
    )
    def test_numpy_array_with_nan(self):
        import numpy as np
        from xpytools.xtype.cast.to_primitives import to_primitives

        arr = np.array([1.0, np.nan, 3.0])
        result = to_primitives(arr)
        assert result == [1.0, None, 3.0]

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_dataframe(self):
        import pandas as pd
        from xpytools.xtype.cast.to_primitives import to_primitives

        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = to_primitives(df)
        assert result == [{"a": 1, "b": 3}, {"a": 2, "b": 4}]

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_series(self):
        import pandas as pd
        from xpytools.xtype.cast.to_primitives import to_primitives

        series = pd.Series([1, 2, 3])
        result = to_primitives(series)
        assert result == [1, 2, 3]

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_na(self):
        import pandas as pd
        from xpytools.xtype.cast.to_primitives import to_primitives

        result = to_primitives(pd.NA)
        assert result is None

    @pytest.mark.skipif(
        not pytest.importorskip("pandas", reason="pandas not installed"),
        reason="pandas not available"
    )
    def test_pandas_nat(self):
        import pandas as pd
        from xpytools.xtype.cast.to_primitives import to_primitives

        result = to_primitives(pd.NaT)
        assert result is None

    @pytest.mark.skipif(
        not pytest.importorskip("pydantic", reason="pydantic not installed"),
        reason="pydantic not available"
    )
    def test_pydantic_v2_model(self):
        from pydantic import BaseModel
        from xpytools.xtype.cast.to_primitives import to_primitives

        class User(BaseModel):
            name: str
            age: int

        user = User(name="Charlie", age=25)
        result = to_primitives(user)
        assert result == {"name": "Charlie", "age": 25}

    @pytest.mark.skipif(
        not pytest.importorskip("pydantic", reason="pydantic not installed"),
        reason="pydantic not available"
    )
    def test_nested_pydantic_models(self):
        from pydantic import BaseModel
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Address(BaseModel):
            city: str

        class User(BaseModel):
            name: str
            address: Address

        user = User(name="Dave", address=Address(city="LA"))
        result = to_primitives(user)
        assert result == {"name": "Dave", "address": {"city": "LA"}}

    def test_complex_nested_structure(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class Status(Enum):
            ACTIVE = "active"

        @dataclass
        class Item:
            id: int
            status: Status

        data = {
            "items": [Item(id=1, status=Status.ACTIVE), Item(id=2, status=Status.ACTIVE)],
            "meta": {"count": 2, "nans": [float('nan'), None]},
            "tuples": (1, 2, 3)
        }

        result = to_primitives(data)
        expected = {
            "items": [
                {"id": 1, "status": "active"},
                {"id": 2, "status": "active"}
            ],
            "meta": {"count": 2, "nans": [None, None]},
            "tuples": [1, 2, 3]
        }
        assert result == expected

    def test_unserializable_object_fallback(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class CustomClass:
            def __str__(self):
                return "custom"

        obj = CustomClass()
        result = to_primitives(obj)
        # Should fall back to str()
        assert result == "custom"

    def test_unserializable_object_str_failure(self):
        from xpytools.xtype.cast.to_primitives import to_primitives

        class BadClass:
            def __str__(self):
                raise RuntimeError("Cannot convert")

        obj = BadClass()
        result = to_primitives(obj)
        # Should return None on failure
        assert result is None