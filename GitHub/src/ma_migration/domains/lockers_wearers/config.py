from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LockersWearersConfig:
    vat_col: str = "NIP / VAT Number"
    barcode_col: str = "Barcode"
    customer_id_locwea_col: str = "CustomerID"
    customer_id_cus_col: str = "CustomerID in HeliosDb"
    contract_type_col: str = "Contract type (rental / laundry/ Both)"
    finishing_method_col: str = "Finishing Method"
