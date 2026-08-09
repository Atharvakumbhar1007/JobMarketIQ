from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw/jobs.csv")


def extract_jobs():
    """
    Extract raw job data from CSV.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Extracted {len(df)} job records.")

    return df


if __name__ == "__main__":
    df = extract_jobs()

    print(df.head())
    print(df.shape)