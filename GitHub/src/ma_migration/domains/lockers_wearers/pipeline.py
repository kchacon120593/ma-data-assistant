from __future__ import annotations
import os
import pandas as pd
import numpy as np
import warnings

from ma_migration.core.validation import assert_no_duplicates, warn_if_any_null
from ma_migration.core.strings import numeric_id_to_str
from .config import LockersWearersConfig
from .schema import LOCWEA_TRANS_REF

def load_active_garments_from_excels(files: list[str | os.PathLike]) -> pd.DataFrame:
    schema = ['NIP / VAT Number', 'Barcode', 'Invoiced', 'Source_File']
    dfs = []
    for f in files:
        df = pd.read_excel(f)
        df = df.iloc[:, :3]
        df.columns = schema[:3]
        df['Source_File'] = os.path.basename(str(f))
        dfs.append(df)
    active = pd.concat(dfs, ignore_index=True)
    active['NIP / VAT Number'] = active['NIP / VAT Number'].map('{:.0f}'.format).str.strip()
    active['Invoiced'] = active['Invoiced'].astype(str).str.strip().str.lower()
    return active

def validate_active_garments(active: pd.DataFrame) -> None:
    valid_invoiced = {'yes','no'}
    messages = []
    for source, g in active.groupby('Source_File'):
        vat_len = g['NIP / VAT Number'].astype(str).str.len()
        invalid_vat = g[vat_len != 10]
        if not invalid_vat.empty:
            messages.append(
                f"❌ {source}: VAT numbers with length != 10\n" +
                invalid_vat[['NIP / VAT Number']].drop_duplicates().to_string(index=False)
            )
        invalid_inv = g[~g['Invoiced'].isin(valid_invoiced)]
        if not invalid_inv.empty:
            messages.append(
                f"❌ {source}: Invoiced values not in {{yes,no}}\n" +
                invalid_inv[['Invoiced']].drop_duplicates().to_string(index=False)
            )
    if messages:
        raise ValueError("\n****** DATA CHECK *****\n\n" + "\n\n".join(messages))

def prepare_lockers_and_wearers(
    locwea: pd.DataFrame,
    locwea_ref: pd.DataFrame,
    customers_for_lockers_wearers: pd.DataFrame,
    customers_contract_types: pd.DataFrame,
    active_garments: pd.DataFrame,
    *,
    cfg: LockersWearersConfig = LockersWearersConfig(),
) -> pd.DataFrame:
    """Generalized lockers & wearers preparation.

    This mirrors notebook logic at a functional level:
    - Keep only customers in master file
    - Split rental vs wash-only (based on contract type = Laundry)
    - Filter rental garments using ActiveGarments files (VAT+Barcode)
    - Join wash-only back, flag isRental
    - Add lockers/wearers reference columns
    - Add finishing method / dept ids / mato columns / formatting (as available)
    """
    # Keep only customers in master file
    cus_unique = customers_for_lockers_wearers[[cfg.customer_id_cus_col, 'Contract number', cfg.vat_col, 'Customer name']].drop_duplicates()
    locwea = locwea.merge(cus_unique, how='inner', left_on=cfg.customer_id_locwea_col, right_on=cfg.customer_id_cus_col).drop(columns=[cfg.customer_id_cus_col])

    # Split wash-only customers
    ct = customers_contract_types[[cfg.vat_col, cfg.contract_type_col]].drop_duplicates()
    wash_vats = ct.loc[ct[cfg.contract_type_col] == 'Laundry', cfg.vat_col]
    wash_mask = locwea[cfg.vat_col].isin(wash_vats)
    locwea_wash = locwea[wash_mask].copy()
    locwea_rental = locwea[~wash_mask].copy()

    # Filter rental garments using active garments list
    locwea_rental = locwea_rental.merge(active_garments, how='inner',
                                        left_on=[cfg.vat_col, cfg.barcode_col],
                                        right_on=[cfg.vat_col, cfg.barcode_col])
    locwea_rental['isRental'] = 1
    locwea_all = pd.concat([locwea_rental, locwea_wash], axis=0, ignore_index=True)
    locwea_all['isRental'] = locwea_all['isRental'].fillna(0)

    # Duplicate barcode validation (notebook raises)
    assert_no_duplicates(locwea_all, cfg.barcode_col, label="Lockers/Wearers")

    # Add lockers/wearers reference info
    ref = locwea_ref.rename(columns=LOCWEA_TRANS_REF).drop_duplicates()
    assert_no_duplicates(ref, cfg.barcode_col, label="Lockers/Wearers Reference")
    locwea_all = locwea_all.merge(ref, how='left', on=cfg.barcode_col, suffixes=("","_Ref"))

    # Warn if missing department id from reference (notebook warns)
    if 'DepartmentID_Ref' in locwea_all.columns:
        warn_if_any_null(locwea_all, 'DepartmentID_Ref', label="Lockers/Wearers")

    # Basic formatting: ensure barcode is string
    locwea_all[cfg.barcode_col] = locwea_all[cfg.barcode_col].astype(str).str.strip()

    return locwea_all
