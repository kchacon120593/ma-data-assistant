from __future__ import annotations
import numpy as np
import pandas as pd

from ma_migration.core.strings import strip_object_columns, numeric_id_to_str, zfill_str

def clean_object_columns(cus: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from all object/string columns in the customers DataFrame."""
    return strip_object_columns(cus)

def clean_customer_id(cus: pd.DataFrame, customer_id_col: str) -> pd.DataFrame:
    """Ensure customer ID column is string type and stripped of whitespace."""
    cus = cus.copy()
    cus[customer_id_col] = cus[customer_id_col].astype(str).str.strip()
    return cus

def normalize_invoicing_cluster(cus: pd.DataFrame, cluster_col: str) -> pd.DataFrame:
    """Ensure invoicing cluster codes are zero-padded to length 4."""
    cus = cus.copy()
    cus[cluster_col] = zfill_str(cus[cluster_col], 4)
    return cus

def replace_invoicing_coupling_codes(cus: pd.DataFrame, coupling_col: str, *, mapping: dict[str,str]) -> pd.DataFrame:
    """Replace invoicing coupling codes according to the provided mapping."""
    cus = cus.copy()
    cus[coupling_col] = cus[coupling_col].replace(mapping)
    return cus

def assign_default_coupling(cus: pd.DataFrame, coupling_col: str, default: str="0001") -> pd.DataFrame:
    """Assign a default invoicing coupling code where missing."""
    cus = cus.copy()
    cus[coupling_col].replace(np.nan, default, inplace=True)
    return cus

def drop_customers_without_vat(cus: pd.DataFrame, vat_col: str) -> pd.DataFrame:
    """Drop customers that do not have a VAT number."""
    return cus[cus[vat_col].notna()].copy()


def add_invoicing_customer_id(cus: pd.DataFrame, *, vat_col: str, coupling_col: str, cluster_col: str, out_col: str="Invoicing_CustomerID") -> pd.DataFrame:
    """Create invoicing customer ID based on VAT, coupling code, and cluster."""
    cus = cus.copy()
    cus[out_col] = numeric_id_to_str(cus[vat_col]) + "_" + cus[coupling_col].astype(str) + "_" + cus[cluster_col].astype(str)
    # notebook: coupling code 0001 means no coupling => no separate invoicing customer
    mask = cus[coupling_col].astype(str) == "0001"
    cus.loc[mask, out_col] = np.nan
    return cus

def normalize_department_id_when_single_missing(cus: pd.DataFrame, customer_id_col: str, dept_id_col: str) -> pd.DataFrame:
    """If a customer has only one unique department and the dept ID is missing, fill it with the customer ID."""
    cus = cus.copy()
    dept_counts = cus.groupby(customer_id_col)[dept_id_col].nunique(dropna=False)
    cus["UniqueDeptCount"] = cus[customer_id_col].map(dept_counts)
    mask = cus[dept_id_col].isna() & (cus["UniqueDeptCount"] == 1)
    cus.loc[mask, dept_id_col] = cus.loc[mask, customer_id_col]
    return cus

def add_mato_columns(cus: pd.DataFrame, *, vat_col: str, dept_id_col: str) -> pd.DataFrame:
    """Add MATO-specific columns based on VAT and Department ID."""
    cus = cus.copy()
   # cus["MATO_DeliveryCustomerCode"] = cus[dept_id_col] #Review logic for MATO DeliveryCustomerCode
    cus["MATO_CustomerID"] = cus[vat_col]
    return cus

def explode_contract_type_both(cus: pd.DataFrame, contract_type_raw_col: str) -> pd.DataFrame:
    """Explode rows where Contract Type is 'Both' into two rows: 'Rental' and 'Laundry'."""
    col_name = contract_type_raw_col
    
    cus = cus.copy()
    cus = (
        cus.assign(ContractType=cus[contract_type_raw_col].apply(lambda x: ["Rental","Laundry"] if x=="Both" else [x]))
        .explode("ContractType", ignore_index=True)
    )
    cus["ContractTypeID"] = cus["ContractType"].astype(str).str[0].str.upper()
    
    cus.drop(columns=[contract_type_raw_col], inplace=True)
    
    cus.rename(columns={"ContractType": col_name}, inplace=True)
    
    return cus
