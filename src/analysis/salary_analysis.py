"""
salary_analysis.py
------------------
Analysis functions for salary patterns and trends.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np

_PROCESSED = PROJECT_ROOT / "data" / "processed"


def _load_jobs() -> pd.DataFrame:
    df = pd.read_csv(_PROCESSED / "jobs_cleaned.csv")
    df["salary_avg"] = (
        pd.to_numeric(df["salary_min"], errors="coerce") +
        pd.to_numeric(df["salary_max"], errors="coerce")
    ) / 2
    return df


# ============================================================
# Analysis functions
# ============================================================

def salary_by_role(n: int = 20) -> pd.DataFrame:
    """
    Return average salary (min, max, avg) grouped by job title.
    Sorted by average salary descending.
    """
    df = _load_jobs()
    result = (
        df.groupby("job_title")
        .agg(
            salary_min=("salary_min", "mean"),
            salary_max=("salary_max", "mean"),
            salary_avg=("salary_avg", "mean"),
            job_count=("job_id", "count"),
        )
        .round(0)
        .sort_values("salary_avg", ascending=False)
        .head(n)
        .reset_index()
    )
    return result


def salary_by_location(n: int = 15) -> pd.DataFrame:
    """
    Return average salary grouped by location.
    """
    df = _load_jobs()
    result = (
        df.groupby("location")
        .agg(
            salary_avg=("salary_avg", "mean"),
            salary_min=("salary_min", "mean"),
            salary_max=("salary_max", "mean"),
            job_count=("job_id", "count"),
        )
        .round(0)
        .sort_values("salary_avg", ascending=False)
        .head(n)
        .reset_index()
    )
    return result


def salary_by_experience() -> pd.DataFrame:
    """
    Return average salary grouped by experience bracket.
    """
    df = _load_jobs()
    df["exp_bracket"] = pd.cut(
        pd.to_numeric(df["experience_min"], errors="coerce"),
        bins=[-1, 1, 3, 5, 8, 15, 100],
        labels=["0-1 yrs", "1-3 yrs", "3-5 yrs", "5-8 yrs", "8-15 yrs", "15+ yrs"],
    )
    result = (
        df.groupby("exp_bracket", observed=True)
        .agg(
            salary_avg=("salary_avg", "mean"),
            job_count=("job_id", "count"),
        )
        .round(0)
        .reset_index()
    )
    return result


def salary_by_work_mode() -> pd.DataFrame:
    """Return average salary by work mode (remote/hybrid/onsite)."""
    df = _load_jobs()
    result = (
        df.groupby("work_mode")
        .agg(
            salary_avg=("salary_avg", "mean"),
            job_count=("job_id", "count"),
        )
        .round(0)
        .sort_values("salary_avg", ascending=False)
        .reset_index()
    )
    return result


def salary_distribution_stats() -> dict:
    """Return overall salary distribution statistics."""
    df = _load_jobs()
    avgs = df["salary_avg"].dropna()
    return {
        "count": int(len(avgs)),
        "mean": int(avgs.mean()),
        "median": int(avgs.median()),
        "min": int(avgs.min()),
        "max": int(avgs.max()),
        "p25": int(np.percentile(avgs, 25)),
        "p75": int(np.percentile(avgs, 75)),
    }


if __name__ == "__main__":
    print("Salary by Role (top 10):")
    print(salary_by_role(10).to_string(index=False))

    print("\nSalary by Location:")
    print(salary_by_location().to_string(index=False))

    print("\nSalary by Experience:")
    print(salary_by_experience().to_string(index=False))

    print("\nDistribution Stats:")
    stats = salary_distribution_stats()
    for k, v in stats.items():
        print(f"  {k}: {v:,}")
