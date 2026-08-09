"""
test_pipeline.py
-----------------
Unit tests for the data pipeline and analysis functions.
Run from project root: pytest tests/ -v
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
import pandas as pd
from src.data.transform import (
    clean_column_names,
    normalize_job_title,
    normalize_location,
    normalize_work_mode,
    remove_duplicates,
)


# ============================================================
# Transform tests
# ============================================================

def test_clean_column_names():
    df = pd.DataFrame(columns=["Job Title", "Company Name", "Posted-Date"])
    result = clean_column_names(df)
    assert "job_title" in result.columns
    assert "company_name" in result.columns
    assert "posted_date" in result.columns


def test_clean_column_names_strips_spaces():
    df = pd.DataFrame(columns=["  job title  "])
    result = clean_column_names(df)
    assert "job_title" in result.columns


def test_normalize_job_title_title_case():
    assert normalize_job_title("  senior DATA scientist ") == "Senior Data Scientist"


def test_normalize_job_title_nan():
    assert normalize_job_title(float("nan")) == ""


def test_normalize_location_alias_bombay():
    assert normalize_location("Bombay") == "Mumbai"


def test_normalize_location_alias_bengaluru():
    assert normalize_location("bengaluru") == "Bangalore"


def test_normalize_location_unknown_passthrough():
    assert normalize_location("Jaipur") == "Jaipur"


def test_normalize_location_nan():
    assert normalize_location(float("nan")) == ""


def test_normalize_work_mode_remote():
    assert normalize_work_mode("work from home") == "remote"
    assert normalize_work_mode("wfh") == "remote"
    assert normalize_work_mode("REMOTE") == "remote"


def test_normalize_work_mode_hybrid():
    assert normalize_work_mode("hybrid") == "hybrid"
    assert normalize_work_mode("partial remote") == "hybrid"


def test_normalize_work_mode_onsite():
    assert normalize_work_mode("on-site") == "onsite"
    assert normalize_work_mode("office") == "onsite"


def test_normalize_work_mode_unknown():
    assert normalize_work_mode("flexible") == "unknown"
    assert normalize_work_mode(float("nan")) == "unknown"


def test_remove_duplicates_by_job_id():
    df = pd.DataFrame({
        "job_id": ["A", "B", "A"],
        "title": ["Dev", "Eng", "Dev"],
    })
    result = remove_duplicates(df)
    assert len(result) == 2


def test_remove_duplicates_no_job_id():
    df = pd.DataFrame({
        "title": ["Dev", "Eng", "Dev"],
        "company": ["X", "Y", "X"],
    })
    result = remove_duplicates(df)
    assert len(result) == 2