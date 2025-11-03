#  Copyright (c) 2025.
#  Author: Willem van der Schans.
#  Licensed under the MIT License (https://opensource.org/license/mit).

"""
xpytools.types
---------------------
Runtime-safe extended types and validators.

Includes:
- `TTLSet` → Thread-safe expiring set for in-memory tracking.
- `UUIDLike` → Pydantic-compatible UUID string validator.
- `literal` → Runtime-constrained pseudo-Literal types.
"""

from . import check, cast
from .TTLSet import TTLSet
from .UUIDLike import UUIDLike
from . import literal


__all__ = [
    "TTLSet",
    "UUIDLike",
    "literal",
    "check",
    "cast"
]
