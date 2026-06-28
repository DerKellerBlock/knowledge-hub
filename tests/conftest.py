"""Shared pytest configuration for Knowledge Hub tests.

Auto-applies the layer markers (unit/integration/e2e/mcp) based on the test
file's directory, so individual test files do not need to repeat
``@pytest.mark.<layer>`` on every test. This keeps the marker-based layer
selection (``-m unit`` etc.) working with the plan's test files.

Task 6 of the test-suite plan extends this file with the ``tmp_hub``,
``dummy_domain`` and ``indexed_dummy`` fixtures.
"""

import pytest


def pytest_collection_modifyitems(items):
    """Auto-mark tests by directory so ``-m <layer>`` works without per-test
    decorators."""
    for item in items:
        # item.fspath is the path to the test file
        parts = item.fspath.strpath.split("/tests/")
        if len(parts) != 2:
            continue
        layer = parts[1].split("/")[0]  # unit | integration | e2e | mcp
        marker = getattr(pytest.mark, layer, None)
        if marker is not None:
            item.add_marker(marker)