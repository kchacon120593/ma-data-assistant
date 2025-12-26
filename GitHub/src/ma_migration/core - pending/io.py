from __future__ import annotations
from pathlib import Path


import glob
import pandas as pd

def read_excel(path: str | Path, *, sheet_name: str | int | None = 0, header: int | None = 0, skiprows: int | None = None) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name, header=header, skiprows=skiprows)

def read_csv(path: str | Path, *, sep: str = "\t", encoding: str = "UTF-8", lineterminator: str = "\n") -> pd.DataFrame:
    return pd.read_csv(path, sep=sep, encoding=encoding, lineterminator=lineterminator)

def list_many_excels(pattern: str) -> list[Path]:
    return [Path(p) for p in glob.glob(pattern)]
