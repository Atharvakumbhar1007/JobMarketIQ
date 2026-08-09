"""Jobs router."""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

_JOBS_DF: pd.DataFrame | None = None


def _get_jobs() -> pd.DataFrame:
    global _JOBS_DF
    if _JOBS_DF is None:
        path = PROJECT_ROOT / "data" / "processed" / "jobs_cleaned.csv"
        _JOBS_DF = pd.read_csv(path)
    return _JOBS_DF


@router.get("")
def list_jobs(
    title: str = Query(None, description="Filter by job title (partial match)"),
    location: str = Query(None, description="Filter by location"),
    work_mode: str = Query(None, description="remote | hybrid | onsite"),
    company: str = Query(None, description="Filter by company (partial match)"),
    employment_type: str = Query(None, description="Full-time | Part-time | Contract | Internship"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List jobs with optional filters and pagination."""
    df = _get_jobs().copy()

    if title:
        df = df[df["job_title"].str.contains(title, case=False, na=False)]
    if location:
        df = df[df["location"].str.contains(location, case=False, na=False)]
    if work_mode:
        df = df[df["work_mode"].str.lower() == work_mode.lower()]
    if company:
        df = df[df["company"].str.contains(company, case=False, na=False)]
    if employment_type:
        df = df[df["employment_type"].str.lower() == employment_type.lower()]

    total = len(df)
    start = (page - 1) * page_size
    end = start + page_size
    page_df = df.iloc[start:end]

    results = []
    for _, row in page_df.iterrows():
        results.append({
            "job_id": str(row.get("job_id", "")),
            "job_title": str(row.get("job_title", "")),
            "company": str(row.get("company", "")),
            "location": str(row.get("location", "")),
            "work_mode": str(row.get("work_mode", "")),
            "employment_type": str(row.get("employment_type", "")),
            "salary_min": float(row["salary_min"]) if pd.notna(row.get("salary_min")) else None,
            "salary_max": float(row["salary_max"]) if pd.notna(row.get("salary_max")) else None,
            "experience_min": int(row["experience_min"]) if pd.notna(row.get("experience_min")) else None,
            "experience_max": int(row["experience_max"]) if pd.notna(row.get("experience_max")) else None,
            "remote": bool(row.get("remote", False)),
            "posted_date": str(row.get("posted_date", "")),
            "description": str(row.get("description", ""))[:300] + "..." if len(str(row.get("description", ""))) > 300 else str(row.get("description", "")),
        })

    return {"total": total, "page": page, "page_size": page_size, "results": results}


@router.get("/{job_id}")
def get_job(job_id: str):
    """Get a single job by ID."""
    df = _get_jobs()
    row = df[df["job_id"].astype(str) == job_id]
    if row.empty:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")
    r = row.iloc[0]
    return {
        "job_id": str(r.get("job_id", "")),
        "job_title": str(r.get("job_title", "")),
        "company": str(r.get("company", "")),
        "location": str(r.get("location", "")),
        "work_mode": str(r.get("work_mode", "")),
        "employment_type": str(r.get("employment_type", "")),
        "salary_min": float(r["salary_min"]) if pd.notna(r.get("salary_min")) else None,
        "salary_max": float(r["salary_max"]) if pd.notna(r.get("salary_max")) else None,
        "experience_min": int(r["experience_min"]) if pd.notna(r.get("experience_min")) else None,
        "experience_max": int(r["experience_max"]) if pd.notna(r.get("experience_max")) else None,
        "remote": bool(r.get("remote", False)),
        "posted_date": str(r.get("posted_date", "")),
        "description": str(r.get("description", "")),
    }
