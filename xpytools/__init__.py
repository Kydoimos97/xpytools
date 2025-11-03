#  Copyright (c) 2025.
#  Author: Willem van der Schans.
#  Licensed under the MIT License (https://opensource.org/license/mit).

"""
xpytools
--------
General-purpose Python utilities by Willem van der Schans.

Submodules
----------
- xpytools.Checks → runtime-safe validators (`is_*`, `safe_*`)
- xpytools.Cast   → type conversion helpers (`as_*`)
- xpytools.types  → extended and Pydantic-compatible type factories
"""

import sys

from . import types, decorators
from . import utils as xpyt

# Bring Typing submodules up one level
check = types.check
cast = types.cast
# Register them as top-level accessible modules
sys.modules[__name__ + ".check"] = check
sys.modules[__name__ + ".cast"] = cast

__all__ = ["check", "cast", "types", 'decorators', 'xpyt']
