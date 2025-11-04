# API Reference

Welcome to the xpytools API documentation. This section provides comprehensive documentation for all modules and functions.

## Module Overview

### Core Type System (`xtype`)
- **[xcast](xtype.md#xcast)** - Safe type conversions that return `None` on failure
- **[xcheck](xtype.md#xcheck)** - Runtime type validation with boolean returns
- **[choice](xtype.md#choice)** - Runtime-validated constrained types
- **[Extended Types](xtype.md#extended-types)** - TTLSet, UUIDLike, and other specialized types

### Utilities (`xtool`)
- **[DataFrame Operations](xtool.md#dataframe-operations)** - pandas utilities for data cleaning
- **[Image Processing](xtool.md#image-processing)** - Unified image I/O and transformations
- **[Text Processing](xtool.md#text-processing)** - String manipulation and cleaning
- **[SQL Bridge](xtool.md#sql-bridge)** - Database integration helpers
- **[Pydantic Extensions](xtool.md#pydantic-extensions)** - Enhanced Pydantic features

### Decorators (`xdeco`)
- **[Function Enhancers](xdeco.md)** - `@requireModules`, `@asSingleton`

## Quick Start Examples

### Safe Type Conversion
```python
from xpytools import xcast

result = xcast.as_int("42")       # 42
invalid = xcast.as_int("abc")     # None (doesn't crash)
```

### Runtime Validation
```python
from xpytools import xcheck

xcheck.is_int(42)          # True
xcheck.is_none("null")     # True (handles many null variants)
```

### Constrained Types
```python
from xpytools.xtype import strChoice

Status = strChoice("active", "inactive", "pending")
status = Status("active")  # "active"
```

### Utilities
```python
from xpytools import xtool

# DataFrame operations
xtool.df.normalize_column_names(df)

# Image loading from any source
img = xtool.img.load("path/or/url/or/base64")

# Text cleaning
clean = xtool.txt.clean("messy  text\n\n")
```

## Design Principles

**Safe by Default**: Functions prefer returning `None` over raising exceptions
**Null-Aware**: Consistent handling of 20+ null representations (`None`, `"null"`, `""`, etc.)
**Type-Safe**: Strong typing throughout with mypy/pyright compatibility
**Minimal Dependencies**: Core functionality works standalone; optional features require opt-in packages
