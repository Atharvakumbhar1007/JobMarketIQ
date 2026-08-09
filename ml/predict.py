"""
predict.py
-----------
Load trained salary prediction model and predict salary
for given job parameters.
"""

import sys
import pickle
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "salary_model.pkl"

_artifact = None


def _load_artifact():
    global _artifact
    if _artifact is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Run `python ml/train.py` first."
            )
        with open(MODEL_PATH, "rb") as f:
            _artifact = pickle.load(f)
    return _artifact


def _safe_encode(encoder, value: str, default: str = "Unknown") -> int:
    """Encode a label, falling back to the most common class if unseen."""
    classes = list(encoder.classes_)
    if value in classes:
        return encoder.transform([value])[0]
    if default in classes:
        return encoder.transform([default])[0]
    return 0  # fallback


def predict_salary(
    job_title: str,
    location: str,
    company: str = "Unknown",
    employment_type: str = "Full-time",
    experience_min: int = 0,
    experience_max: int = 2,
    skill_count: int = 5,
    work_mode: str = "hybrid",
) -> dict:
    """
    Predict salary for a given job configuration.

    Returns:
        {
            "predicted_salary": int,         # INR
            "predicted_salary_lpa": float,   # Lakhs per annum
            "salary_range_min": int,
            "salary_range_max": int,
        }
    """
    artifact = _load_artifact()
    model = artifact["model"]
    encoders = artifact["encoders"]

    experience_avg = (experience_min + experience_max) / 2
    is_remote = 1 if work_mode == "remote" else 0
    is_hybrid = 1 if work_mode == "hybrid" else 0

    features = np.array([[
        _safe_encode(encoders["le_title"], job_title),
        _safe_encode(encoders["le_location"], location),
        _safe_encode(encoders["le_company"], company),
        _safe_encode(encoders["le_emp_type"], employment_type),
        experience_min,
        experience_max,
        experience_avg,
        skill_count,
        is_remote,
        is_hybrid,
    ]])

    predicted = model.predict(features)[0]

    # Estimate range as ±15%
    range_min = int(predicted * 0.85)
    range_max = int(predicted * 1.15)

    return {
        "predicted_salary": int(predicted),
        "predicted_salary_lpa": round(predicted / 100_000, 2),
        "salary_range_min": range_min,
        "salary_range_max": range_max,
        "salary_range_min_lpa": round(range_min / 100_000, 2),
        "salary_range_max_lpa": round(range_max / 100_000, 2),
    }


def get_available_options() -> dict:
    """Return valid values for each categorical field."""
    artifact = _load_artifact()
    return artifact.get("label_values", {})


if __name__ == "__main__":
    result = predict_salary(
        job_title="Data Scientist",
        location="Bangalore",
        employment_type="Full-time",
        experience_min=3,
        experience_max=6,
        skill_count=8,
        work_mode="hybrid",
    )

    print("Salary Prediction Result:")
    for k, v in result.items():
        print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v}")
