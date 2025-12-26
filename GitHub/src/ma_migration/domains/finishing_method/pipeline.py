from __future__ import annotations
import pandas as pd

from ma_migration.core.validation import assert_allowed_values
from .config import FinishingMethodConfig

def prepare_finishing_methods(fm: pd.DataFrame, customers_expanded: pd.DataFrame, *, cfg: FinishingMethodConfig = FinishingMethodConfig()) -> pd.DataFrame:
    # validate allowed finishing methods
    assert_allowed_values(fm[cfg.finishing_method_col_raw].astype(str), list(cfg.valid_values), label=cfg.finishing_method_col_raw)

    # validate uniqueness per Customer-Product (must not have >1)
    mask = fm.groupby([cfg.customer_id_col, cfg.item_type_id_col])[cfg.finishing_method_col_raw].transform("nunique") > 1
    if mask.any():
        raise ValueError("More than one Finishing Method per Customer-Product combination")

    fm = fm.rename(columns={cfg.finishing_method_col_raw: cfg.finishing_method_col}).copy()
    fm_uq = fm[[cfg.customer_id_col, cfg.finishing_method_col]].drop_duplicates()

    # add VAT Number from customers master file (expanded customers contains VAT)
    vat = customers_expanded[["CustomerID in HeliosDb", "NIP / VAT Number"]].drop_duplicates()
    fm_uq = fm_uq.merge(vat, how="left", left_on=cfg.customer_id_col, right_on="CustomerID in HeliosDb")
    fm_uq = fm_uq.drop(columns=["CustomerID in HeliosDb"])
    return fm_uq
