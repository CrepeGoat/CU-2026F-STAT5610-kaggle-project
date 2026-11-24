import os
from collections import defaultdict
from pathlib import Path

import kagglehub
import numpy as np
import pandas as pd

CWD = Path(os.path.dirname(os.path.realpath(__file__)))
COMPETITION_NAME = "cu-boulder-stat-learning-fall-2026-final-project"


def fetch_dataset():
    train_path = CWD / "data" / "train.csv"
    test_path = CWD / "data" / "test.csv"
    dtypes = defaultdict(
        lambda: np.float64,
        x4="category",
        x5="category",
        x10="category",
        Y="category",
    )

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
            output_dir=CWD / "data",
            force_download=True,
        )

    df_train = pd.read_csv(train_path, index_col="ID", dtype=dtypes)
    df_test = pd.read_csv(test_path, index_col="ID", dtype=dtypes)
    print("✅ data loaded!")

    return (df_train, df_test)
