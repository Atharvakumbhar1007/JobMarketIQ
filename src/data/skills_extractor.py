"""
skills_extractor.py
--------------------
Keyword-based NLP skill extraction from job descriptions.
Produces data/processed/job_skills.csv
"""

import re
import csv
import pandas as pd
from pathlib import Path

# ============================================================
# Skill dictionary
# ============================================================

SKILL_CATEGORIES = {
    "Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "Go",
        "Rust", "Kotlin", "Swift", "Scala", "R", "PHP", "Ruby", "C#",
        "Bash", "Shell", "Perl", "MATLAB", "Groovy",
    ],
    "Frameworks": [
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django",
        "FastAPI", "Flask", "Spring Boot", "NestJS", "Next.js", "Svelte",
        "Laravel", "Rails", "ASP.NET", "Gatsby", "Nuxt.js", "Fastify",
        "Strapi", "GraphQL",
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Cassandra", "SQLite", "DynamoDB", "Oracle DB", "SQL Server",
        "Neo4j", "InfluxDB", "CockroachDB", "Firestore", "Supabase",
        "Snowflake", "BigQuery", "Redshift",
    ],
    "Cloud": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Jenkins", "CircleCI", "GitHub Actions",
        "Helm", "Istio", "ArgoCD", "CloudFormation", "Pulumi",
        "Lambda", "ECS", "EKS", "S3", "EC2",
    ],
    "ML & AI": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "Scikit-learn", "Keras", "XGBoost", "LightGBM", "NLP",
        "Computer Vision", "Reinforcement Learning", "MLflow",
        "Hugging Face", "LangChain", "Pandas", "NumPy",
        "Feature Engineering", "A/B Testing",
    ],
    "DevOps": [
        "Git", "Linux", "CI/CD", "Prometheus", "Grafana", "Nginx",
        "Apache Kafka", "RabbitMQ", "Celery", "Airflow",
        "Datadog", "New Relic", "Splunk", "ELK Stack",
    ],
    "BI & Analytics": [
        "Power BI", "Tableau", "Looker", "Data Studio", "Metabase",
        "SQL", "Spark", "Hadoop", "Hive", "Databricks",
        "dbt", "Fivetran", "Stitch",
    ],
}

# Build flat lookup: lowercase_name → (canonical_name, category)
_SKILL_LOOKUP: dict[str, tuple[str, str]] = {}
for category, skills in SKILL_CATEGORIES.items():
    for skill in skills:
        _SKILL_LOOKUP[skill.lower()] = (skill, category)

# Build a compiled regex pattern for efficient multi-skill matching
# Sort by length desc so longer matches (e.g. "Spring Boot") beat shorter ("Spring")
_PATTERNS = sorted(_SKILL_LOOKUP.keys(), key=len, reverse=True)
_REGEX = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in _PATTERNS) + r")\b",
    re.IGNORECASE,
)


# ============================================================
# Extraction function
# ============================================================

def extract_skills(text: str) -> list[str]:
    """Extract canonical skill names from free text."""
    if not text or not isinstance(text, str):
        return []
    matches = _REGEX.findall(text)
    seen = set()
    result = []
    for m in matches:
        canonical, _ = _SKILL_LOOKUP[m.lower()]
        if canonical not in seen:
            seen.add(canonical)
            result.append(canonical)
    return result


def extract_skills_with_categories(text: str) -> list[dict]:
    """Extract skills with their categories from free text."""
    if not text or not isinstance(text, str):
        return []
    matches = _REGEX.findall(text)
    seen = set()
    result = []
    for m in matches:
        canonical, category = _SKILL_LOOKUP[m.lower()]
        if canonical not in seen:
            seen.add(canonical)
            result.append({"skill": canonical, "category": category})
    return result


# ============================================================
# Batch processing
# ============================================================

def process_jobs_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add an 'extracted_skills' column to the dataframe.
    If a 'skills' column exists (pipe-separated), use it directly;
    otherwise extract from 'description'.
    """
    if "skills" in df.columns:
        # Skills already provided as pipe-separated string
        df["extracted_skills"] = df["skills"].apply(
            lambda s: [x.strip() for x in str(s).split("|") if x.strip()]
            if pd.notna(s) else []
        )
    elif "description" in df.columns:
        df["extracted_skills"] = df["description"].apply(extract_skills)
    else:
        df["extracted_skills"] = [[] for _ in range(len(df))]

    return df


def build_job_skills_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Explode the extracted_skills column into a job_id × skill table.
    """
    records = []
    id_col = "job_id" if "job_id" in df.columns else df.index.name or "index"

    for _, row in df.iterrows():
        job_id = row.get("job_id", row.name)
        for skill in row.get("extracted_skills", []):
            _, category = _SKILL_LOOKUP.get(skill.lower(), (skill, "Other"))
            records.append({
                "job_id": job_id,
                "skill_name": skill,
                "category": category,
            })
    return pd.DataFrame(records)


def build_skills_catalog(job_skills_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a deduplicated skills catalog with category and demand count.
    """
    catalog = (
        job_skills_df
        .groupby(["skill_name", "category"])
        .size()
        .reset_index(name="demand_count")
        .sort_values("demand_count", ascending=False)
        .reset_index(drop=True)
    )
    catalog["skill_id"] = range(1, len(catalog) + 1)
    return catalog[["skill_id", "skill_name", "category", "demand_count"]]


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    RAW_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"
    PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

    print("=" * 60)
    print("JOBMARKETIQ SKILL EXTRACTION")
    print("=" * 60)

    df = pd.read_csv(RAW_PATH)
    print(f"\nLoaded {len(df)} job records.")

    df = process_jobs_dataframe(df)

    # Build job_skills join table
    job_skills_df = build_job_skills_table(df)
    print(f"Extracted {len(job_skills_df)} skill mentions across all jobs.")

    # Build skills catalog
    skills_catalog = build_skills_catalog(job_skills_df)
    print(f"Unique skills found: {len(skills_catalog)}")

    # Save outputs
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    job_skills_df.to_csv(PROCESSED_PATH / "job_skills.csv", index=False)
    skills_catalog.to_csv(PROCESSED_PATH / "skills.csv", index=False)

    print("\nTop 15 most demanded skills:")
    print(skills_catalog.head(15).to_string(index=False))

    print("\nSaved to:")
    print(f"  {PROCESSED_PATH / 'job_skills.csv'}")
    print(f"  {PROCESSED_PATH / 'skills.csv'}")
    print("\nDone!")
