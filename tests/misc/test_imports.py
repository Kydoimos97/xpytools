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
    assert hasattr(mod, "xcheck")
    assert hasattr(mod, "xcast")
    assert hasattr(mod.xtype, "choice")
    assert hasattr(mod, "xtype")
    assert hasattr(mod, "xdeco")

    # Verify submodules load properly
    importlib.import_module("xpytools.xtool")
    importlib.import_module("xpytools.xtool")

    # Internal integrity
    xtool = mod.xtool
    assert hasattr(xtool, "txt")
    assert hasattr(xtool, "df")
    assert hasattr(xtool, "img")
    assert hasattr(xtool, "sql")
    assert hasattr(xtool, "xpyt_pydantic")

    # Sanity checks for expected callable objects
    assert callable(xtool.txt.pad)
    assert callable(xtool.txt.truncate)
    assert callable(xtool.df.lookup)
    assert callable(xtool.img.load)


def test_internal_utils_structure():
    """Ensure xtool mirrors the same public layout as xtool."""
    utils = importlib.import_module("xpytools.xtool")

    for sub in ("txt", "df", "img", "sql", "xpyt_pydantic"):
        assert hasattr(utils, sub), f"Missing {sub} in xpytools.xtool"

    # Consistency between xtool and xtool
    xtool = importlib.import_module("xpytools.xtool")
    for sub in ("txt", "df", "img", "sql", "xpyt_pydantic"):
        assert getattr(xtool, sub) is getattr(utils, sub)
