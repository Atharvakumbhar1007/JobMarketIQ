import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw dataset
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"


# Load dataset
def load_data(path):
    return pd.read_csv(path)


# Step 5: Generate data quality report
def generate_quality_report(df):

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": df.duplicated().sum(),
        "missing_values": df.isnull().sum().sum()
    }

    return report


# Step 6: Clean column names
def clean_column_names(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


if __name__ == "__main__":

    df = load_data(DATA_PATH)

    # Basic inspection
    print("Dataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values by Column:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # Generate quality report BEFORE transformation
    report_before = generate_quality_report(df)

    print("\nData Quality Report BEFORE Cleaning:")

    for key, value in report_before.items():
        print(f"{key}: {value}")

    # Step 6: Clean column names
    print("\nBefore Column Cleaning:")
    print(df.columns.tolist())

    df = clean_column_names(df)

    print("\nAfter Column Cleaning:")
    print(df.columns.tolist())

    # Generate quality report AFTER transformation
    report_after = generate_quality_report(df)

    print("\nData Quality Report AFTER Cleaning:")

    for key, value in report_after.items():
        print(f"{key}: {value}")