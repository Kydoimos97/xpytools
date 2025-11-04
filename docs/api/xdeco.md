# Decorators API

The `xdeco` module provides lightweight decorators for runtime safety and object management.

## Function Decorators

::: xpytools.xdeco


## @requireModules

Gracefully handle missing optional dependencies. Functions can either return `None` or raise `ImportError` when required modules are unavailable.

### Examples

```python
from xpytools import xdeco

# Return None if modules missing (default)
@xdeco.requireModules(["pandas", "numpy"])
def process_data():
    import pandas as pd
    import numpy as np
    return pd.DataFrame(np.random.randn(100, 4))

result = process_data()
if result is None:
    print("pandas or numpy not available")

# Raise ImportError if modules missing
@xdeco.requireModules(["requests"], exc_raise=True)
def fetch_data(url):
    import requests
    return requests.get(url).json()

# Control return behavior
@xdeco.requireModules(["matplotlib"], return_none=False, exc_raise=False)
def plot_data(data):
    # Function simply won't execute if matplotlib missing
    import matplotlib.pyplot as plt
    plt.plot(data)
```

### Parameters

- `modules`: List of module names to check (e.g., `["pandas", "numpy"]`)
- `exc_raise`: Raise `ImportError` if modules missing (default: `False`)
- `return_none`: Return `None` if modules missing (default: `True`)

### Use Cases

**ETL Pipelines**: Gracefully skip optional processing steps
```python
@xdeco.requireModules(["pandas"])
def optimize_dataframe(df):
    # Only runs if pandas available
    return df.memory_usage(deep=True).sum()
```

**Optional Features**: Enable advanced functionality only when dependencies exist
```python
@xdeco.requireModules(["PIL"], exc_raise=False)
def generate_thumbnail(image_path):
    from PIL import Image
    img = Image.open(image_path)
    img.thumbnail((128, 128))
    return img
```

**Development vs Production**: Different behavior based on available tools
```python
@xdeco.requireModules(["pytest"])
def run_tests():
    import pytest
    return pytest.main(["-v", "tests/"])
```

## @asSingleton

Enforce singleton pattern on classes. Ensures only one instance exists, returning the same object on subsequent instantiations.

### Examples

```python
from xpytools import xdeco

@xdeco.asSingleton
class DatabaseConnection:
    def __init__(self, host="localhost"):
        self.host = host
        self.connection = self._establish_connection()
    
    def _establish_connection(self):
        # Expensive connection setup
        return f"Connected to {self.host}"

# First instantiation creates the object
db1 = DatabaseConnection("prod-server")
print(db1.connection)  # "Connected to prod-server"

# Subsequent calls return the same instance
db2 = DatabaseConnection("different-server")  # Ignored!
print(db2 is db1)      # True
print(db2.connection)  # "Connected to prod-server"
```

### Use Cases

**Resource Management**: Expensive objects that should only exist once
```python
@xdeco.asSingleton
class CacheManager:
    def __init__(self):
        self.cache = {}
        self.stats = {"hits": 0, "misses": 0}
```

**Configuration**: Global settings objects
```python
@xdeco.asSingleton
class AppConfig:
    def __init__(self):
        self.settings = self._load_config()
    
    def _load_config(self):
        # Load from environment, files, etc.
        return {"debug": True, "api_key": "secret"}
```

**Logging**: Centralized logging instances
```python
@xdeco.asSingleton
class Logger:
    def __init__(self):
        self.handlers = []
        self.setup_logging()
```

## Best Practices

### Combining Decorators

```python
@xdeco.asSingleton
@xdeco.requireModules(["redis"], exc_raise=True)
class RedisCache:
    def __init__(self, host="localhost"):
        import redis
        self.client = redis.Redis(host=host)
```

### Error Handling

```python
@xdeco.requireModules(["expensive_lib"])
def optional_feature():
    try:
        import expensive_lib
        return expensive_lib.do_work()
    except Exception as e:
        # Function only runs if modules available
        # But can still handle runtime errors
        return None
```

### Testing Considerations

```python
# Test with missing dependencies
def test_graceful_degradation():
    # Mock missing module
    with patch.dict('sys.modules', {'pandas': None}):
        result = my_pandas_function()
        assert result is None

# Test singleton behavior
def test_singleton():
    obj1 = MySingleton()
    obj2 = MySingleton()
    assert obj1 is obj2
```

## Implementation Notes

- `@requireModules` checks module availability at decoration time
- `@asSingleton` stores instances in class-level registry
- Both decorators preserve function signatures and docstrings
- Thread-safe singleton implementation
- Minimal performance overhead
