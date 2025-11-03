from __future__ import annotations, annotations

from typing import Any


# noinspection PyUnresolvedReferences
def is_none(value: Any) -> bool:
    """
    Return True if `value` represents a null or missing value.

    This includes:
      - `None`
      - `float('nan')`
      - `numpy.nan` (if NumPy is installed)
      - `pandas.NA` / `pandas.NaT` / `pandas.NAN` (if pandas is installed)
      - string representations: 'nan', 'none', 'null', 'na', 'n/a', etc.

    Safe even if pandas or numpy are not available.

    Examples
    --------
    >>> is_none(None)
    True
    >>> is_none(float('nan'))
    True
    >>> is_none("NaN")
    True
    >>> is_none(pd.NA)
    True
    >>> is_none(0)
    False
    >>> is_none("")
    False
    """
    # Standard None
    if value is None:
        return True

    # Fast path: Python NaN
    try:
        # float('nan') != float('nan')
        if isinstance(value, float) and value != value:
            return True
    except Exception:
        pass

    # NumPy checks (if available)
    try:
        import numpy as np
        if isinstance(value, np.generic):
            # np.isnan() for all numeric types
            try:
                if np.isnan(value):
                    return True
            except Exception:
                pass
        # explicitly compare to np.nan singleton
        if value is np.nan:
            return True
    except ImportError:
        pass

    # Pandas checks (if available)
    try:
        import pandas as pd
        # covers pd.NA, pd.NaT, pd.NAN, and pd.isna()
        if getattr(pd, "isna", None) and pd.isna(value):
            return True
    except ImportError:
        pass
    except Exception:
        # sometimes pd.isna can raise on weird types
        pass

    # String null-like values (case-insensitive)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"none", "null", "nan", "na", "n/a", "nil", ""}:
            return True

    return False
