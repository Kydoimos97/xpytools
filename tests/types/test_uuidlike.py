"""
Unit tests for xpytools.types.uuidlike
--------------------------------------
Tests standalone validation and Pydantic model integration.
"""

from uuid import UUID

import pytest
from pydantic import BaseModel, ValidationError

from xpytools.xtype import UUIDLike


def test_uuidlike_accepts_valid_str():
    s = "550e8400-e29b-41d4-a716-446655440000"
    assert UUIDLike(s) == s
    assert isinstance(UUIDLike(s), str)


def test_uuidlike_accepts_uuid_object():
    u = UUID("550e8400-e29b-41d4-a716-446655440000")
    result = UUIDLike(u)
    assert isinstance(result, str)
    assert result == str(u)


def test_uuidlike_rejects_invalid_value():
    with pytest.raises(ValueError):
        UUIDLike("123")
    with pytest.raises(ValueError):
        UUIDLike("not-a-uuid")


def test_uuidlike_repr_and_callable():
    assert "UUIDLike" in repr(UUIDLike)
    assert callable(UUIDLike)


def test_uuidlike_works_in_pydantic_model():
    class Example(BaseModel):
        run_id: UUIDLike

    s = "550e8400-e29b-41d4-a716-446655440000"
    model = Example(run_id=s)
    assert model.run_id == s

    with pytest.raises(ValidationError):
        Example(run_id="not-a-uuid")
