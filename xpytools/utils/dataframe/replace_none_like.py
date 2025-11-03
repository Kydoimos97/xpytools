from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from ...types.cast import as_none
from ...types.check import is_df, is_empty

if TYPE_CHECKING:
    from pandas import DataFrame as pdDataFrame
from ...decorators import requireModules


@requireModules(["pandas"], exc_raise=True)
def replace_none_like(df: "pdDataFrame") -> Optional["pdDataFrame"]:
    """
    Replace all None-like representations (NaN, '', 'null', etc.)
    in a DataFrame with proper Python None using `as_none()`.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame.

    Returns
    -------
    DataFrame | None
        Cleaned DataFrame or None if not a valid DataFrame.
    """
    if not is_df(df) or is_empty(df):
        raise ValueError("Invalid DataFrame")

    def _normalize_value(v: Any) -> Any:
        return as_none(v)

    return df.applymap(_normalize_value)
