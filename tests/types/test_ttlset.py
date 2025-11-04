"""
Unit tests for xpytools.types.ttlset
------------------------------------
Tests TTL-based expiration, eviction, and thread-safety behavior.
"""

import threading
import time

import pytest

from xpytools.xtype import TTLSet


@pytest.fixture
def small_ttlset():
    return TTLSet(ttl=0.5, maxsize=4, sweep_interval=2)


def test_add_and_expire(small_ttlset):
    s = small_ttlset
    s.add("a")
    assert "a" in s
    time.sleep(0.6)
    assert "a" not in s  # expired


def test_refresh_existing_key(small_ttlset):
    s = small_ttlset
    s.add("x")
    time.sleep(0.3)
    s.add("x")  # refreshes TTL
    time.sleep(0.3)
    assert "x" in s  # refreshed, still valid


def test_eviction_when_maxsize_reached():
    s = TTLSet(ttl=5, maxsize=3)
    for i in range(5):
        s.add(f"k{i}")
    # Should keep only the most recent 3 keys
    assert len(s._cache) <= 3
    assert "k0" not in s and "k1" not in s


def test_sweep_removes_expired_keys():
    s = TTLSet(ttl=0)
    s.add("a")
    s.add("b")
    s.sweep()
    assert "a" not in s and "b" not in s


def test_clear_empties_cache():
    s = TTLSet(ttl=2)
    s.add("foo")
    s.add("bar")
    s.clear()
    assert "foo" not in s
    assert "bar" not in s
    assert len(s._cache) == 0


def test_thread_safety_during_concurrent_adds():
    s = TTLSet(ttl=2, maxsize=50)
    threads = []

    def worker(i):
        for _ in range(20):
            s.add(f"k{i}")

    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Should not raise any exceptions and still contain some keys
    assert any(f"k{i}" in s for i in range(5))
