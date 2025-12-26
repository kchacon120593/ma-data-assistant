from __future__ import annotations
import pandas as pd

from ma_migration.core.validation import assert_allowed_values
from ma_migration.core.strings import numeric_id_to_str
from ma_migration.core.dates import format_date
from .config import InvoicingCustomersConfig

def prepare_invoicing_customers(cus_inv: pd.DataFrame, *, cfg: InvoicingCustomersConfig = InvoicingCustomersConfig()) -> dict[str,pd.DataFrame]:
    # notebook selects subset of columns (keep the same behavior by not forcing a schema here)
    cus_inv = cus_inv.drop_duplicates().copy()

    # validate coupling codes
    assert_allowed_values(cus_inv[cfg.coupling_col].astype(str), list(cfg.valid_coupling), label=cfg.coupling_col)

    # remove no-coupling cases
    cus_inv = cus_inv[cus_inv[cfg.coupling_col].astype(str) != "0001"].copy()

    # rename address columns if present
    rename_map = {
        "Postcode.1": "InvoiceAddress_Postcode",
        "City / Town.1": "InvoiceAddress_City/Town",
        "Address.1": "Invoice Address",
    }
    cus_inv = cus_inv.rename(columns={k:v for k,v in rename_map.items() if k in cus_inv.columns})

    # build invoicing customer id
    cus_inv["Invoicing_CustomerID"] = numeric_id_to_str(cus_inv[cfg.vat_col]) + "_" + cus_inv[cfg.coupling_col].astype(str) + "_" + cus_inv[cfg.cluster_col].astype(str)

    # convert dates
    for c in ["Contract signed (e.g. 31.8.2022)","Contract term (e.g. until 31.8.2025)"]:
        if c in cus_inv.columns:
            cus_inv[c] = cus_inv[c].apply(format_date)

    # uat
    cus_inv_uat = cus_inv.copy()
    if cfg.customer_name_col in cus_inv_uat.columns:
        cus_inv_uat[cfg.customer_name_col] = "UAT_" + cus_inv_uat[cfg.customer_name_col].astype(str)

    return {"invoicing_customers": cus_inv, "invoicing_customers_uat": cus_inv_uat}
