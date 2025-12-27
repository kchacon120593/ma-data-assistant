from __future__ import annotations
import pandas as pd

#from .config import CustomersConfig
from . import transforms as T
from . import validations as V
from ma_migration.core.contracts import DomainContract
from ma_migration.core.result import DomainResult


def prepare_customers(
    cus: pd.DataFrame,
    *,
    contract: DomainContract,
    strict: bool = True
    ) -> DomainResult: 
    res = DomainResult()
    
    """Prepare customer data."""    
    
    # ----------- Transformations -----------
    cus = T.clean_object_columns(cus)
    
    customer_id_col = contract.columns.Source_Customer_ID
    cus = T.clean_customer_id(cus, customer_id_col)
    
    invoicing_cluster_col = contract.columns.Invoicing_Cluster
    cus = T.normalize_invoicing_cluster(cus, invoicing_cluster_col)

    invoicing_coupling_code_col = contract.columns.Invoicing_Coupling_Code
    cus = T.replace_invoicing_coupling_codes(cus, invoicing_coupling_code_col,
                                             mapping={"no coupling":"0001","manual invoice":"0090"}) # Replace as needed


    cus = T.assign_default_coupling(cus, invoicing_coupling_code_col, default="0001")

    try:
        V.validate_invoicing_coupling(cus, invoicing_coupling_code_col, list(invoicing_coupling_code_col))
    except ValueError as e:
        res.errors.append(str(e))
        
    vat_col = contract.columns.NIP_VAT_Number
    cus = T.drop_customers_without_vat(cus, vat_col)

    cus_inv = cus.copy()
    cus_lw = cus.copy()


    #-------------- UPDATE WHEN WORKING WITH DEPT ID ----------------
    
    #cus["DepartmentID/BranchID in HeliosDb_OG"] = cus[cfg.dept_id_col].copy(deep=True)
    #cus = T.normalize_department_id_when_single_missing(cus, cfg.customer_id_col, cfg.dept_id_col)



  #  cus = T.add_mato_columns(cus, vat_col=vat_col, dept_id_col=cfg.dept_id_col) add dept_d_id_col in the contract


    cus = T.add_invoicing_customer_id(
        cus,
        vat_col=vat_col,
        coupling_col=invoicing_coupling_code_col,
        cluster_col=invoicing_cluster_col
    )

    contract_type_raw_col = contract.columns.Contract_Type
    cus = T.explode_contract_type_both(cus, contract_type_raw_col)
    
    contract_valid_values = contract.columns.Contract_Type.valid_values

    try:
        V.validate_contract_types(cus, contract_type_raw_col, list(contract_valid_values))
    except ValueError as e:
        res.errors.append(str(e))

    res.data = {
        "customers_base": cus,
        "customers_for_invoicing": cus_inv,
        "customers_for_lockers_wearers": cus_lw
    }

    res.raise_if_strict(strict)
    return res
