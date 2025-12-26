from __future__ import annotations
import pandas as pd

from .config import CustomersConfig
from . import transforms as T
from . import validations as V
from ma_migration.core.result import DomainResult

def prepare_customers(
    cus: pd.DataFrame,
    *,
    cfg: CustomersConfig = CustomersConfig(),
    strict: bool = True
) -> DomainResult:
    res = DomainResult()

    cus = T.clean_object_columns(cus)
    cus = T.add_clean_customer_id(cus, cfg.customer_id_col)
    cus = T.normalize_invoicing_cluster(cus, cfg.invoicing_cluster_col)

    cus = T.replace_invoicing_coupling_codes(
        cus, cfg.invoicing_coupling_col,
        mapping={"no coupling":"0001","manual invoice":"0090"}
    )
    cus = T.assign_default_coupling(cus, cfg.invoicing_coupling_col, default="0001")

    try:
        V.validate_invoicing_coupling(cus, cfg.invoicing_coupling_col, list(cfg.valid_invoicing_coupling))
    except ValueError as e:
        res.errors.append(str(e))

    cus = T.drop_customers_without_vat(cus, cfg.vat_col)

    cus_inv = cus.copy()
    cus_lw = cus.copy()

    cus["DepartmentID/BranchID in HeliosDb_OG"] = cus[cfg.dept_id_col].copy(deep=True)
    cus = T.normalize_department_id_when_single_missing(cus, cfg.customer_id_col, cfg.dept_id_col)

    cus = T.add_mato_columns(cus, vat_col=cfg.vat_col, dept_id_col=cfg.dept_id_col)
    cus = T.add_invoicing_customer_id(
        cus,
        vat_col=cfg.vat_col,
        coupling_col=cfg.invoicing_coupling_col,
        cluster_col=cfg.invoicing_cluster_col
    )

    expanded = T.explode_contract_type_both(cus, cfg.contract_type_raw_col)

    try:
        V.validate_contract_types(expanded, "ContractType", list(cfg.valid_contract_types))
    except ValueError as e:
        res.errors.append(str(e))

    res.data = {
        "customers_base": cus,
        "customers_for_invoicing": cus_inv,
        "customers_for_lockers_wearers": cus_lw,
        "customers_expanded": expanded,
    }

    res.raise_if_strict(strict)
    return res
