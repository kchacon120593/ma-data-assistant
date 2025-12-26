from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CustomersConfig:
    vat_col: str = "NIP / VAT Number"
    customer_id_col: str = "CustomerID in HeliosDb"
    dept_id_col: str = "DepartmentID/BranchID in HeliosDb"
    dept_name_col: str = "Department/Branch Name"
    contract_type_raw_col: str = "Contract type (rental / laundry/ Both)"
    invoicing_coupling_col: str = "Invoicing Coupling Code"
    invoicing_cluster_col: str = "Invoicing Cluster"

    # business enums (kept as in notebook)
    valid_invoicing_coupling: tuple[str, ...] = ("0001","0090","0091","0092","0093","0094")
    valid_contract_types: tuple[str, ...] = ("Rental","Laundry")
