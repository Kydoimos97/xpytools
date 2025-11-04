import pytest


class TestAsSingleton:
    """Tests for @asSingleton decorator"""

    def test_singleton_creates_single_instance(self):
        from xpytools.xdeco import asSingleton

        @asSingleton
        class MyClass:
            def __init__(self, value):
                self.value = value

        obj1 = MyClass(10)
        obj2 = MyClass(20)

        assert obj1 is obj2
        assert obj1.value == 10  # init only called once
        assert obj2.value == 10

    def test_singleton_preserves_class_metadata(self):
        from xpytools.xdeco import asSingleton

        @asSingleton
        class MyClass:
            """Test docstring"""
            pass

        assert MyClass.__name__ == "MyClass"
        assert MyClass.__doc__ == "Test docstring"

    def test_singleton_raises_on_new_override(self):
        from xpytools.xdeco import asSingleton

        with pytest.raises(Exception, match="Singleton violation"):
            @asSingleton
            class BadClass:
                def __new__(cls):
                    pass

    def test_singleton_raises_on_cls_instance_attr(self):
        from xpytools.xdeco import asSingleton

        with pytest.raises(Exception, match="Singleton violation"):
            @asSingleton
            class BadClass:
                __cls_instance = None
