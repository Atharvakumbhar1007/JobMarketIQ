import pandas as pd
from pathlib import Path

from transform import (
    clean_column_names,
    remove_duplicates,
    normalize_job_title,
    normalize_location,
    normalize_work_mode
)


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "jobs.csv"
)

PROCESSED_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "jobs_cleaned.csv"
)

QUALITY_REPORT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "data_quality_report.csv"
)


# ============================================================
# Step 14: Extract
# ============================================================

def extract_jobs():

    print("Loading raw dataset...")

    df = pd.read_csv(RAW_PATH)

    print(f"Extracted {len(df)} job records.")

    return df


# ============================================================
# Step 14: Transform
# ============================================================

def transform_jobs(df):

    print("\nStarting transformation...")

    # Step 6: Clean column names
    df = clean_column_names(df)

    # Step 7: Remove duplicates
    df = remove_duplicates(df)

    # Step 9: Normalize job titles
    if "job_title" in df.columns:

        df["job_title"] = df["job_title"].apply(
            normalize_job_title
        )

    # Step 10: Normalize locations
    if "location" in df.columns:

        df["location"] = df["location"].apply(
            normalize_location
        )

    # Step 13: Normalize work mode
    if "work_mode" in df.columns:

        df["work_mode"] = df["work_mode"].apply(
            normalize_work_mode
        )

    print("Transformation completed.")

    return df


# ============================================================
# Step 15: Save processed data
# ============================================================

def save_processed_data(df):

    PROCESSED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_PATH,
        index=False
    )

    print(
        f"\nSaved {len(df)} records to:"
    )

    print(PROCESSED_PATH)


# ============================================================
# Step 17: Generate data-quality report
# ============================================================

def generate_quality_report(raw_df, final_df):

    raw_rows = len(raw_df)
    final_rows = len(final_df)

    duplicates_removed = raw_rows - final_rows

    report = {
        "raw_rows": raw_rows,
        "final_rows": final_rows,
        "duplicates_removed": duplicates_removed,

        "missing_descriptions": (
            final_df["description"].isna().sum()
            if "description" in final_df.columns
            else 0
        ),

        "missing_salaries": (
            final_df["salary"].isna().sum()
            if "salary" in final_df.columns
            else 0
        ),

        "missing_locations": (
            final_df["location"].isna().sum()
            if "location" in final_df.columns
            else 0
        )
    }

    return report


# ============================================================
# Step 17: Save data-quality report
# ============================================================

def save_quality_report(report):

    QUALITY_REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_df = pd.DataFrame(
        list(report.items()),
        columns=["metric", "value"]
    )

    report_df.to_csv(
        QUALITY_REPORT_PATH,
        index=False
    )

    print("\nQuality report saved to:")
    print(QUALITY_REPORT_PATH)


# ============================================================
# Main ETL Pipeline
# ============================================================

def main():

    print("=" * 60)
    print("JOBMARKETIQ ETL PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Extract
    # --------------------------------------------------------

    print("\n[1] Extracting data...")

    raw_df = extract_jobs()

    print("\nRaw shape:")
    print(raw_df.shape)

    # --------------------------------------------------------
    # 2. Transform
    # --------------------------------------------------------

    print("\n[2] Transforming data...")

    df = transform_jobs(raw_df)

    print("\nProcessed shape:")
    print(df.shape)

    # --------------------------------------------------------
    # 3. Save processed data
    # --------------------------------------------------------

    print("\n[3] Saving processed data...")

    save_processed_data(df)

    # --------------------------------------------------------
    # 4. Generate quality report
    # --------------------------------------------------------

    print("\n[4] Generating data-quality report...")

    report = generate_quality_report(
        raw_df,
        df
    )

    print("\nData Quality Report:")

    for key, value in report.items():
        print(f"{key}: {value}")

    # --------------------------------------------------------
    # 5. Save quality report
    # --------------------------------------------------------

    print("\n[5] Saving quality report...")

    save_quality_report(report)

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    print(f"\nFinal records: {len(df)}")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()