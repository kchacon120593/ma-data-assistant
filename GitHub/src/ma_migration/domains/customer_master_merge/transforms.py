from __future__ import annotations
import pandas as pd

from ma_migration.core.dedupe import append_sequential_suffix_for_duplicates
from ma_migration.core.dates import format_date

def merge_customers_finishing(customers_expanded: pd.DataFrame, fm_uq: pd.DataFrame, *, vat_col: str) -> pd.DataFrame:
    return customers_expanded.merge(fm_uq, how="left", left_on=vat_col, right_on=vat_col)

def fill_defaults(cus_fm: pd.DataFrame, defaults: dict[str, object]) -> pd.DataFrame:
    df = cus_fm.copy()
    for col, val in defaults.items():
        if col in df.columns:
            df[col].fillna(val, inplace=True)
    return df

def replace_values(df: pd.DataFrame, col: str, replacements: dict) -> pd.DataFrame:
    df = df.copy()
    if col in df.columns:
        df[col].replace(replacements, inplace=True)
    return df

def build_delivery_and_codes(df: pd.DataFrame, *,
                             dept_name_col: str,
                             finishing_method_col: str,
                             contract_type_id_col: str,
                             contract_number_col: str = "Contract number",
                             mato_delivery_code_col: str = "MATO_DeliveryCustomerCode") -> pd.DataFrame:
    """Notebook intent: append finishing method + contract type ID to delivery-related identifiers."""
    out = df.copy()
    suffix = out[finishing_method_col].astype(str) + "_" + out[contract_type_id_col].astype(str)
    if dept_name_col in out.columns:
        out[dept_name_col] = out[dept_name_col].astype(str) + "_" + suffix
    if mato_delivery_code_col in out.columns:
        out[mato_delivery_code_col] = out[mato_delivery_code_col].astype(str) + "_" + suffix
    if contract_number_col in out.columns:
        out[contract_number_col] = out[contract_number_col].map('{:.0f}'.format).astype(str).str.strip() + "_" + suffix
    return out

def ensure_unique_identifiers(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = append_sequential_suffix_for_duplicates(out[c])
    return out

def rename_address_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Matches notebook rename mapping."""
    mapping = {
        "Postcode": "DeliveryAddress_Postcode",
        "City / Town": "DeliveryAddress_City/Town",
        "Address": "Delivery Address",
        "Postcode.1": "InvoiceAddress_Postcode",
        "City / Town.1": "InvoiceAddress_City/Town",
        "Address.1": "Invoice Address",
    }
    return df.rename(columns={k:v for k,v in mapping.items() if k in df.columns})

def convert_contract_dates(df: pd.DataFrame,
                           signed_col: str="Contract signed (e.g. 31.8.2022)",
                           term_col: str="Contract term (e.g. until 31.8.2025)") -> pd.DataFrame:
    out = df.copy()
    if signed_col in out.columns:
        out[signed_col] = out[signed_col].apply(format_date)
    if term_col in out.columns:
        out[term_col] = out[term_col].apply(format_date)
    return out

def add_uat_prefix(df: pd.DataFrame, cols: list[str], prefix: str="UAT_") -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = prefix + out[c].astype(str)
    return out
