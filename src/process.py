import pandas as pd
from typing import List, Dict
from .utils import parse_date

REQUIRED_COLS = [
    "sport","tournament_name","level","start_date","end_date",
    "official_url","streaming","image","summary"
]

def to_dataframe(items: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(items)
    # ensure columns
    for c in REQUIRED_COLS:
        if c not in df.columns:
            df[c] = ""
    # normalize dates
    df["start_date"] = df["start_date"].map(parse_date)
    df["end_date"] = df["end_date"].map(parse_date)
    # sort by start date
    if "start_date" in df.columns:
        df = df.sort_values(by=["start_date","sport","level"], na_position="last").reset_index(drop=True)
    return df[REQUIRED_COLS]
