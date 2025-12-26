from __future__ import annotations
import warnings
import numpy as np
import pandas as pd

def assert_allowed_values(series: pd.Series, allowed: list[str], *, label: str, strict: bool = True):
    """Asserts that all values in a series are among the allowed values."""
    array = series.astype(str).unique()
    if np.isin(array, allowed).all():
        return
    invalid = array[~np.isin(array, allowed)]
    msg = f"Invalid values in {label}: {invalid}"
    if strict:
        raise ValueError(msg)
    warnings.simplefilter("always", UserWarning)
    warnings.warn(msg, UserWarning)

def assert_no_duplicates(df: pd.DataFrame, col: str, *, label: str, strict: bool = True):
    """Asserts that there are no duplicate values in a specified column of a DataFrame."""
    dups = df[col][df[col].duplicated()].unique()
    if len(dups) != 0:
        msg = f"{label}: duplicated values in {col}: {dups[:10]}{'...' if len(dups)>10 else ''}"
        if strict:
            raise ValueError(msg)
        warnings.simplefilter("always", UserWarning)
        warnings.warn(msg, UserWarning)

def warn_if_any_null(df: pd.DataFrame, col: str, *, label: str, strict: bool = False):
    nulls = int(df[col].isna().sum())
    if nulls:
        msg = f"{label}: {nulls} rows have NULL in {col}"
        if strict:
            raise ValueError(msg)
        warnings.simplefilter("always", UserWarning)
        warnings.warn(msg, UserWarning)
