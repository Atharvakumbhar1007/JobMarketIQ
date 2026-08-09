import pandas as pd
from pathlib import Path


# ============================================================
# Project configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"

__all__ = [
    "clean_column_names",
    "remove_duplicates",
    "normalize_job_title",
    "normalize_location",
    "normalize_work_mode",
    "load_data",
    "LOCATION_ALIASES",
]


# ============================================================
# Load dataset
# ============================================================

def load_data(path):
    return pd.read_csv(path)


# ============================================================
# Step 6: Clean column names
# ============================================================

def clean_column_names(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


# ============================================================
# Step 7: Remove duplicate jobs
# ============================================================

def remove_duplicates(df):

    rows_before = len(df)

    if "job_id" in df.columns:
        df = df.drop_duplicates(subset=["job_id"])
    else:
        df = df.drop_duplicates()

    rows_after = len(df)

    print(f"Rows before duplicate removal: {rows_before}")
    print(f"Rows after duplicate removal: {rows_after}")
    print(f"Duplicates removed: {rows_before - rows_after}")

    return df


# ============================================================
# Step 9: Normalize job titles
# ============================================================

def normalize_job_title(value):

    if pd.isna(value):
        return ""

    return " ".join(
        str(value).strip().split()
    ).title()


# ============================================================
# Step 10: Normalize locations
# ============================================================

LOCATION_ALIASES = {
    "bombay": "Mumbai",
    "mumbai, mh": "Mumbai",
    "mumbai, maharashtra": "Mumbai",
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "delhi": "New Delhi",
    "new delhi": "New Delhi",
    "ncr": "New Delhi",
    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",
    "noida": "Noida",
    "chennai": "Chennai",
    "madras": "Chennai",
    "hyderabad": "Hyderabad",
    "pune": "Pune",
    "kolkata": "Kolkata",
    "calcutta": "Kolkata",
}


def normalize_location(value):

    if pd.isna(value):
        return ""

    location = str(value).strip().lower()

    return LOCATION_ALIASES.get(
        location,
        str(value).strip()
    )


# ============================================================
# Step 13: Normalize work mode
# ============================================================

def normalize_work_mode(value):

    if pd.isna(value):
        return "unknown"

    value = str(value).lower().strip()

    if value in ["remote", "work from home", "wfh", "fully remote"]:
        return "remote"

    if value in ["hybrid", "partial remote"]:
        return "hybrid"

    if value in ["onsite", "on-site", "office", "in-office", "on site"]:
        return "onsite"

    return "unknown"


# ============================================================
# Script entry point
# ============================================================

if __name__ == "__main__":

    df = load_data(DATA_PATH)

    print("=" * 60)
    print("JOBMARKETIQ DATA TRANSFORMATION")
    print("=" * 60)

    print("\nOriginal columns:")
    print(df.columns.tolist())

    print("\nOriginal shape:")
    print(df.shape)

    df = clean_column_names(df)

    print("\nCleaned columns:")
    print(df.columns.tolist())

    print("\nDuplicate Removal:")
    df = remove_duplicates(df)

    if "job_title" in df.columns:
        print("\nJob titles BEFORE normalization:")
        print(df["job_title"].head(10).to_list())
        df["job_title"] = df["job_title"].apply(normalize_job_title)
        print("\nJob titles AFTER normalization:")
        print(df["job_title"].head(10).to_list())

    if "location" in df.columns:
        print("\nLocations BEFORE normalization:")
        print(df["location"].head(10).to_list())
        df["location"] = df["location"].apply(normalize_location)
        print("\nLocations AFTER normalization:")
        print(df["location"].head(10).to_list())

    if "work_mode" in df.columns:
        print("\nWork modes BEFORE normalization:")
        print(df["work_mode"].head(20).to_list())
        df["work_mode"] = df["work_mode"].apply(normalize_work_mode)
        print("\nWork modes AFTER normalization:")
        print(df["work_mode"].head(20).to_list())
        print("\nWork mode distribution:")
        print(df["work_mode"].value_counts(dropna=False))

    print("\n" + "=" * 60)
    print("FINAL DATASET INFORMATION")
    print("=" * 60)
    print("\nFinal shape:")
    print(df.shape)
    print("\nFinal columns:")
    print(df.columns.tolist())