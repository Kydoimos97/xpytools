# Installation

## Requirements

- Python 3.11 or higher
- Optional dependencies based on features used

## Install from PyPI

```bash
pip install xpytools
```

## Install with All Dependencies

For full functionality including pandas, PIL, and Pydantic support:

```bash
pip install xpytools[all]
```

## Development Installation

To install from source for development:

```bash
git clone https://github.com/Kydoimos97/xpytools.git
cd xpytools
pip install -e .
```

For development with all dependencies:

```bash
pip install -e .[all]
```

## Optional Dependencies

xpytools is designed with minimal core dependencies. Additional functionality requires optional packages:

### DataFrame Operations
```bash
pip install pandas
```
Required for: `xtool.df.*`, `xcast.as_df()`, DataFrame-related checks

### Image Processing
```bash
pip install Pillow
```
Required for: `xtool.img.*` image loading and manipulation

### Enhanced Text Cleaning
```bash
pip install cleantext
```
Required for: Advanced text normalization in `xtool.txt.clean()`

### Pydantic Integration
```bash
pip install pydantic
```
Required for: `choice` types in Pydantic models, `xtool.pydantic.*`

## Import Verification

Test your installation:

```python
from xpytools import xcast, xcheck, xtool
from xpytools.xtype import strChoice

# Basic functionality
result = xcast.as_int("42")
print(f"✓ xcast working: {result}")

valid = xcheck.is_none(None)
print(f"✓ xcheck working: {valid}")

Color = strChoice("red", "green", "blue")
color = Color("red")
print(f"✓ choice working: {color}")
```

Expected output:
```
✓ xcast working: 42
✓ xcheck working: True
✓ choice working: red
```

## Troubleshooting

### ImportError for Optional Features

If you get import errors for pandas, PIL, or other optional dependencies:

```python
from xpytools import xdeco

@xdeco.requireModules(["pandas"])
def my_df_function():
    # This will gracefully skip if pandas isn't installed
    import pandas as pd
    return pd.DataFrame()
```

### Version Compatibility

Check your Python version:
```bash
python --version  # Should be 3.11+
```

Upgrade if needed:
```bash
pip install --upgrade python
```