import pandas as pd


REQUIRED_COLUMNS = [
    "job_title",
    "company",
    "location",
    "description"
]


def validate_columns(df: pd.DataFrame):

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True


def validate_dataframe(df: pd.DataFrame):

    if df.empty:
        raise ValueError("Dataset is empty.")

    validate_columns(df)

    print("Dataset validation passed.")

    return True