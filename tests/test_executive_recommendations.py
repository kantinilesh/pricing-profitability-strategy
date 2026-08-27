"""
Unit tests for Phase 10 Executive Recommendations.
"""

import os
import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")

def test_executive_markdown_files_exist():
    expected_files = [
        "EXECUTIVE_SUMMARY.md",
        "MANAGEMENT_RECOMMENDATIONS.md",
        "PRIORITIZATION_MATRIX.md"
    ]
    for f in expected_files:
        path = os.path.join(REPO_ROOT, f)
        assert os.path.exists(path), f"Missing executive document: {f}"
        assert os.path.getsize(path) > 500, f"Executive document {f} is empty or too short."
