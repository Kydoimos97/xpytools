#  Copyright (c) 2025.
#  Author: Willem van der Schans.
#  Licensed under the MIT License (https://opensource.org/license/mit).

"""
Smoke tests for all top-level imports of xpytools.

Validates that each expected submodule imports correctly and
exposes the intended symbols (no import errors or missing attrs).
"""

from __future__ import annotations

import importlib


def test_top_level_imports():
    """Ensure xpytools and its top-level namespaces import without errors."""
    mod = importlib.import_module("xpytools")

    # Basic sanity checks
    assert hasattr(mod, "xtool")
    assert hasattr(mod, "check")
    assert hasattr(mod, "cast")
    assert hasattr(mod, "literal")
    assert hasattr(mod, "xtype")
    assert hasattr(mod, "decorators")

    # Verify submodules load properly
    importlib.import_module("xpytools.xtool")
    importlib.import_module("xpytools.xtool")

    # Internal integrity
    xpyt = mod.xpyt
    assert hasattr(xpyt, "txt")
    assert hasattr(xpyt, "df")
    assert hasattr(xpyt, "img")
    assert hasattr(xpyt, "sql")
    assert hasattr(xpyt, "xpyt_pydantic")

    # Sanity checks for expected callable objects
    assert callable(xpyt.txt.pad)
    assert callable(xpyt.txt.truncate)
    assert callable(xpyt.df.lookup)
    assert callable(xpyt.img.load)


def test_internal_utils_structure():
    """Ensure xtool mirrors the same public layout as xtool."""
    utils = importlib.import_module("xpytools.xtool")

    for sub in ("txt", "df", "img", "sql", "xpyt_pydantic"):
        assert hasattr(utils, sub), f"Missing {sub} in xpytools.xtool"

    # Consistency between xtool and xtool
    xpyt = importlib.import_module("xpytools.xtool")
    for sub in ("txt", "df", "img", "sql", "xpyt_pydantic"):
        assert getattr(xpyt, sub) is getattr(utils, sub)
