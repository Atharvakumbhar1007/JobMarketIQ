import pandas as pd


DATA_PATH = "data/raw/jobs.csv"


def load_data(path):
    return pd.read_csv(path)


def inspect_data(df):
    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())


if __name__ == "__main__":
    df = load_data(DATA_PATH)
    inspect_data(df)