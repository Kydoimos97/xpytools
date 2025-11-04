"""
Unit tests for xpytools.types.literal_enum
------------------------------------------
Covers: LiteralEnum, StrLiteral, IntLiteral, FloatLiteral, AnyTLiteral
"""

import pytest
from pydantic import BaseModel, ValidationError

from xpytools.xtype.choice import (
    strChoice,
    intChoice,
    floatChoice,
    anyChoice,
    )


# ---------------------------------------------------------------------------
# LiteralEnum Base Behavior
# ---------------------------------------------------------------------------

def test_literal_enum_accepts_only_allowed_values():
    State = strChoice("open", "closed", "pending")
    assert State("open") == "open"
    assert State("closed") == "closed"
    with pytest.raises(ValueError):
        State("invalid")


def test_literal_enum_mixed_type_support():
    Mixed = anyChoice("a", 1, 2.5)
    assert Mixed("a") == "a"
    assert Mixed(1) == 1
    assert Mixed(2.5) == 2.5
    with pytest.raises(ValueError):
        Mixed("nope")


def test_literal_enum_repr_contains_choices():
    Example = strChoice("x", "y")
    assert "LiteralEnum" in repr(Example)


# ---------------------------------------------------------------------------
# StrLiteral Behavior
# ---------------------------------------------------------------------------

def test_strliteral_valid_values():
    Color = strChoice("red", "green", "blue")
    assert Color("red") == "red"
    with pytest.raises(ValueError):
        Color("yellow")


def test_strliteral_retains_str_behavior():
    Name = strChoice("foo", "bar")
    value = Name("foo")
    assert value.upper() == "FOO"
    assert isinstance(value, str)


# ---------------------------------------------------------------------------
# IntLiteral Behavior
# ---------------------------------------------------------------------------

def test_intliteral_valid_and_invalid():
    Status = intChoice(200, 404, 500)
    assert Status(404) == 404
    with pytest.raises(ValueError):
        Status(403)


def test_intliteral_behaves_like_int():
    Code = intChoice(1, 2, 3)
    value = Code(2)
    assert isinstance(value.bit_length(), int)
    assert value.bit_length() > 0


# ---------------------------------------------------------------------------
# FloatLiteral Behavior
# ---------------------------------------------------------------------------

def test_floatliteral_valid_values():
    Precision = floatChoice(0.1, 0.01)
    assert Precision(0.01) == pytest.approx(0.01)


def test_floatliteral_rejects_invalid_value():
    Precision = floatChoice(0.1, 0.01)
    with pytest.raises(ValueError):
        Precision(1.0)


def test_floatliteral_preserves_float_methods():
    F = floatChoice(1.5, 2.5)
    val = F(1.5)
    assert val.is_integer() is False
    assert isinstance(val.real, float)


# ---------------------------------------------------------------------------
# AnyTLiteral Behavior
# ---------------------------------------------------------------------------

def test_anytliteral_mixed_types_allowed():
    Mixed = anyChoice("foo", 1, None, {})
    assert Mixed("foo") == "foo"
    assert Mixed(1) == 1
    assert Mixed({}) == {}
    assert Mixed(None) is None


def test_anytliteral_rejects_unlisted_value():
    Mixed = anyChoice("foo", 1)
    with pytest.raises(ValueError):
        Mixed("bar")


# ---------------------------------------------------------------------------
# Pydantic Integration
# ---------------------------------------------------------------------------

def test_pydantic_accepts_valid_literal_values():
    Kind = strChoice("cat", "dog")
    Count = intChoice(1, 2, 3)

    class Animal(BaseModel):
        kind: Kind
        count: Count

    a = Animal(kind="cat", count=2)
    assert a.kind == "cat"
    assert a.count == 2


def test_pydantic_rejects_invalid_values():
    Kind = strChoice("cat", "dog")

    class Animal(BaseModel):
        kind: Kind

    with pytest.raises(ValidationError):
        Animal(kind="fish")
