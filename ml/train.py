"""
train.py
---------
Train a salary prediction model using RandomForestRegressor.
Saves model artifact to ml/models/salary_model.pkl
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "jobs_cleaned.csv"
JOB_SKILLS_PATH = PROJECT_ROOT / "data" / "processed" / "job_skills.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "salary_model.pkl"


# ============================================================
# Feature engineering
# ============================================================

def build_features(jobs_df: pd.DataFrame, job_skills_df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features for salary prediction."""

    df = jobs_df.copy()

    # Target variable: average salary
    df["salary_avg"] = (
        pd.to_numeric(df["salary_min"], errors="coerce") +
        pd.to_numeric(df["salary_max"], errors="coerce")
    ) / 2

    # Drop rows with missing salary
    df = df.dropna(subset=["salary_avg"])

    # Skill count per job
    skill_counts = (
        job_skills_df
        .groupby("job_id")
        .size()
        .reset_index(name="skill_count")
    )
    df = df.merge(skill_counts, on="job_id", how="left")
    df["skill_count"] = df["skill_count"].fillna(0).astype(int)

    # Remote flag
    df["is_remote"] = (df["work_mode"] == "remote").astype(int)
    df["is_hybrid"] = (df["work_mode"] == "hybrid").astype(int)

    # Experience features
    df["experience_min"] = pd.to_numeric(df["experience_min"], errors="coerce").fillna(0)
    df["experience_max"] = pd.to_numeric(df["experience_max"], errors="coerce").fillna(0)
    df["experience_avg"] = (df["experience_min"] + df["experience_max"]) / 2

    # Encode categorical variables
    le_title = LabelEncoder()
    le_location = LabelEncoder()
    le_company = LabelEncoder()
    le_emp_type = LabelEncoder()

    df["job_title_enc"] = le_title.fit_transform(df["job_title"].fillna("Unknown"))
    df["location_enc"] = le_location.fit_transform(df["location"].fillna("Unknown"))
    df["company_enc"] = le_company.fit_transform(df["company"].fillna("Unknown"))
    df["emp_type_enc"] = le_emp_type.fit_transform(df["employment_type"].fillna("Unknown"))

    return df, {
        "le_title": le_title,
        "le_location": le_location,
        "le_company": le_company,
        "le_emp_type": le_emp_type,
    }


FEATURE_COLS = [
    "job_title_enc",
    "location_enc",
    "company_enc",
    "emp_type_enc",
    "experience_min",
    "experience_max",
    "experience_avg",
    "skill_count",
    "is_remote",
    "is_hybrid",
]


# ============================================================
# Training
# ============================================================

def train():
    print("=" * 60)
    print("JOBMARKETIQ SALARY PREDICTION MODEL")
    print("=" * 60)

    # Load data
    print("\n[1] Loading data...")
    jobs_df = pd.read_csv(PROCESSED_PATH)
    job_skills_df = pd.read_csv(JOB_SKILLS_PATH)
    print(f"  Jobs: {len(jobs_df)} | Skills: {len(job_skills_df)}")

    # Feature engineering
    print("\n[2] Engineering features...")
    df, encoders = build_features(jobs_df, job_skills_df)
    print(f"  Training samples: {len(df)}")

    X = df[FEATURE_COLS].values
    y = df["salary_avg"].values

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    print("\n[3] Training RandomForestRegressor...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_leaf=5,
        n_jobs=-1,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Evaluate
    print("\n[4] Evaluating...")
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"  R2 Score  : {r2:.4f}")
    print(f"  MAE       : INR {mae:,.0f}")
    print(f"  MAE (LPA) : {mae / 100_000:.2f} LPA")


    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")
    print(f"\n  5-Fold CV R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")


    # Feature importance
    importances = pd.DataFrame({
        "feature": FEATURE_COLS,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    print("\n  Feature importances:")
    for _, row in importances.iterrows():
        bar = "=" * int(row["importance"] * 40)
        print(f"  {row['feature']:<20} {bar} {row['importance']:.4f}")


    # Save model artifact
    print("\n[5] Saving model...")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "encoders": encoders,
        "feature_cols": FEATURE_COLS,
        "metrics": {"r2": r2, "mae": mae},
        "label_values": {
            "job_titles": encoders["le_title"].classes_.tolist(),
            "locations": encoders["le_location"].classes_.tolist(),
            "companies": encoders["le_company"].classes_.tolist(),
            "emp_types": encoders["le_emp_type"].classes_.tolist(),
        },
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifact, f)

    print(f"  Model saved to: {MODEL_PATH}")
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    train()
