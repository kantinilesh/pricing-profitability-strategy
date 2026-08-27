"""
Unit tests for Phase 11 Executive Presentation.
"""

import os
import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")

def test_executive_presentation_exists():
    path = os.path.join(REPO_ROOT, "EXECUTIVE_PRESENTATION.md")
    assert os.path.exists(path), "Missing EXECUTIVE_PRESENTATION.md"
    assert os.path.getsize(path) > 1000, "EXECUTIVE_PRESENTATION.md is empty or too short."

def test_all_10_slides_present():
    path = os.path.join(REPO_ROOT, "EXECUTIVE_PRESENTATION.md")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for slide_num in range(1, 11):
        assert f"Slide {slide_num}:" in content, f"Missing Slide {slide_num} in EXECUTIVE_PRESENTATION.md"
        assert f"Headline" in content, f"Missing Headline structure in EXECUTIVE_PRESENTATION.md"
