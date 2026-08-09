"""
seed.py
-------
Seeds the SQLite database from processed CSV files.
Run after pipeline.py has produced the processed data.
"""

import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from datetime import date
from sqlalchemy.exc import IntegrityError

from src.database.db import create_all_tables, SessionLocal
from src.database.models import Location, Job, Skill, JobSkill


# ============================================================
# Paths
# ============================================================

PROCESSED = PROJECT_ROOT / "data" / "processed"
RAW = PROJECT_ROOT / "data" / "raw"


# ============================================================
# Seed locations
# ============================================================

def seed_locations(session, df: pd.DataFrame) -> dict[str, int]:
    """Insert unique cities and return city → location_id map."""
    city_map: dict[str, int] = {}
    cities = df["location"].dropna().unique()

    for city in cities:
        existing = session.query(Location).filter_by(city=str(city)).first()
        if existing:
            city_map[str(city)] = existing.location_id
        else:
            loc = Location(city=str(city), country="India")
            session.add(loc)
            session.flush()
            city_map[str(city)] = loc.location_id

    session.commit()
    print(f"  Seeded {len(city_map)} locations.")
    return city_map


# ============================================================
# Seed skills
# ============================================================

def seed_skills(session, skills_df: pd.DataFrame) -> dict[str, int]:
    """Insert skills catalog and return skill_name → skill_id map."""
    skill_map: dict[str, int] = {}

    for _, row in skills_df.iterrows():
        existing = session.query(Skill).filter_by(skill_name=row["skill_name"]).first()
        if existing:
            skill_map[row["skill_name"]] = existing.skill_id
        else:
            skill = Skill(
                skill_name=str(row["skill_name"]),
                category=str(row.get("category", "Other")),
                demand_count=int(row.get("demand_count", 0)),
            )
            session.add(skill)
            session.flush()
            skill_map[row["skill_name"]] = skill.skill_id

    session.commit()
    print(f"  Seeded {len(skill_map)} skills.")
    return skill_map


# ============================================================
# Seed jobs
# ============================================================

def seed_jobs(session, jobs_df: pd.DataFrame, city_map: dict[str, int]) -> int:
    """Insert job records. Returns number inserted."""
    count = 0
    for _, row in jobs_df.iterrows():
        existing = session.query(Job).filter_by(job_id=str(row["job_id"])).first()
        if existing:
            continue

        location_id = city_map.get(str(row.get("location", "")))

        # Parse posted_date safely
        try:
            posted = date.fromisoformat(str(row["posted_date"]))
        except Exception:
            posted = None

        job = Job(
            job_id=str(row["job_id"]),
            job_title=str(row.get("job_title", "")),
            company=str(row.get("company", "")),
            location_id=location_id,
            salary_min=float(row["salary_min"]) if pd.notna(row.get("salary_min")) else None,
            salary_max=float(row["salary_max"]) if pd.notna(row.get("salary_max")) else None,
            experience_min=int(row["experience_min"]) if pd.notna(row.get("experience_min")) else None,
            experience_max=int(row["experience_max"]) if pd.notna(row.get("experience_max")) else None,
            employment_type=str(row.get("employment_type", "")),
            work_mode=str(row.get("work_mode", "unknown")),
            remote=bool(row.get("remote", False)),
            description=str(row.get("description", "")),
            posted_date=posted,
        )
        session.add(job)
        count += 1

    session.commit()
    print(f"  Seeded {count} jobs.")
    return count


# ============================================================
# Seed job_skills
# ============================================================

def seed_job_skills(session, job_skills_df: pd.DataFrame, skill_map: dict[str, int]) -> int:
    """Insert job-skill associations."""
    count = 0
    for _, row in job_skills_df.iterrows():
        skill_id = skill_map.get(str(row["skill_name"]))
        if skill_id is None:
            continue
        existing = session.query(JobSkill).filter_by(
            job_id=str(row["job_id"]), skill_id=skill_id
        ).first()
        if existing:
            continue
        try:
            js = JobSkill(job_id=str(row["job_id"]), skill_id=skill_id)
            session.add(js)
            count += 1
        except IntegrityError:
            session.rollback()

    session.commit()
    print(f"  Seeded {count} job-skill associations.")
    return count


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 60)
    print("JOBMARKETIQ DATABASE SEEDER")
    print("=" * 60)

    # Run skill extraction first to generate processed files
    from src.data.skills_extractor import (
        process_jobs_dataframe,
        build_job_skills_table,
        build_skills_catalog,
    )

    # Load raw jobs
    jobs_path = RAW / "jobs.csv"
    if not jobs_path.exists():
        print(f"ERROR: {jobs_path} not found. Run scripts/generate_dataset.py first.")
        sys.exit(1)

    print("\n[1] Running skill extraction...")
    jobs_df = pd.read_csv(jobs_path)
    jobs_df = process_jobs_dataframe(jobs_df)
    job_skills_df = build_job_skills_table(jobs_df)
    skills_catalog = build_skills_catalog(job_skills_df)

    # Save processed files
    PROCESSED.mkdir(parents=True, exist_ok=True)
    jobs_df.drop(columns=["extracted_skills"], errors="ignore").to_csv(
        PROCESSED / "jobs_cleaned.csv", index=False
    )
    job_skills_df.to_csv(PROCESSED / "job_skills.csv", index=False)
    skills_catalog.to_csv(PROCESSED / "skills.csv", index=False)
    print(f"  Processed data saved to {PROCESSED}/")

    # Create tables
    print("\n[2] Creating database tables...")
    create_all_tables()

    session = SessionLocal()
    try:
        print("\n[3] Seeding locations...")
        city_map = seed_locations(session, jobs_df)

        print("\n[4] Seeding skills...")
        skill_map = seed_skills(session, skills_catalog)

        print("\n[5] Seeding jobs...")
        seed_jobs(session, jobs_df, city_map)

        print("\n[6] Seeding job-skill associations...")
        seed_job_skills(session, job_skills_df, skill_map)

    finally:
        session.close()

    print("\n" + "=" * 60)
    print("DATABASE SEEDING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
