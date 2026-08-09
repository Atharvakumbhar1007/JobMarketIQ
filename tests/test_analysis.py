"""
test_analysis.py
----------------
Unit tests for the analysis functions.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Create a mock for the read_csv calls
@pytest.fixture(autouse=True)
def mock_data(monkeypatch):
    def mock_read_csv(filepath, *args, **kwargs):
        filepath = str(filepath)
        if "jobs_cleaned.csv" in filepath:
            return pd.DataFrame({
                "job_id": ["1", "2", "3", "4"],
                "job_title": ["Data Scientist", "Software Engineer", "Data Scientist", "Frontend Developer"],
                "company": ["Tech A", "Tech B", "Tech C", "Tech A"],
                "location": ["Bangalore", "Mumbai", "Bangalore", "Pune"],
                "salary_min": [1000000, 800000, 1200000, 600000],
                "salary_max": [1500000, 1200000, 1800000, 1000000],
                "experience_min": [2, 1, 3, 1],
                "experience_max": [5, 3, 6, 3],
                "employment_type": ["Full-time", "Full-time", "Contract", "Full-time"],
                "work_mode": ["remote", "hybrid", "onsite", "remote"],
            })
        elif "job_skills.csv" in filepath:
            return pd.DataFrame({
                "job_id": ["1", "1", "2", "3", "4"],
                "skill_name": ["Python", "SQL", "Python", "Python", "React"],
                "category": ["Languages", "Databases", "Languages", "Languages", "Frameworks"],
            })
        elif "skills.csv" in filepath:
            return pd.DataFrame({
                "skill_name": ["Python", "SQL", "React"],
                "category": ["Languages", "Databases", "Frameworks"],
                "demand_count": [3, 1, 1],
            })
        return pd.DataFrame()

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)


def test_top_skills():
    from src.analysis.skill_demand import top_skills
    res = top_skills(2)
    assert len(res) == 2
    assert res.iloc[0]["skill_name"] == "Python"
    assert res.iloc[0]["demand_count"] == 3


def test_skill_by_location():
    from src.analysis.skill_demand import skill_by_location
    res = skill_by_location("Bangalore")
    # Job 1 (Python, SQL), Job 3 (Python) are in Bangalore
    assert len(res) == 2
    assert res[res["skill_name"] == "Python"]["count"].values[0] == 2
    assert res[res["skill_name"] == "SQL"]["count"].values[0] == 1


def test_salary_by_role():
    from src.analysis.salary_analysis import salary_by_role
    res = salary_by_role()
    assert len(res) == 3
    
    ds = res[res["job_title"] == "Data Scientist"].iloc[0]
    assert ds["job_count"] == 2
    # DS1: min 1M, max 1.5M => avg 1.25M
    # DS2: min 1.2M, max 1.8M => avg 1.5M
    # Mean of avgs = 1.375M
    assert ds["salary_avg"] == 1375000.0


def test_salary_distribution_stats():
    from src.analysis.salary_analysis import salary_distribution_stats
    res = salary_distribution_stats()
    assert res["count"] == 4
    # Avgs: 1.25M, 1M, 1.5M, 0.8M
    # Mean = 1.1375M
    assert res["mean"] == 1137500


def test_overview_stats():
    from src.analysis.location_analysis import overview_stats
    res = overview_stats()
    assert res["total_jobs"] == 4
    assert res["total_companies"] == 3
    assert res["total_locations"] == 3
    assert res["remote_jobs"] == 2


def test_skill_gap_analysis():
    from src.analysis.skill_gap import skill_gap
    # Target Data Scientist: skills required are Python (2 jobs), SQL (1 job)
    res = skill_gap(["Python"], "Data Scientist")
    assert res["target_role"] == "Data Scientist"
    assert res["role_skill_count"] == 2
    assert res["user_match_count"] == 1
    assert "Python" in res["matched_skills"]
    assert res["missing_skills"][0]["skill_name"] == "SQL"
    assert res["missing_skills"][0]["pct_jobs"] == 50.0  # 1 out of 2 jobs
