#  Copyright (c) 2025.
#  Author: Willem van der Schans.
#  Licensed under the MIT License (https://opensource.org/license/mit).

"""
xpytools.decorators
-------------------
Lightweight decorators for runtime safety and object management.

Provides:
    • requireModules(module_names) → raises or skips when dependencies are missing
    • asSingleton(cls)             → enforce singleton behavior on class definition
"""

from __future__ import annotations

from .requireModules import requireModules
from .asSingleton import asSingleton

__all__ = [
    "requireModules",
    "asSingleton",
]
