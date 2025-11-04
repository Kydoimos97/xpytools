"""
pytest configuration for xpytools test suite
"""
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
            "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
            )
    config.addinivalue_line(
            "markers", "integration: marks tests as integration tests"
            )


@pytest.fixture
def sample_dict():
    """Sample nested dictionary for testing"""
    return {
            "name": "test",
            "nested": {
                    "value": 42,
                    "deep": {
                            "key": "value"
                            }
                    },
            "list": [1, 2, 3]
            }


@pytest.fixture
def sample_json_string():
    """Sample JSON string for testing"""
    return '{"name": "test", "value": 42, "items": [1, 2, 3]}'
