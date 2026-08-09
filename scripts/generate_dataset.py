"""
generate_dataset.py
-------------------
Generates a realistic 5,000-row synthetic Indian tech job market dataset
and saves it to data/raw/jobs.csv
"""

import random
import uuid
import csv
from pathlib import Path
from datetime import date, timedelta

# ============================================================
# Seed for reproducibility
# ============================================================

random.seed(42)

# ============================================================
# Reference data
# ============================================================

LOCATIONS = [
    "Bangalore", "Mumbai", "Hyderabad", "Pune", "Chennai",
    "New Delhi", "Gurugram", "Noida", "Kolkata", "Ahmedabad",
    "Kochi", "Jaipur", "Chandigarh", "Indore", "Nagpur",
]

WORK_MODES = ["remote", "hybrid", "onsite"]
WORK_MODE_WEIGHTS = [0.25, 0.35, 0.40]

EMPLOYMENT_TYPES = ["Full-time", "Part-time", "Contract", "Internship"]
EMPLOYMENT_WEIGHTS = [0.70, 0.05, 0.15, 0.10]

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Infosys", "TCS", "Wipro",
    "HCL Technologies", "Tech Mahindra", "Accenture", "IBM",
    "Cognizant", "Capgemini", "Oracle", "SAP Labs", "Adobe",
    "Flipkart", "Swiggy", "Zomato", "Ola", "Paytm",
    "Razorpay", "Freshworks", "Zoho", "Byju's", "Meesho",
    "PhonePe", "Cred", "Nykaa", "Dunzo", "Urban Company",
    "Mindtree", "Mphasis", "Hexaware", "L&T Infotech", "Persistent",
    "Zensar", "Cyient", "Mastech", "Birlasoft", "NIIT Technologies",
]

# Skills grouped by category
SKILL_CATEGORIES = {
    "languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "Go",
        "Rust", "Kotlin", "Swift", "Scala", "R", "PHP", "Ruby", "C#",
    ],
    "frameworks": [
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django",
        "FastAPI", "Flask", "Spring Boot", "NestJS", "Next.js", "Svelte",
        "Laravel", "Rails", "ASP.NET",
    ],
    "databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Cassandra", "SQLite", "DynamoDB", "Oracle DB", "SQL Server",
        "Neo4j", "InfluxDB", "CockroachDB",
    ],
    "cloud": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Jenkins", "CircleCI", "GitHub Actions",
        "Helm", "Istio", "ArgoCD",
    ],
    "ml": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "Scikit-learn", "Keras", "XGBoost", "LightGBM", "NLP",
        "Computer Vision", "Reinforcement Learning", "MLflow",
        "Hugging Face", "LangChain", "Pandas", "NumPy",
    ],
    "devops": [
        "Git", "Linux", "CI/CD", "Prometheus", "Grafana", "Nginx",
        "Apache Kafka", "RabbitMQ", "Celery", "Airflow",
    ],
    "bi": [
        "Power BI", "Tableau", "Looker", "Data Studio", "Metabase",
        "SQL", "Spark", "Hadoop", "Hive", "Databricks",
    ],
}

ALL_SKILLS = [s for skills in SKILL_CATEGORIES.values() for s in skills]

# Job roles mapped to likely skill pools
JOB_ROLE_SKILLS = {
    "Software Engineer": (["languages", "frameworks", "databases"], 4, 8),
    "Senior Software Engineer": (["languages", "frameworks", "databases", "devops"], 5, 10),
    "Backend Developer": (["languages", "frameworks", "databases", "devops"], 4, 8),
    "Frontend Developer": (["languages", "frameworks"], 4, 7),
    "Full Stack Developer": (["languages", "frameworks", "databases"], 5, 9),
    "Data Engineer": (["languages", "databases", "cloud", "devops", "bi"], 5, 9),
    "Data Scientist": (["languages", "ml", "databases", "bi"], 5, 9),
    "ML Engineer": (["languages", "ml", "cloud", "devops"], 5, 9),
    "DevOps Engineer": (["cloud", "devops", "languages"], 5, 9),
    "Site Reliability Engineer": (["cloud", "devops", "languages"], 5, 8),
    "Cloud Architect": (["cloud", "devops"], 5, 9),
    "Android Developer": (["languages", "frameworks", "databases"], 4, 7),
    "iOS Developer": (["languages", "frameworks", "databases"], 4, 7),
    "Platform Engineer": (["cloud", "devops", "languages", "databases"], 5, 9),
    "QA Engineer": (["languages", "devops"], 3, 6),
    "Data Analyst": (["languages", "bi", "databases"], 4, 7),
    "Business Intelligence Developer": (["bi", "databases", "languages"], 4, 7),
    "Product Data Analyst": (["bi", "databases", "languages"], 3, 6),
    "Security Engineer": (["cloud", "devops", "languages"], 4, 7),
    "Python Developer": (["languages", "frameworks", "databases"], 4, 8),
    "Java Developer": (["languages", "frameworks", "databases"], 4, 8),
    "React Developer": (["frameworks", "languages"], 3, 6),
    "Node.js Developer": (["frameworks", "languages", "databases"], 3, 6),
    "Database Administrator": (["databases", "devops"], 4, 7),
    "Scrum Master": (["devops"], 2, 4),
    "Technical Lead": (["languages", "frameworks", "databases", "cloud"], 6, 11),
    "Engineering Manager": (["languages", "frameworks", "cloud", "devops"], 5, 9),
    "Solutions Architect": (["cloud", "frameworks", "databases", "devops"], 6, 10),
    "Data Platform Engineer": (["databases", "cloud", "languages", "bi"], 5, 9),
    "NLP Engineer": (["languages", "ml", "frameworks"], 4, 8),
}

JOB_TITLES = list(JOB_ROLE_SKILLS.keys())

# Salary ranges by seniority (annual LPA in INR)
SALARY_RANGES = {
    "junior": (3, 8),      # 3-8 LPA
    "mid": (8, 18),        # 8-18 LPA
    "senior": (18, 40),    # 18-40 LPA
    "lead": (35, 70),      # 35-70 LPA
}

SENIORITY_KEYWORDS = {
    "junior": ["Junior", "Associate", "Trainee", "Intern"],
    "senior": ["Senior", "Lead", "Principal", "Staff", "Manager", "Architect", "Director"],
    "lead": ["Engineering Manager", "Solutions Architect", "Technical Lead"],
}

DESCRIPTION_TEMPLATES = [
    "We are looking for a talented {title} to join our {team} team at {company}. "
    "You will be responsible for designing, developing and maintaining scalable systems. "
    "The ideal candidate has strong experience with {skill_list}. "
    "You will work in an agile environment and collaborate with cross-functional teams.",

    "Join {company} as a {title} and help us build world-class products. "
    "This role requires expertise in {skill_list}. "
    "You will be part of a fast-paced {team} team, solving challenging technical problems.",

    "{company} is hiring an experienced {title} to strengthen our engineering team. "
    "Key responsibilities include building robust backend services, optimizing performance, "
    "and contributing to architectural decisions. Must have hands-on experience with {skill_list}.",

    "As a {title} at {company}, you will design and implement scalable {domain} solutions. "
    "We expect proficiency in {skill_list}. You'll work closely with product and design teams "
    "to deliver high-quality features in a collaborative environment.",

    "Exciting opportunity for a {title} at {company}! "
    "We are scaling our platform and need someone with deep expertise in {skill_list}. "
    "You will mentor junior engineers and drive best practices across the {team} team.",
]

TEAMS = ["Engineering", "Platform", "Data", "Product", "Infrastructure",
         "Backend", "Frontend", "Full Stack", "ML", "DevOps", "Analytics"]

DOMAINS = ["data", "cloud", "web", "mobile", "infrastructure", "machine learning",
           "distributed systems", "microservices", "real-time analytics"]


# ============================================================
# Helper functions
# ============================================================

def pick_skills_for_role(title: str) -> list[str]:
    """Pick a realistic set of skills for a given job title."""
    if title not in JOB_ROLE_SKILLS:
        cats, min_s, max_s = (["languages", "frameworks"], 3, 6)
    else:
        cats, min_s, max_s = JOB_ROLE_SKILLS[title]

    pool = []
    for cat in cats:
        pool.extend(SKILL_CATEGORIES.get(cat, []))

    n = random.randint(min_s, max_s)
    return random.sample(pool, min(n, len(pool)))


def get_seniority(title: str) -> str:
    """Determine salary tier based on job title."""
    for kw in SENIORITY_KEYWORDS["lead"]:
        if kw in title:
            return "lead"
    for kw in SENIORITY_KEYWORDS["senior"]:
        if kw in title:
            return "senior"
    for kw in SENIORITY_KEYWORDS["junior"]:
        if kw in title:
            return "junior"
    return "mid"


def generate_salary(seniority: str) -> tuple[int, int]:
    """Generate min/max salary (in LPA * 100000 → stored as annual INR)."""
    lo, hi = SALARY_RANGES[seniority]
    salary_min = round(random.uniform(lo, (lo + hi) / 2), 1)
    salary_max = round(random.uniform((lo + hi) / 2, hi), 1)
    # Convert LPA to INR
    return int(salary_min * 100_000), int(salary_max * 100_000)


def generate_experience(seniority: str) -> tuple[int, int]:
    """Generate min/max years of experience."""
    ranges = {
        "junior": (0, 2),
        "mid": (2, 5),
        "senior": (5, 10),
        "lead": (8, 15),
    }
    lo, hi = ranges[seniority]
    exp_min = random.randint(lo, max(lo, hi - 2))
    exp_max = random.randint(exp_min + 1, hi)
    return exp_min, exp_max


def generate_description(title: str, company: str, skills: list[str]) -> str:
    """Generate a realistic job description."""
    template = random.choice(DESCRIPTION_TEMPLATES)
    skill_list = ", ".join(skills[:6]) if skills else "various technologies"
    return template.format(
        title=title,
        company=company,
        skill_list=skill_list,
        team=random.choice(TEAMS),
        domain=random.choice(DOMAINS),
    )


def random_date(start_days_ago: int = 180) -> str:
    """Generate a random posted date within the last N days."""
    delta = random.randint(0, start_days_ago)
    d = date.today() - timedelta(days=delta)
    return d.isoformat()


# ============================================================
# Main generator
# ============================================================

def generate_dataset(n: int = 5000) -> list[dict]:
    records = []
    for _ in range(n):
        job_id = str(uuid.uuid4())
        title = random.choice(JOB_TITLES)
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        work_mode = random.choices(WORK_MODES, weights=WORK_MODE_WEIGHTS)[0]
        employment_type = random.choices(EMPLOYMENT_TYPES, weights=EMPLOYMENT_WEIGHTS)[0]

        seniority = get_seniority(title)
        salary_min, salary_max = generate_salary(seniority)
        exp_min, exp_max = generate_experience(seniority)

        skills = pick_skills_for_role(title)
        description = generate_description(title, company, skills)
        posted_date = random_date()

        records.append({
            "job_id": job_id,
            "job_title": title,
            "company": company,
            "location": location,
            "work_mode": work_mode,
            "employment_type": employment_type,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "experience_min": exp_min,
            "experience_max": exp_max,
            "description": description,
            "skills": "|".join(skills),   # pipe-separated for easy parsing
            "posted_date": posted_date,
            "remote": work_mode == "remote",
        })

    return records


def save_dataset(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} records to {path}")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"

    print("=" * 60)
    print("JOBMARKETIQ DATASET GENERATOR")
    print("=" * 60)
    print(f"\nGenerating {5000} synthetic job listings...")

    records = generate_dataset(5000)
    save_dataset(records, OUTPUT_PATH)

    # Quick stats
    titles = [r["job_title"] for r in records]
    locations = [r["location"] for r in records]
    modes = [r["work_mode"] for r in records]

    print("\n--- Quick Stats ---")
    print(f"Total records : {len(records)}")
    print(f"Unique titles : {len(set(titles))}")
    print(f"Unique locations: {len(set(locations))}")
    print(f"Remote jobs   : {modes.count('remote')}")
    print(f"Hybrid jobs   : {modes.count('hybrid')}")
    print(f"Onsite jobs   : {modes.count('onsite')}")
    print("\nDone!")
