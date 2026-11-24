import os
from collections import defaultdict
from pathlib import Path

import kagglehub
import numpy as np
import pandas as pd

COMPETITION_NAME = "cu-boulder-stat-learning-fall-2026-final-project"

train_path = Path("./data/train.csv")
test_path = Path("./data/test.csv")


DTYPES = defaultdict(
    lambda: np.float64,
    x4="category",
    x5="category",
    x10="category",
    Y="category",
)


def fetch_dataset():
    try:
        _ = pd.read_csv(train_path)
        _ = pd.read_csv(test_path)
    except FileNotFoundError:
        print("data not found.")
        print("loading kaggle API key from `.env`...")
        from dotenv import load_dotenv

        load_dotenv()
        kaggle_api_token = os.getenv("KAGGLE_API_TOKEN")
        assert kaggle_api_token is not None, (
            "no `.env` file found (make sure it's in <PROJECT_ROOT>/code/.env)"
        )

        print("API key loaded.")

        print("downloading `.csv` data files...")
        _ = kagglehub.competition_download(
            COMPETITION_NAME,
            output_dir=Path("./data"),
            force_download=True,
        )

    df_train = pd.read_csv(train_path, index_col="ID", dtype=DTYPES)
    df_test = pd.read_csv(test_path, index_col="ID", dtype=DTYPES)
    print("✅ data loaded!")

    return (df_train, df_test)
