import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_df_csv(df: pd.DataFrame, name: str) -> Path:
    p = DATA_DIR / f"{name}.csv"
    df.to_csv(p, index=False)
    return p
