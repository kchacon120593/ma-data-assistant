from __future__ import annotations
import numpy as np
import pandas as pd

from ma_migration.core.validation import assert_allowed_values

def validate_invoicing_coupling(cus: pd.DataFrame, coupling_col: str, valid_values: list[str]) -> None:
    assert_allowed_values(cus[coupling_col], valid_values, label=coupling_col)

def validate_contract_types(expanded: pd.DataFrame, contract_type_col: str, valid_values: list[str]) -> None:
    assert_allowed_values(expanded[contract_type_col], valid_values, label=contract_type_col)
