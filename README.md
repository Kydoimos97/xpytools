<h1 align="center">xPyTools</h1>

<p align="center">
  <a href="https://github.com/Kydoimos97/xpytools/actions/workflows/run-tests.yml">
    <img src="https://github.com/Kydoimos97/xpytools/actions/workflows/run-tests.yml/badge.svg" alt="Tests">
  </a>
  <a href="https://codecov.io/gh/Kydoimos97/xpytools">
    <img src="https://codecov.io/gh/Kydoimos97/xpytools/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.11%2B-blue.svg" alt="Python 3.11+">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT">
  </a>
</p>

<p align="center"><b>
Python utilities for safe type handling, data manipulation, and runtime validation.
</b></p>

<p align="center">
A collection of defensive programming tools that handle messy real-world data:
inconsistent nulls, malformed inputs, timezone chaos, and format conversions.<br>
Built for data pipelines, ETL workflows, and APIs where you can't trust your inputs.
</p>

---

<p align="center">
  📘 <a href="https://xpytools.readthedocs.io/en/latest"><b>Read the Docs</b></a>
</p>



## Installation

```bash
pip install xpytools

# Optional: with dependencies
pip install xpytools[all]
```

**Requirements**: Python 3.11+

---

## Import Patterns

xpytools provides multiple import patterns. Choose based on your preference:

### Recommended Imports

**Note: Be cautious with alias overwrites of different packages. 
The preferred import method is `from xpytools import xtool` as this ensures uniqueness.
Additionally this enforces prepending the targeted data type: `xtool.txt.clean()` vs `clean()` which is ambiguous.


```python
# Type system shortcuts (most concise)
from xpytools import xcast, xcheck
from xpytools.xtype import strChoice, intChoice, floatChoice, anyChoice

result = xcast.as_int("42")
valid = xcheck.is_none(value)
Status = strChoice("active", "inactive")
Code = intChoice(200, 404, 500)
```

```python
# Utilities via xtool (preferred for df/img/txt/sql)
from xpytools import xtool

xtool.df.normalize_column_names(df)
xtool.img.load("image.png")
xtool.txt.clean(text)
```

```python
# Decorators
from xpytools import xdeco

@xdeco.requireModules(["pandas"])
@xdeco.asSingleton
class DataProcessor:
    pass
```

### Alternative Imports

```python
# Full module imports
from xpytools import xtype

xtype.xcast.as_int("42")
xtype.xcheck.is_none(value)
```

```python
# Direct submodule imports
from xpytools.xtool import df, txt, img
from xpytools.xtype import xcast, xcheck
```

```python
# Deep imports (for specific functions)
from xpytools.xtype.xcheck import is_none, is_int
from xpytools.xtype.choice import strChoice, intChoice
```

### Import Gotchas

❌ **Don't do this** - Mixing import levels can be confusing:
```python
from xpytools.xtool import xtool  # Redundant - xtool importing itself
```

✅ **Do this instead**:
```python
from xpytools import xtool  # Works - clean import
xtool.df.normalize_column_names(df)

# Or for type system:
from xpytools import xcast, xcheck
from xpytools.xtype import strChoice

result = xcast.as_int("42")
valid = xcheck.is_none(value)
Color = strChoice("red", "green", "blue")
```

---

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

#### `xpytools.xtype` - Extended Types
Specialized types and containers.

- `UUIDLike` - Pydantic-compatible UUID validator (accepts str or UUID objects)
- `TTLSet` - Thread-safe set with automatic expiration (useful for deduplication, rate limiting)

---

### Utility Modules (`xpytools.xtool`)

#### `xtool.df` - DataFrame Helpers
Pandas utilities for cleaning and transforming data.

- `normalize_column_names()` - Convert to lowercase snake_case, handle duplicates
- `lookup()` - Safe value retrieval (no KeyError or IndexError)
- `merge_fill()` - Merge DataFrames and fill missing values intelligently
- `replace_none_like()` - Normalize all null representations to Python `None`

#### `xtool.img` - Image I/O
Unified interface for loading images from any source.

- `load()` - Load from file path, URL, bytes, or base64
- Format converters: `to_bytes()`, `to_base64()`, `from_bytes()`, `from_base64()`
- Transformations: `create_thumbnail()`, `resize()`

#### `xtool.txt` - Text Processing
String manipulation and cleaning utilities.

- `clean()` - Normalize text (with optional `cleantext` integration)
- `strip_html()` - Remove HTML tags and entities
- `strip_ascii()` - Remove non-ASCII characters
- `truncate()` - Safely truncate with ellipsis
- `pad()` - Fixed-width padding (left/right/center)
- `split_lines()` - Wrap text to fixed width

#### `xtool.sql` - SQL/DataFrame Bridge
Prepare data for database insertion.

- `prepare_dataframe()` - Clean DataFrames for SQL (convert lists to PostgreSQL arrays, normalize nulls)
- `to_pg_array()` - Convert Python lists to PostgreSQL array literals

#### `xtool.xpyt_pydantic` - Pydantic Extensions
Enhanced Pydantic model features.

- `TypeSafeAccessMixin` - Auto-serialize UUIDs, Enums, datetimes, nested models in Pydantic

---

### Decorators (`xpytools.xdeco`)

#### `@requireModules(["pandas", "numpy"])`
Gracefully skip function execution when optional dependencies are missing. Returns `None` or raises `ImportError` depending on configuration.

#### `@asSingleton`
Enforce singleton pattern on class definitions. Prevents multiple instances.

---

## Design Philosophy

**1. Safe by default** - Functions return `None` instead of crashing  
**2. No surprises** - `is_none()` handles 20+ null representations uniformly  
**3. Minimal dependencies** - Core modules work standalone; pandas/PIL/Pydantic are optional  
**4. SOLID principles** - Small, focused functions; easy to test and compose  
**5. Type-safe** - Strong typing throughout; plays well with mypy/pyright

---

## Common Use Cases

- **ETL Pipelines**: Normalize inconsistent data sources before loading
- **APIs**: Validate and coerce user inputs safely
- **Data Science**: Clean pandas DataFrames with repeatable transformations
- **Configuration**: Parse environment variables, JSON configs, user settings
- **Image Processing**: Unified I/O regardless of source (file, URL, base64, bytes)

---

## Usage Examples

### Type System
```python
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
StatusCode = intChoice(200, 404, 500)

color = Color("red")                # "red"
# Color("yellow")                   # ValueError
```

### Utilities
```python
from xpytools import xtool

# DataFrame operations
xtool.df.normalize_column_names(df)
safe_value = xtool.df.lookup(df, "column", "key")

# Text processing
clean_text = xtool.txt.clean("messy   text\n\n")
truncated = xtool.txt.truncate("long text", 10)

# Image handling
img = xtool.img.load("path/to/image.png")
img_bytes = xtool.img.to_bytes(img, format="PNG")
```

### Decorators
```python
from xpytools import xdeco

@xdeco.requireModules(["pandas", "numpy"])
def process_data():
    import pandas as pd
    import numpy as np
    return pd.DataFrame(np.random.randn(100, 4))

@xdeco.asSingleton
class DatabaseConnection:
    def __init__(self):
        self.conn = "connection"
```

---

## Project Structure

```
xpytools/
├── xtype/              # Type system (xcast, xcheck, choice)
│   ├── xcast/          # Safe conversions (as_*)
│   ├── xcheck/         # Validators (is_*)
│   └── choice/         # Runtime-validated pseudo-Literals
├── xtool/              # Utilities 
│   ├── df/             # DataFrame helpers
│   ├── img/            # Image I/O
│   ├── txt/            # Text processing
│   ├── sql/            # SQL/DataFrame bridge
│   └── xpyt_pydantic/       # Pydantic extensions
└── xdeco/              # Decorators (@requireModules, @asSingleton)
```

---

## Testing

```bash
# Run full test suite
pytest tests/ -v

# With coverage
pytest tests/ --cov=xpytools --cov-report=term-missing
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

**Author**: Willem van der Schans  
**Copyright**: © 2025