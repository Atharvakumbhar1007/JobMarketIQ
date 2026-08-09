import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def load_jobs(df):

    df.to_sql(
        "jobs_raw",
        engine,
        if_exists="replace",
        index=False
    )

    print(
        f"Loaded {len(df)} records into PostgreSQL."
    )