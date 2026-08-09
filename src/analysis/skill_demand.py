"""
skill_demand.py
---------------
Analysis functions for skill demand trends.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

# ============================================================
# Data loading helpers
# ============================================================

_PROCESSED = PROJECT_ROOT / "data" / "processed"


def _load_job_skills() -> pd.DataFrame:
    return pd.read_csv(_PROCESSED / "job_skills.csv")


def _load_jobs() -> pd.DataFrame:
    return pd.read_csv(_PROCESSED / "jobs_cleaned.csv")


def _load_skills_catalog() -> pd.DataFrame:
    return pd.read_csv(_PROCESSED / "skills.csv")


# ============================================================
# Analysis functions
# ============================================================

def top_skills(n: int = 20) -> pd.DataFrame:
    """
    Return the top N most demanded skills across all jobs.
    Returns DataFrame: skill_name, category, demand_count
    """
    catalog = _load_skills_catalog()
    return (
        catalog
        .sort_values("demand_count", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def skill_by_location(location: str, n: int = 15) -> pd.DataFrame:
    """
    Return top N skills for jobs in a specific location.
    """
    jobs = _load_jobs()
    job_skills = _load_job_skills()

    # Filter jobs to the given location
    location_jobs = jobs[jobs["location"].str.lower() == location.lower()]
    if location_jobs.empty:
        return pd.DataFrame(columns=["skill_name", "category", "count"])

    local_job_ids = set(location_jobs["job_id"].astype(str))

    # Filter job_skills to those job_ids
    local_skills = job_skills[job_skills["job_id"].astype(str).isin(local_job_ids)]

    result = (
        local_skills
        .groupby(["skill_name", "category"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    return result


def skill_trend_by_category() -> pd.DataFrame:
    """
    Return total demand count broken down by skill category.
    """
    job_skills = _load_job_skills()
    result = (
        job_skills
        .groupby("category")
        .size()
        .reset_index(name="total_mentions")
        .sort_values("total_mentions", ascending=False)
        .reset_index(drop=True)
    )
    return result


def skills_by_role(job_title: str, n: int = 15) -> pd.DataFrame:
    """
    Return top N skills associated with a specific job title.
    """
    jobs = _load_jobs()
    job_skills = _load_job_skills()

    role_jobs = jobs[jobs["job_title"].str.lower() == job_title.lower()]
    if role_jobs.empty:
        return pd.DataFrame(columns=["skill_name", "category", "count"])

    role_job_ids = set(role_jobs["job_id"].astype(str))
    role_skills = job_skills[job_skills["job_id"].astype(str).isin(role_job_ids)]

    result = (
        role_skills
        .groupby(["skill_name", "category"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    return result


def unique_locations() -> list[str]:
    """Return list of all unique locations in the dataset."""
    jobs = _load_jobs()
    return sorted(jobs["location"].dropna().unique().tolist())


def unique_roles() -> list[str]:
    """Return list of all unique job titles in the dataset."""
    jobs = _load_jobs()
    return sorted(jobs["job_title"].dropna().unique().tolist())


if __name__ == "__main__":
    print("Top 15 skills globally:")
    print(top_skills(15).to_string(index=False))

    print("\nTop skills in Bangalore:")
    print(skill_by_location("Bangalore", 10).to_string(index=False))

    print("\nSkill category breakdown:")
    print(skill_trend_by_category().to_string(index=False))
