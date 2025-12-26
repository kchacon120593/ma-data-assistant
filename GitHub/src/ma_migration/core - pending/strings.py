from __future__ import annotations
import pandas as pd
import numpy as np

def strip_object_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strips leading and trailing whitespace from all object-type columns in a DataFrame."""
    df = df.copy()
    obj_cols = df.select_dtypes(include="object").columns
    if len(obj_cols) > 0:
        df[obj_cols] = df[obj_cols].apply(lambda s: s.astype(str).str.strip())
    return df

def zfill_str(series: pd.Series, width: int) -> pd.Series:
    """Zero-fill a string series to a specified width."""
    return series.astype(str).str.zfill(width)

def numeric_id_to_str(series: pd.Series) -> pd.Series:
    """Converts a numeric ID series to string, removing any decimal places and stripping whitespace."""
    return series.map('{:.0f}'.format).astype(str).str.strip()

def coerce_numeric_keep_nan(series: pd.Series) -> pd.Series:
    """Converts a series to numeric, coercing errors to NaN."""
    return series.apply(lambda x: pd.to_numeric(x, errors='coerce'))
