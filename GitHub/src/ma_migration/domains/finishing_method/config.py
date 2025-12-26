from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FinishingMethodConfig:
    finishing_method_col_raw: str = "FinishingMethod_FinishingMethod"
    finishing_method_col: str = "Finishing Method"
    customer_id_col: str = "ID Kontrahenta"
    item_type_id_col: str = "ID Asortymentu Egzemplarza"
    valid_values: tuple[str, ...] = ("310","100","300","STD")
