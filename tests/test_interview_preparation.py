"""
Unit tests for Phase 12 Bain Interview Defense document.
"""

import os
import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")

def test_interview_preparation_exists():
    path = os.path.join(REPO_ROOT, "INTERVIEW_PREPARATION.md")
    assert os.path.exists(path), "Missing INTERVIEW_PREPARATION.md"
    assert os.path.getsize(path) > 2000, "INTERVIEW_PREPARATION.md is empty or too short."

def test_all_40_questions_answered():
    path = os.path.join(REPO_ROOT, "INTERVIEW_PREPARATION.md")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for q_num in range(1, 41):
        assert f"Q{q_num}:" in content, f"Missing Question Q{q_num} in INTERVIEW_PREPARATION.md"

def test_pyramid_principle_answers_present():
    path = os.path.join(REPO_ROOT, "INTERVIEW_PREPARATION.md")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "30-second answer" in content
    assert "2-minute answer" in content
    assert "5-minute walkthrough" in content
