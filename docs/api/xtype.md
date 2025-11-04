# Type System API

The `xtype` module provides safe type handling, validation, and constrained types.

## xcast

Convert between types without crashing. Returns `None` on failure instead of raising exceptions.

::: xpytools.xtype.xcast


### Examples

```python
from xpytools import xcast

# Primitives
xcast.as_int("42")          # 42
xcast.as_int("abc")         # None
xcast.as_float("3.14")      # 3.14
xcast.as_bool("true")       # True
xcast.as_str(123)           # "123"

# JSON
xcast.as_json('{"key": "value"}')  # {"key": "value"}
xcast.as_dict(["key", "value"])    # {"key": "value"}

# Datetime
xcast.as_datetime("2023-01-01")    # datetime object
xcast.as_datetime_str(timestamp)   # ISO string

# Null normalization
xcast.as_none("null")       # None
xcast.as_none("")           # None
xcast.as_none("N/A")        # None
```

## xcheck

Boolean validators for defensive programming. All functions return `True`/`False`.

::: xpytools.xtype.xcheck


### Examples

```python
from xpytools import xcheck

# Type validation
xcheck.is_int(42)           # True
xcheck.is_int("42")         # False
xcheck.is_float(3.14)       # True
xcheck.is_str("hello")      # True

# Collection validation
xcheck.is_dict({"a": 1})    # True
xcheck.is_list_like([1,2])  # True
xcheck.is_empty([])         # True

# Null detection (handles 20+ variants)
xcheck.is_none(None)        # True
xcheck.is_none("null")      # True
xcheck.is_none("")          # True
xcheck.is_none("N/A")       # True
xcheck.is_none(float('nan')) # True

# Special types
xcheck.is_uuid("550e8400-e29b-41d4-a716-446655440000")  # True
xcheck.is_base64("SGVsbG8=")  # True
xcheck.is_json('{"valid": true}')  # True
```

## choice

Create runtime-validated types without full Enum classes. Integrates with Pydantic v2.

::: xpytools.xtype.choice


### Examples

```python
from xpytools.xtype import strChoice, intChoice, floatChoice, anyChoice

# String constraints
Color = strChoice("red", "green", "blue")
color = Color("red")        # "red"
# Color("yellow")           # ValueError

# Integer constraints  
StatusCode = intChoice(200, 404, 500)
code = StatusCode(200)      # 200

# Float constraints
Precision = floatChoice(0.1, 0.01, 0.001)
prec = Precision(0.01)      # 0.01

# Mixed type constraints
Mixed = anyChoice("foo", 1, 2.5, None)
value = Mixed("foo")        # "foo"
```

### Pydantic Integration

```python
from pydantic import BaseModel
from xpytools.xtype import strChoice

UserRole = strChoice("admin", "user", "guest")

class User(BaseModel):
    name: str
    role: UserRole

user = User(name="Alice", role="admin")  # Works
# User(name="Bob", role="invalid")       # ValidationError
```

## Extended Types

Specialized types and containers for advanced use cases.

### TTLSet - Time-to-Live Set

::: xpytools.xtype.TTLSet
    options:
      show_root_heading: true
      show_signature: true

```python
from xpytools.xtype import TTLSet

# Create set with 5-minute TTL
cache = TTLSet(ttl=300)

cache.add("user123")
cache.contains("user123")   # True

# After 5 minutes...
cache.contains("user123")   # False (expired)
```

### UUIDLike - Pydantic UUID Validator

::: xpytools.xtype.UUIDLike
    options:
      show_root_heading: true
      show_signature: true

```python
from pydantic import BaseModel
from xpytools.xtype import UUIDLike

class Record(BaseModel):
    id: UUIDLike

# Accepts both string and UUID objects
record1 = Record(id="550e8400-e29b-41d4-a716-446655440000")
record2 = Record(id=uuid.uuid4())
```
