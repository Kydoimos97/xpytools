# Utilities API

The `xtool` module provides utilities for data manipulation, image processing, text handling, and more.

## DataFrame Operations

Pandas utilities for cleaning and transforming data.

::: xpytools.xtool.df


### Examples

```python
from xpytools import xtool

# Normalize column names to snake_case
df = xtool.df.normalize_column_names(df)
# "First Name" -> "first_name"
# "User ID" -> "user_id"

# Safe value lookup (no KeyError/IndexError)
value = xtool.df.lookup(df, "column", "key", default="N/A")

# Merge with intelligent filling
result = xtool.df.merge_fill(left_df, right_df, on="id")

# Replace all null-like values with None
clean_df = xtool.df.replace_none_like(df)
# Converts: "", "null", "N/A", NaN, etc. -> None
```

## Image Processing

Unified interface for loading images from any source.

::: xpytools.xtool.img

::: xpytools.xtool.img.resize


### Examples

```python
from xpytools import xtool

# Load from various sources
img1 = xtool.img.load("path/to/image.png")
img2 = xtool.img.load("https://example.com/image.jpg")
img3 = xtool.img.load(base64_encoded_string)
img4 = xtool.img.load(bytes_data)

# Format conversions
png_bytes = xtool.img.to_bytes(img, format="PNG")
base64_str = xtool.img.to_base64(img, format="JPEG")
img_from_b64 = xtool.img.from_base64(base64_str)

# Transformations
thumbnail = xtool.img.create_thumbnail(img, size=(150, 150))
resized = xtool.img.resize(img, width=800, height=600)
```

## Text Processing

String manipulation and cleaning utilities.

::: xpytools.xtool.txt


### Examples

```python
from xpytools import xtool

# Text cleaning and normalization
clean = xtool.txt.clean("  messy   text\n\n\t")
# Result: "messy text"

# HTML stripping
plain = xtool.txt.strip_html("<p>Hello <b>world</b>!</p>")
# Result: "Hello world!"

# ASCII filtering
ascii_only = xtool.txt.strip_ascii("Hello 世界!")
# Result: "Hello !"

# Safe truncation
short = xtool.txt.truncate("very long text", 10)
# Result: "very lo..."

# Fixed-width padding
padded = xtool.txt.pad("text", 10, align="center")
# Result: "   text   "

# Text wrapping
lines = xtool.txt.split_lines("very long text that needs wrapping", width=10)
# Result: ["very long", "text that", "needs", "wrapping"]
```

## SQL Bridge

Prepare data for database insertion, especially PostgreSQL.

::: xpytools.xtool.sql


### Examples

```python
from xpytools import xtool

# Prepare DataFrame for SQL insertion
clean_df = xtool.sql.prepare_dataframe(df)
# - Converts lists to PostgreSQL arrays
# - Normalizes null values
# - Handles complex types

# Convert Python list to PostgreSQL array literal
pg_array = xtool.sql.to_pg_array([1, 2, 3])
# Result: "{1,2,3}"

pg_str_array = xtool.sql.to_pg_array(["a", "b", "c"])
# Result: '{"a","b","c"}'
```

## Pydantic Extensions

Enhanced Pydantic model features for better serialization.

::: xpytools.xtool.xpyt_pydantic
    options:
      show_root_heading: true
      show_root_toc_entry: true

### Examples

```python
from pydantic import BaseModel
from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

class User(BaseModel, TypeSafeAccessMixin):
    id: UUID
    name: str
    created_at: datetime
    tags: List[str]

user = User(
    id="550e8400-e29b-41d4-a716-446655440000",
    name="Alice",
    created_at="2023-01-01T00:00:00Z",
    tags=["admin", "active"]
)

# Auto-serializes complex types for JSON
user_dict = user.model_dump()
# UUID -> string, datetime -> ISO string, etc.
```

## Integration Notes

### Optional Dependencies

Most `xtool` functions require optional dependencies:

- **DataFrame operations**: `pip install pandas`
- **Image processing**: `pip install Pillow`
- **Enhanced text cleaning**: `pip install cleantext`
- **Pydantic extensions**: `pip install pydantic`

### Graceful Degradation

Functions automatically handle missing dependencies:

```python
# If pandas not installed, returns None instead of crashing
result = xtool.df.normalize_column_names(df)
if result is None:
    print("pandas not available")
```

### Decorator Protection

Use `@requireModules` for explicit dependency handling:

```python
from xpytools import xdeco

@xdeco.requireModules(["pandas"], exc_raise=True)
def my_dataframe_function(df):
    return xtool.df.normalize_column_names(df)
```
