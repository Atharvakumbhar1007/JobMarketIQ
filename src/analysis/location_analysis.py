"""
location_analysis.py
---------------------
Analysis functions for geographic job market trends.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

_PROCESSED = PROJECT_ROOT / "data" / "processed"


def _load_jobs() -> pd.DataFrame:
    return pd.read_csv(_PROCESSED / "jobs_cleaned.csv")


# ============================================================
# Analysis functions
# ============================================================

def job_count_by_city() -> pd.DataFrame:
    """Return total job count per city, sorted descending."""
    df = _load_jobs()
    result = (
        df.groupby("location")
        .size()
        .reset_index(name="job_count")
        .sort_values("job_count", ascending=False)
        .reset_index(drop=True)
    )
    return result


def remote_ratio() -> pd.DataFrame:
    """Return distribution of work modes (remote/hybrid/onsite)."""
    df = _load_jobs()
    result = (
        df.groupby("work_mode")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )
    total = result["count"].sum()
    result["percentage"] = (result["count"] / total * 100).round(1)
    return result


def employment_type_breakdown() -> pd.DataFrame:
    """Return distribution of employment types."""
    df = _load_jobs()
    result = (
        df.groupby("employment_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )
    total = result["count"].sum()
    result["percentage"] = (result["count"] / total * 100).round(1)
    return result


def jobs_by_city_and_mode() -> pd.DataFrame:
    """Return job count grouped by city and work_mode."""
    df = _load_jobs()
    result = (
        df.groupby(["location", "work_mode"])
        .size()
        .reset_index(name="count")
        .sort_values(["location", "count"], ascending=[True, False])
        .reset_index(drop=True)
    )
    return result


def top_companies(n: int = 20) -> pd.DataFrame:
    """Return top N companies by job posting count."""
    df = _load_jobs()
    result = (
        df.groupby("company")
        .size()
        .reset_index(name="job_count")
        .sort_values("job_count", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    return result


def overview_stats() -> dict:
    """Return platform-wide summary statistics."""
    df = _load_jobs()
    df["salary_avg"] = (
        pd.to_numeric(df["salary_min"], errors="coerce") +
        pd.to_numeric(df["salary_max"], errors="coerce")
    ) / 2

    return {
        "total_jobs": int(len(df)),
        "total_companies": int(df["company"].nunique()),
        "total_locations": int(df["location"].nunique()),
        "remote_jobs": int((df["work_mode"] == "remote").sum()),
        "avg_salary": int(df["salary_avg"].mean()),
        "avg_salary_lpa": round(df["salary_avg"].mean() / 100_000, 1),
    }


if __name__ == "__main__":
    print("Jobs by City:")
    print(job_count_by_city().to_string(index=False))

    print("\nWork Mode Distribution:")
    print(remote_ratio().to_string(index=False))

    print("\nOverview Stats:")
    for k, v in overview_stats().items():
        print(f"  {k}: {v}")
