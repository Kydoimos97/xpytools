"""Comprehensive tests for xpytools.xtype.cast.datetime"""
import pytest
from datetime import datetime, timezone, timedelta


class TestAsDatetimeComprehensive:
    """Exhaustive tests for as_datetime"""

    def test_datetime_passthrough(self):
        from xpytools.xtype.cast import as_datetime
        dt = datetime.now(tz=timezone.utc)
        assert as_datetime(dt) == dt

    def test_iso_string_utc(self):
        from xpytools.xtype.cast import as_datetime
        result = as_datetime("2024-01-01T10:00:00Z")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 1
        assert result.hour == 10

    def test_iso_string_with_offset(self):
        from xpytools.xtype.cast import as_datetime
        result = as_datetime("2024-01-01T10:00:00+05:00")
        assert isinstance(result, datetime)
        assert result.tzinfo is not None

    def test_naive_datetime_string(self):
        from xpytools.xtype.cast import as_datetime
        result = as_datetime("2024-01-01T10:00:00")
        assert isinstance(result, datetime)
        # Should assume UTC by default
        assert result.tzinfo == timezone.utc

    def test_naive_datetime_no_tz_assumption(self):
        from xpytools.xtype.cast import as_datetime
        result = as_datetime("2024-01-01T10:00:00", assume_tz_utc=False)
        assert isinstance(result, datetime)
        assert result.tzinfo is None

    def test_unix_timestamp_int(self):
        from xpytools.xtype.cast import as_datetime
        timestamp = 1704096000  # 2024-01-01 00:00:00 UTC
        result = as_datetime(timestamp)
        assert isinstance(result, datetime)
        assert result.year == 2024

    def test_unix_timestamp_float(self):
        from xpytools.xtype.cast import as_datetime
        timestamp = 1704096000.5
        result = as_datetime(timestamp)
        assert isinstance(result, datetime)
        assert result.microsecond > 0

    def test_invalid_string(self):
        from xpytools.xtype.cast import as_datetime
        assert as_datetime("not a date") is None
        assert as_datetime("2024-99-99") is None

    def test_none_input(self):
        from xpytools.xtype.cast import as_datetime
        assert as_datetime(None) is None

    def test_invalid_timestamp(self):
        from xpytools.xtype.cast import as_datetime
        # Timestamp way out of range
        assert as_datetime(-999999999999999) is None

    def test_unsafe_mode(self):
        from xpytools.xtype.cast import as_datetime
        with pytest.raises(Exception):
            as_datetime("invalid", safe=False)


class TestAsDatetimeStrComprehensive:
    """Exhaustive tests for as_datetime_str"""

    def test_utc_datetime_full(self):
        from xpytools.xtype.cast import as_datetime_str
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        result = as_datetime_str(dt)
        assert result == "2024-01-01T12:30:45"

    def test_naive_datetime_with_utc(self):
        from xpytools.xtype.cast import as_datetime_str
        dt = datetime(2024, 1, 1, 12, 30, 45)
        result = as_datetime_str(dt, include_utc=True)
        assert "+00:00" in result

    def test_naive_datetime_without_utc(self):
        from xpytools.xtype.cast import as_datetime_str
        dt = datetime(2024, 1, 1, 12, 30, 45)
        result = as_datetime_str(dt, include_utc=False)
        assert "+00:00" not in result
        assert "2024-01-01T12:30:45" == result

    def test_date_only(self):
        from xpytools.xtype.cast import as_datetime_str
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        result = as_datetime_str(dt, include_time=False)
        assert result == "2024-01-01"

    def test_date_only_no_utc(self):
        from xpytools.xtype.cast import as_datetime_str
        dt = datetime(2024, 1, 1, 12, 30, 45)
        result = as_datetime_str(dt, include_time=False, include_utc=False)
        assert result == "2024-01-01"

    def test_with_microseconds(self):
        from xpytools.xtype.cast import as_datetime_str
        dt = datetime(2024, 1, 1, 12, 30, 45, 123456, tzinfo=timezone.utc)
        result = as_datetime_str(dt)
        # Should include seconds but microseconds formatting may vary
        assert "12:30:45" in result

    def test_timezone_offset_normalization(self):
        from xpytools.xtype.cast import as_datetime_str
        # Test that +0000 gets converted to +00:00
        tz = timezone(timedelta(hours=0))
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=tz)
        result = as_datetime_str(dt, include_utc=True)
        assert result.endswith("+00:00")

    def test_non_utc_timezone(self):
        from xpytools.xtype.cast import as_datetime_str
        tz = timezone(timedelta(hours=5, minutes=30))
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=tz)
        result = as_datetime_str(dt, include_utc=True)
        assert "+05:30" in result or "+0530" in result

    def test_none_input(self):
        from xpytools.xtype.cast import as_datetime_str
        assert as_datetime_str(None) is None

    def test_invalid_datetime_object(self):
        from xpytools.xtype.cast import as_datetime_str
        assert as_datetime_str("not a datetime") is None

    def test_edge_case_year_boundaries(self):
        from xpytools.xtype.cast import as_datetime_str
        # Very old date
        dt = datetime(1900, 1, 1, tzinfo=timezone.utc)
        result = as_datetime_str(dt)
        assert "1900-01-01" in result

        # Far future
        dt = datetime(2099, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        result = as_datetime_str(dt)
        assert "2099-12-31" in result