# xpytools

**Python utilities for safe type handling, data manipulation, and runtime validation.**

A collection of defensive programming tools that handle messy real-world data: inconsistent nulls, malformed inputs, timezone chaos, and format conversions. Built for data pipelines, ETL workflows, and APIs where you can't trust your inputs.

## Quick Start

```python
# Type system shortcuts
from xpytools import xcast, xcheck
from xpytools.xtype import strChoice, intChoice

# Safe conversions
result = xcast.as_int("42")         # 42
bad_result = xcast.as_int("abc")    # None

# Runtime validation  
valid = xcheck.is_none(value)       # True/False
is_number = xcheck.is_int("123")    # True

# Constrained types
Color = strChoice("red", "green", "blue")
color = Color("red")                # "red"
```

## What's Included

### Core Modules

#### `xpytools.xcast` - Safe Type Conversions
Convert between types without crashing. Returns `None` on failure instead of raising exceptions.

- **Primitives**: `as_int()`, `as_float()`, `as_bool()`, `as_str()`, `as_bytes()`
- **JSON**: `as_json()`, `as_json_str()`, `as_dict()`, `as_list()`
- **Datetime**: `as_datetime()`, `as_datetime_str()` (handles ISO 8601, timestamps, timezones)
- **DataFrames**: `as_df()` (coerce various inputs to pandas DataFrame)
- **Null normalization**: `as_none()` (handles `None`, `NaN`, `"null"`, `""`, etc.)
- **Primitives export**: `to_primitives()` (recursively convert dataclasses, Enums, Pydantic models, NumPy, pandas to JSON-safe types)

#### `xpytools.xcheck` - Runtime Type Validation
Boolean validators for defensive programming. All `is_*` functions return `True`/`False`.

- **Primitives**: `is_int()`, `is_float()`, `is_bool()`, `is_str()`, `is_bytes()`
- **Collections**: `is_dict()`, `is_list_like()`, `is_numeric()`, `is_empty()`
- **JSON**: `is_json()`, `is_json_like()`
- **Datetime**: `is_datetime()`, `is_datetime_like()`
- **Null detection**: `is_none()` (detects `None`, `NaN`, `pd.NA`, `"null"`, `""`, and 20+ variants)
- **Special**: `is_uuid()`, `is_uuid_like()`, `is_base64()`, `is_df()`

#### `xpytools.choice` - Runtime-Validated Enums
Create constrained types without full Enum classes. Integrates with Pydantic v2.

- `strChoice("red", "green", "blue")` - constrained strings
- `intChoice(200, 404, 500)` - constrained integers
- `floatChoice(0.1, 0.01)` - constrained floats
- `anyChoice("foo", 1, None)` - mixed-type literals

### Utility Modules (`xpytools.xtool`)

#### `xtool.df` - DataFrame Helpers
Pandas utilities for cleaning and transforming data.

#### `xtool.img` - Image I/O
Unified interface for loading images from any source.

#### `xtool.txt` - Text Processing
String manipulation and cleaning utilities.

#### `xtool.sql` - SQL/DataFrame Bridge
Prepare data for database insertion.

#### `xtool.xpyt_pydantic` - Pydantic Extensions
Enhanced Pydantic model features.

### Decorators (`xpytools.xdeco`)

#### `@requireModules(["pandas", "numpy"])`
Gracefully skip function execution when optional dependencies are missing.

#### `@asSingleton`
Enforce singleton pattern on class definitions.

## Design Philosophy

**1. Safe by default** - Functions return `None` instead of crashing  
**2. No surprises** - `is_none()` handles 20+ null representations uniformly  
**3. Minimal dependencies** - Core modules work standalone; pandas/PIL/Pydantic are optional  
**4. SOLID principles** - Small, focused functions; easy to test and compose  
**5. Type-safe** - Strong typing throughout; plays well with mypy/pyright

## Common Use Cases

- **ETL Pipelines**: Normalize inconsistent data sources before loading
- **APIs**: Validate and coerce user inputs safely
- **Data Science**: Clean pandas DataFrames with repeatable transformations
- **Configuration**: Parse environment variables, JSON configs, user settings
- **Image Processing**: Unified I/O regardless of source (file, URL, base64, bytes)

## Requirements

Python 3.11+

## License

MIT License

**Author**: Kydoimos97  
**Copyright**: © 2025