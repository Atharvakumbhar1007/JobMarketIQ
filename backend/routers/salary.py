"""Salary router."""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import APIRouter, Query, HTTPException
from backend.schemas import SalaryPredictRequest
from src.analysis.salary_analysis import (
    salary_by_role,
    salary_by_location,
    salary_by_experience,
    salary_by_work_mode,
    salary_distribution_stats,
)

router = APIRouter(prefix="/api/salary", tags=["salary"])


@router.get("/by-role")
def get_salary_by_role(n: int = Query(20, ge=1, le=50)):
    """Return average salary grouped by job title."""
    df = salary_by_role(n)
    return df.to_dict(orient="records")


@router.get("/by-location")
def get_salary_by_location(n: int = Query(15, ge=1, le=30)):
    """Return average salary grouped by location."""
    df = salary_by_location(n)
    return df.to_dict(orient="records")


@router.get("/by-experience")
def get_salary_by_experience():
    """Return average salary by experience bracket."""
    df = salary_by_experience()
    return df.to_dict(orient="records")


@router.get("/by-work-mode")
def get_salary_by_work_mode():
    """Return average salary by work mode (remote/hybrid/onsite)."""
    df = salary_by_work_mode()
    return df.to_dict(orient="records")


@router.get("/stats")
def get_salary_stats():
    """Return overall salary distribution statistics."""
    return salary_distribution_stats()


@router.post("/predict")
def predict_salary(request: SalaryPredictRequest):
    """
    Predict salary using the trained ML model.
    Returns predicted salary and confidence range.
    """
    try:
        from ml.predict import predict_salary as _predict
        result = _predict(
            job_title=request.job_title,
            location=request.location,
            company=request.company,
            employment_type=request.employment_type,
            experience_min=request.experience_min,
            experience_max=request.experience_max,
            skill_count=request.skill_count,
            work_mode=request.work_mode,
        )
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.get("/predict/options")
def get_predict_options():
    """Return valid values for job_title, location, company, etc."""
    try:
        from ml.predict import get_available_options
        return get_available_options()
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Model not trained yet. Run ml/train.py first."
        )
