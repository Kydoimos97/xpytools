from __future__ import annotations

from typing import Any, Union

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame as pdDataFrame


def is_empty(obj: Union[Any, "pdDataFrame"]) -> bool:
    """
    Safely check if an object "has values" (non-empty).
    Works for DataFrames, Series, lists, dicts, sets, and strings.
    """
    if obj is None:
        return False
    try:
        if hasattr(obj, "empty"):
            return not getattr(obj, "empty")
        if hasattr(obj, "__len__"):
            return len(obj) > 0
        return bool(obj)
    except Exception:
        return False
