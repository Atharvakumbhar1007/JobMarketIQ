"""Analytics router — overview/summary statistics."""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import APIRouter
from src.analysis.location_analysis import (
    overview_stats,
    job_count_by_city,
    remote_ratio,
    employment_type_breakdown,
    top_companies,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
def get_overview():
    """Platform-wide summary statistics."""
    return overview_stats()


@router.get("/locations")
def get_location_stats():
    """Job count by city."""
    df = job_count_by_city()
    return df.to_dict(orient="records")


@router.get("/remote-ratio")
def get_remote_ratio():
    """Distribution of work modes (remote/hybrid/onsite)."""
    df = remote_ratio()
    return df.to_dict(orient="records")


@router.get("/employment-types")
def get_employment_types():
    """Distribution of employment types."""
    df = employment_type_breakdown()
    return df.to_dict(orient="records")


@router.get("/top-companies")
def get_top_companies(n: int = 20):
    """Top N companies by job posting count."""
    df = top_companies(n)
    return df.to_dict(orient="records")
