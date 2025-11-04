# xPyTools

Complete documentation for all xpytools modules and functions.

**New to xpytools?** See [Installation](../installation.md) for setup instructions.

## Type System (xtype)

Safe type conversions, runtime validation, and constrained types.

- **[xcast](xtype/xcast.md)** - Safe type conversions that return `None` on failure
- **[xcheck](xtype/xcheck.md)** - Runtime type validation with boolean returns
- **[choice](xtype/choice.md)** - Constrained types without full Enum classes
- **[Types](xtype/types.md)** - Specialized type implementations (TTLSet, UUIDLike)
- **[Common Types](xtype/common.md)** - Shared type annotations and utilities

## Utilities (xtool)

DataFrame operations, image processing, text manipulation, and SQL helpers.

- **[DataFrame Operations](xtool/df.md)** - Clean and transform pandas data
- **[Image Processing](xtool/img.md)** - Unified I/O from any source
- **[Text Processing](xtool/txt.md)** - String manipulation and cleaning
- **[SQL Bridge](xtool/sql.md)** - Prepare data for database insertion
- **[Pydantic Extensions](xtool/pydantic.md)** - Enhanced model features

## Decorators (xdeco)

Function enhancers for dependency management and design patterns.

- **[@requireModules](xdeco/requireModules.md)** - Graceful dependency handling
- **[@asSingleton](xdeco/asSingleton.md)** - Singleton pattern enforcement

## External Links

- **[PyPI Package](https://pypi.org/project/xpytools/)** - Install with `pip install xpytools`
- **[GitHub Repository](https://github.com/Kydoimos97/xpytools)** - Source code and issues
- **[Author Profile](https://github.com/Kydoimos97)** - Kydoimos97 on GitHub