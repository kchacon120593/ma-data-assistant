from __future__ import annotations
import pandas as pd

def append_sequential_suffix_for_duplicates(series: pd.Series, *, sep: str = "_") -> pd.Series:
    """Notebook pattern:
    series = series.groupby(series).cumcount().add(1).astype(str).radd(series + '_')
    then remove '_1' for first occurrences.
    """
    s = series.astype(str)
    counts = s.groupby(s).cumcount() + 1
    out = (s + sep) + counts.astype(str)
    out = out.str.replace(rf"{sep}1$", "", regex=True)
    return out

def drop_duplicates(df: pd.DataFrame, *, subset=None) -> pd.DataFrame:
    return df.drop_duplicates(subset=subset)
