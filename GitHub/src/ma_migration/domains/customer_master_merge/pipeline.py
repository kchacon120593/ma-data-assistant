from __future__ import annotations
import pandas as pd
import numpy as np
import warnings

from ma_migration.core.validation import warn_invalid_values
from .config import CustomerMergeConfig
from . import transforms as T

def prepare_customer_master_file(customers_expanded: pd.DataFrame, fm_uq: pd.DataFrame, *, cfg: CustomerMergeConfig = CustomerMergeConfig()) -> dict[str,pd.DataFrame]:
    cus_fm = T.merge_customers_finishing(customers_expanded, fm_uq, vat_col=cfg.vat_col)

    # warning validation for invalid finishing methods (as notebook uses warnings, not errors)
    valid_fm = {"310","100","300","STD"}
    fm_val = cus_fm[cfg.finishing_method_col]
    mask = ~fm_val.astype(str).isin(valid_fm)
    warn_invalid_values(
        cus_fm,
        mask,
        header="⚠️ Invalid Finishing Methods",
        cols=["CustomerID in HeliosDb", cfg.vat_col, "Customer name", cfg.finishing_method_col],
    )

    # fill defaults (only for columns that exist)
    defaults = {
        cfg.dept_name_col: cfg.default_text,
        "AmountOfEmployee": cfg.default_amount_employees,
        "PaymentTerms": cfg.default_payment_terms,
        "Contract type (rental / laundry/ Both)": cfg.default_contract_type,
        "Name of contact person": cfg.default_text,
        "Title (e.g. Procurement manager)": cfg.default_title,
        "Phone/mobile number": cfg.default_phone,
        "Email address": cfg.default_email,
        "Postcode": 0,
        "City / Town": cfg.default_city,
        "Address": cfg.default_address,
        "Postcode.1": 0,
        "City / Town.1": cfg.default_city,
        "Address.1": cfg.default_address,
        "Invoicing mehtod": cfg.default_invoicing_method,
        "Price model": cfg.default_price_model,
        "Industry Category": "Transport equipment manufacturing",
    }
    cus_fm = T.fill_defaults(cus_fm, defaults)
    # extra replacements for dept name
    cus_fm = T.replace_values(cus_fm, cfg.dept_name_col, {"NULL":cfg.default_text, "nan":cfg.default_text, "":cfg.default_text, " ":cfg.default_text, "0":cfg.default_text, 0:cfg.default_text})

    # derive delivery/customer codes (mechanical pattern)
    cus_fm = T.build_delivery_and_codes(cus_fm,
        dept_name_col=cfg.dept_name_col,
        finishing_method_col=cfg.finishing_method_col,
        contract_type_id_col=cfg.contract_type_id_col,
        contract_number_col="Contract number",
        mato_delivery_code_col="MATO_DeliveryCustomerCode",
    )

    # drop helper column from finishing method join if present
    if "ID Kontrahenta" in cus_fm.columns:
        cus_fm = cus_fm.drop(columns=["ID Kontrahenta"])

    # rename address columns
    cus_fm = T.rename_address_columns(cus_fm)

    # ensure uniqueness of identifiers
    cus_fm = T.ensure_unique_identifiers(cus_fm, cols=["Contract number", "MATO_DeliveryCustomerCode"])

    # convert dates
    cus_fm = T.convert_contract_dates(cus_fm)

    # UAT prefixed copy
    cus_fm_uat = T.add_uat_prefix(cus_fm, cols=["Customer name", cfg.dept_name_col])

    # rename Delivery Customer column as in notebook
    cus_fm_uat = cus_fm_uat.rename(columns={cfg.dept_name_col:"Delivery Customer Name"})
    cus_fm = cus_fm.rename(columns={cfg.dept_name_col:"Delivery Customer Name"})

    return {"customer_master": cus_fm, "customer_master_uat": cus_fm_uat}
