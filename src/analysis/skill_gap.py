"""
skill_gap.py
-------------
Skill gap analysis: compares user's skills against
the required skills for a target job role.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

_PROCESSED = PROJECT_ROOT / "data" / "processed"


def _load_jobs() -> pd.DataFrame:
    return pd.read_csv(_PROCESSED / "jobs_cleaned.csv")


def _load_job_skills() -> pd.DataFrame:
    return pd.read_csv(_PROCESSED / "job_skills.csv")


# ============================================================
# Skill gap functions
# ============================================================

def get_role_skills(job_title: str, top_n: int = 15) -> pd.DataFrame:
    """
    Return the top N skills required for a given job role,
    with demand count and percentage of postings requiring them.
    """
    jobs = _load_jobs()
    job_skills = _load_job_skills()

    role_jobs = jobs[jobs["job_title"].str.lower() == job_title.strip().lower()]
    if role_jobs.empty:
        return pd.DataFrame(columns=["skill_name", "category", "count", "pct_jobs"])

    total_role_jobs = len(role_jobs)
    role_job_ids = set(role_jobs["job_id"].astype(str))
    role_skills = job_skills[job_skills["job_id"].astype(str).isin(role_job_ids)]

    skill_counts = (
        role_skills
        .groupby(["skill_name", "category"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    skill_counts["pct_jobs"] = (skill_counts["count"] / total_role_jobs * 100).round(1)
    return skill_counts


def skill_gap(user_skills: list[str], target_role: str, top_n: int = 15) -> dict:
    """
    Compare user's skills against the top required skills for target_role.

    Returns:
        {
            "target_role": str,
            "role_skill_count": int,
            "user_match_count": int,
            "match_percentage": float,
            "matched_skills": list[str],
            "missing_skills": list[dict],   # [{skill_name, category, pct_jobs}]
            "role_skills": list[dict],
        }
    """
    role_skills_df = get_role_skills(target_role, top_n)

    if role_skills_df.empty:
        return {
            "target_role": target_role,
            "error": f"No jobs found for role: '{target_role}'",
        }

    # Normalize user skills for comparison
    user_skills_lower = {s.strip().lower() for s in user_skills}

    role_skills_df["has_skill"] = role_skills_df["skill_name"].str.lower().isin(user_skills_lower)

    matched = role_skills_df[role_skills_df["has_skill"]]["skill_name"].tolist()
    missing = role_skills_df[~role_skills_df["has_skill"]].to_dict(orient="records")

    match_pct = round(len(matched) / len(role_skills_df) * 100, 1) if len(role_skills_df) > 0 else 0

    return {
        "target_role": target_role,
        "role_skill_count": len(role_skills_df),
        "user_match_count": len(matched),
        "match_percentage": match_pct,
        "matched_skills": matched,
        "missing_skills": [
            {
                "skill_name": r["skill_name"],
                "category": r["category"],
                "pct_jobs": r["pct_jobs"],
            }
            for r in missing
        ],
        "role_skills": role_skills_df.to_dict(orient="records"),
    }


def available_roles() -> list[str]:
    """Return all unique job titles available for gap analysis."""
    jobs = _load_jobs()
    return sorted(jobs["job_title"].dropna().unique().tolist())


if __name__ == "__main__":
    user = ["Python", "Pandas", "SQL", "PostgreSQL"]
    role = "Data Scientist"

    print(f"Skill Gap Analysis: '{role}'")
    print(f"Your skills: {user}\n")

    result = skill_gap(user, role)
    print(f"Match: {result['match_percentage']}% ({result['user_match_count']}/{result['role_skill_count']})")
    print(f"\nMatched: {result['matched_skills']}")
    print("\nMissing skills:")
    for s in result["missing_skills"]:
        print(f"  [{s['category']}] {s['skill_name']} — in {s['pct_jobs']}% of postings")
