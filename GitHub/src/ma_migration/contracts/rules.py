from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict
import pandas as pd

@dataclass(frozen=True)
class Rule:
    id: str
    severity: str
    type: str
    column: str | None = None
    columns: list[str] | None = None
    values: list[Any] | None = None
    equals: Any | None = None
    pattern: str | None = None
    max_length: int | None = None

def _mask_not_null(df: pd.DataFrame, col: str) -> pd.Series:
    return df[col].isna()

def _mask_length_not_equals(df: pd.DataFrame, col: str, expected: int) -> pd.Series:
    return df[col].astype(str).str.len() != int(expected)

def _mask_not_allowed(df: pd.DataFrame, col: str, allowed: list[Any]) -> pd.Series:
    return ~df[col].astype(str).isin([str(v) for v in allowed])

def _mask_regex_mismatch(df: pd.DataFrame, col: str, pattern: str) -> pd.Series:
    return ~df[col].astype(str).str.match(pattern, na=False)

def _mask_max_length_exceeded(df: pd.DataFrame, col: str, max_len: int) -> pd.Series:
    return df[col].astype(str).str.len() > int(max_len)

def _mask_duplicates(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    return df.duplicated(subset=cols, keep=False)

RULE_DISPATCH: Dict[str, Callable[[pd.DataFrame, Rule], pd.Series]] = {
    "not_null": lambda df, r: _mask_not_null(df, r.column or ""),
    "length_equals": lambda df, r: _mask_length_not_equals(df, r.column or "", int(r.equals)),
    "allowed_values": lambda df, r: _mask_not_allowed(df, r.column or "", r.values or []),
    "regex": lambda df, r: _mask_regex_mismatch(df, r.column or "", r.pattern or ""),
    "max_length": lambda df, r: _mask_max_length_exceeded(df, r.column or "", int(r.max_length)),
    "unique": lambda df, r: _mask_duplicates(df, r.columns or ([r.column] if r.column else [])),
}
