import json
import time
from typing import Optional
from pathlib import Path
import pandas as pd


CACHE_DIR = Path('cache')
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(key: str) -> Path:
    safe = key.replace('/', '_').replace(' ', '_')

    return CACHE_DIR / f"{safe}.json"

def cache_key(prefix: str, identifier: str) -> str:
    return f"{prefix}_{identifier}"



def load_cache(key: str, max_age_seconds: int = 600) -> Optional[pd.DataFrame]:
    p = _cache_path(key)
    if not p.exists():
        return None

    try:
        with p.open('r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception:
        return None

    ts = meta.get('_cached_at', 0)
    if time.time() - ts > max_age_seconds:
        return None

    data = meta.get('data')

    # ⬅️ Convert JSON back to DataFrame
    try:
        df = pd.read_json(data)
        return df
    except Exception:
        return data  # in case it's not DataFrame JSON


def save_cache(key: str, data) -> None:
    p = _cache_path(key)

    # ⬅️ Convert DataFrame to JSON string before saving
    if isinstance(data, pd.DataFrame):
        data = data.to_json()

    meta = {'_cached_at': time.time(), 'data': data}

    with p.open('w', encoding='utf-8') as f:
         json.dump(meta, f)