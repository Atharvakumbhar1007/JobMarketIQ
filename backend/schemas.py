"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel
from typing import Optional
from datetime import date


# ============================================================
# Jobs
# ============================================================

class JobOut(BaseModel):
    job_id: str
    job_title: str
    company: Optional[str]
    location: Optional[str]
    work_mode: Optional[str]
    employment_type: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    experience_min: Optional[int]
    experience_max: Optional[int]
    remote: Optional[bool]
    posted_date: Optional[str]
    description: Optional[str]


class JobListOut(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[JobOut]


# ============================================================
# Skills
# ============================================================

class SkillOut(BaseModel):
    skill_name: str
    category: str
    demand_count: int


class SkillGapRequest(BaseModel):
    user_skills: list[str]
    target_role: str
    top_n: int = 15


class SkillGapOut(BaseModel):
    target_role: str
    role_skill_count: int
    user_match_count: int
    match_percentage: float
    matched_skills: list[str]
    missing_skills: list[dict]


# ============================================================
# Salary
# ============================================================

class SalaryByRoleOut(BaseModel):
    job_title: str
    salary_min: float
    salary_max: float
    salary_avg: float
    job_count: int


class SalaryByLocationOut(BaseModel):
    location: str
    salary_avg: float
    salary_min: float
    salary_max: float
    job_count: int


class SalaryPredictRequest(BaseModel):
    job_title: str
    location: str
    company: str = "Unknown"
    employment_type: str = "Full-time"
    experience_min: int = 0
    experience_max: int = 2
    skill_count: int = 5
    work_mode: str = "hybrid"


class SalaryPredictOut(BaseModel):
    predicted_salary: int
    predicted_salary_lpa: float
    salary_range_min: int
    salary_range_max: int
    salary_range_min_lpa: float
    salary_range_max_lpa: float


# ============================================================
# Analytics
# ============================================================

class OverviewStats(BaseModel):
    total_jobs: int
    total_companies: int
    total_locations: int
    remote_jobs: int
    avg_salary: int
    avg_salary_lpa: float


class LocationStat(BaseModel):
    location: str
    job_count: int


class WorkModeStat(BaseModel):
    work_mode: str
    count: int
    percentage: float
