# Installation

## Requirements

Python 3.11+

## Install
```bash
# Core functionality (no dependencies)
pip install xpytools

# With all optional features
pip install xpytools[all]
```

## What's in [all]

The `[all]` extra includes optional dependencies for extended functionality:

- **pandas, numpy** - DataFrame operations
- **Pillow** - Image processing  
- **clean-text** - Enhanced text cleaning
- **pydantic** - Choice type integration
- **requests** - URL-based image loading
- **tiktoken** - Token counting utilities

## Verify Installation
```python
from xpytools import xcast, xcheck
from xpytools.xtype import strChoice

result = xcast.as_int("42")           # 42
valid = xcheck.is_none(None)          # True
Color = strChoice("red", "blue")      # Works without any deps
valid_color = Color('red')
```

## Development
```bash
git clone https://github.com/Kydoimos97/xpytools.git
cd xpytools
pip install -e .[all]
```