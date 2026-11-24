import os
import subprocess
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

COMPETITION_NAME = "cu-boulder-stat-learning-fall-2026-final-project"
COMPETITION_URL = f"https://www.kaggle.com/competitions/{COMPETITION_NAME}"

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
        r = subprocess.run(
            [
                "kaggle",
                "competitions",
                "download",
                "-c",
                COMPETITION_NAME,
                "-p",
                "data",
            ],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0, "❌ download failed"
        print("download complete. unzipping files...")
        print("unzipping files...")
        with zipfile.ZipFile(
            Path("./data/cu-boulder-stat-learning-fall-2026-final-project.zip")
        ) as zf:
            zf.extractall(Path("./data"))
        print("unzip complete.")

    df_train = pd.read_csv(train_path, index_col="ID", dtype=DTYPES)
    df_test = pd.read_csv(test_path, index_col="ID", dtype=DTYPES)
    print("✅ data loaded!")

    return (df_train, df_test)
