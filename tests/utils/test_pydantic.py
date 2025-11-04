from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

import pytest

pydantic = pytest.importorskip("xpyt_pydantic", reason="xpyt_pydantic required for xpyt_pydantic tests")
from pydantic import BaseModel


class TestTypeSafeAccessMixin:
    """Tests for TypeSafeAccessMixin"""

    def test_basic_attribute_access(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class User(TypeSafeAccessMixin, BaseModel):
            name: str
            age: int

        user = User(name="Alice", age=30)
        assert user.get_type_safe_attr("name") == "Alice"
        assert user.get_type_safe_attr("age") == 30

    def test_get_all_type_safe_attr(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class User(TypeSafeAccessMixin, BaseModel):
            name: str
            age: int

        user = User(name="Bob", age=25)
        all_attrs = user.get_all_type_safe_attr()
        assert all_attrs["name"] == "Bob"
        assert all_attrs["age"] == 25

    def test_uuid_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Record(TypeSafeAccessMixin, BaseModel):
            id: UUID

        uid = uuid4()
        record = Record(id=uid)
        result = record.get_type_safe_attr("id")
        assert isinstance(result, str)
        assert result == str(uid)

    def test_enum_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Status(Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        class User(TypeSafeAccessMixin, BaseModel):
            status: Status

        user = User(status=Status.ACTIVE)
        result = user.get_type_safe_attr("status")
        assert result == "ACTIVE"

    def test_datetime_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Event(TypeSafeAccessMixin, BaseModel):
            timestamp: datetime

        event = Event(timestamp=datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
        result = event.get_type_safe_attr("timestamp")
        assert isinstance(result, str)
        assert "2024-01-01" in result

    def test_nested_model_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Address(BaseModel):
            city: str
            zip: str

        class User(TypeSafeAccessMixin, BaseModel):
            name: str
            address: Address

        user = User(name="Charlie", address=Address(city="NYC", zip="10001"))
        result = user.get_type_safe_attr("address")
        assert isinstance(result, dict)
        assert result["city"] == "NYC"
        assert result["zip"] == "10001"

    def test_list_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Record(TypeSafeAccessMixin, BaseModel):
            tags: list[str]

        record = Record(tags=["python", "testing"])
        result = record.get_type_safe_attr("tags")
        assert result == ["python", "testing"]

    def test_dict_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Record(TypeSafeAccessMixin, BaseModel):
            metadata: dict[str, int]

        record = Record(metadata={"a": 1, "b": 2})
        result = record.get_type_safe_attr("metadata")
        assert result == {"a": 1, "b": 2}

    def test_none_handling(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class User(TypeSafeAccessMixin, BaseModel):
            name: str
            nickname: str | None = None

        user = User(name="Dave", nickname=None)
        result = user.get_type_safe_attr("nickname")
        assert result is None

    def test_invalid_field_raises(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class User(TypeSafeAccessMixin, BaseModel):
            name: str

        user = User(name="Eve")
        with pytest.raises(KeyError, match="not a valid field"):
            user.get_type_safe_attr("nonexistent")

    def test_exclude_fields(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class User(TypeSafeAccessMixin, BaseModel):
            name: str
            password: str
            age: int

        user = User(name="Frank", password="secret", age=35)
        result = user.get_all_type_safe_attr(exclude_fields=["password"])
        assert "name" in result
        assert "age" in result
        assert "password" not in result

    def test_uuid_coercion_from_string(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Record(TypeSafeAccessMixin, BaseModel):
            id: UUID

        uid_str = "550e8400-e29b-41d4-a716-446655440000"
        record = Record(id=uid_str)
        assert isinstance(record.id, UUID)
        assert str(record.id) == uid_str

    def test_json_field_coercion(self):
        from xpytools.xtool.xpyt_pydantic import TypeSafeAccessMixin

        class Config(TypeSafeAccessMixin, BaseModel):
            settings: dict

        config = Config(settings='{"key": "value"}')
        assert isinstance(config.settings, dict)
        assert config.settings == {"key": "value"}
