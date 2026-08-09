import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw dataset
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"


# Load dataset
def load_data(path):
    return pd.read_csv(path)


# Step 7: Remove duplicate jobs
def remove_duplicates(df):

    if "job_id" in df.columns:
        df = df.drop_duplicates(subset=["job_id"])
    else:
        df = df.drop_duplicates()

    return df


if __name__ == "__main__":

    df = load_data(DATA_PATH)

    print("Before removing duplicates:")
    print("Rows:", len(df))

    df = remove_duplicates(df)

    print("\nAfter removing duplicates:")
    print("Rows:", len(df))