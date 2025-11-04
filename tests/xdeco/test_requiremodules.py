import pytest


class TestRequireModules:
    """Tests for @requireModules decorator"""

    def test_available_module_runs_normally(self):
        from xpytools.xdeco import requireModules

        @requireModules(["sys"])
        def my_func():
            return "success"

        assert my_func() == "success"

    def test_missing_module_returns_none(self):
        from xpytools.xdeco import requireModules

        @requireModules(["nonexistent_module_xyz"])
        def my_func():
            return "should not run"

        assert my_func() is None

    def test_missing_module_raises_when_exc_raise_true(self):
        from xpytools.xdeco import requireModules

        @requireModules(["nonexistent_module_xyz"], exc_raise=True)
        def my_func():
            return "should not run"

        with pytest.raises(ImportError, match="Missing required module"):
            my_func()

    def test_return_none_false_returns_nothing(self):
        from xpytools.xdeco import requireModules

        @requireModules(["nonexistent_module"], return_none=False)
        def my_func():
            return "should not run"

        result = my_func()
        assert result is None  # still returns None but different path

    def test_preserves_function_metadata(self):
        from xpytools.xdeco import requireModules

        @requireModules(["sys"])
        def my_func():
            """Test docstring"""
            pass

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "Test docstring"

    def test_multiple_missing_modules(self):
        from xpytools.xdeco import requireModules

        @requireModules(["fake1", "fake2", "sys"], exc_raise=True)
        def my_func():
            return "should not run"

        with pytest.raises(ImportError) as exc:
            my_func()

        assert "fake1" in str(exc.value)
        assert "fake2" in str(exc.value)
