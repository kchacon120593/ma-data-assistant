from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class InvoicingCustomersConfig:
    vat_col: str = "NIP / VAT Number"
    coupling_col: str = "Invoicing Coupling Code"
    cluster_col: str = "Invoicing Cluster"
    customer_name_col: str = "Customer name"
    valid_coupling: tuple[str, ...] = ("0001","0090","0091","0092","0093","0094")
