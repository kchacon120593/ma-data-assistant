from __future__ import annotations
import pandas as pd

def append_sequential_suffix_for_duplicates(series: pd.Series, *, sep: str = "_") -> pd.Series:
    """
    Appends a sequential suffix to duplicate entries in a pandas Series.
    """
    s = series.astype(str)
    counts = s.groupby(s).cumcount() + 1
    out = (s + sep) + counts.astype(str)
    out = out.str.replace(rf"{sep}1$", "", regex=True)
    return out