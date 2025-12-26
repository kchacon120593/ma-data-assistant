from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CustomerMergeConfig:
    vat_col: str = "NIP / VAT Number"
    dept_name_col: str = "Department/Branch Name"
    finishing_method_col: str = "Finishing Method"
    contract_type_id_col: str = "ContractTypeID"
    coupling_col: str = "Invoicing Coupling Code"
    cluster_col: str = "Invoicing Cluster"

    # defaults (as in notebook)
    default_text: str = "XXXXXX"
    default_amount_employees: str = "100-249"
    default_payment_terms: str = "30"
    default_contract_type: str = "Rental"
    default_title: str = "Production Manager"
    default_phone: int = 0
    default_email: str = "XXX@XX.XX"
    default_city: str = "Sierpc"
    default_address: str = "XXXXXX"
    default_invoicing_method: str = "Mail/Paper"
    default_price_model: str = "Price without locker"
