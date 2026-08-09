"""Skills router."""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import APIRouter, Query
from src.analysis.skill_demand import top_skills, skill_by_location, skill_trend_by_category, skills_by_role, unique_locations, unique_roles
from src.analysis.skill_gap import skill_gap, available_roles, get_role_skills

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("/top")
def get_top_skills(n: int = Query(20, ge=1, le=100)):
    """Return top N most demanded skills across all jobs."""
    df = top_skills(n)
    return df.to_dict(orient="records")


@router.get("/by-location")
def get_skills_by_location(
    location: str = Query(..., description="City name"),
    n: int = Query(15, ge=1, le=50),
):
    """Return top skills in demand for a specific city."""
    df = skill_by_location(location, n)
    return df.to_dict(orient="records")


@router.get("/by-role")
def get_skills_by_role(
    role: str = Query(..., description="Job title"),
    n: int = Query(15, ge=1, le=50),
):
    """Return top skills required for a specific job role."""
    df = skills_by_role(role, n)
    return df.to_dict(orient="records")


@router.get("/categories")
def get_skill_categories():
    """Return skill demand broken down by category."""
    df = skill_trend_by_category()
    return df.to_dict(orient="records")


@router.get("/locations")
def get_available_locations():
    """Return list of all available locations."""
    return {"locations": unique_locations()}


@router.get("/roles")
def get_available_roles():
    """Return list of all available job roles."""
    return {"roles": unique_roles()}


@router.post("/gap")
def analyze_skill_gap(
    user_skills: list[str],
    target_role: str = Query(...),
    top_n: int = Query(15, ge=5, le=30),
):
    """Analyze skill gap between user's skills and target role requirements."""
    result = skill_gap(user_skills, target_role, top_n)
    return result
