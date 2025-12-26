from __future__ import annotations
import pandas as pd

def prepare_product_catalog(li_product_catalog: pd.DataFrame) -> pd.DataFrame:
    return li_product_catalog.copy()

def prepare_product_size_mappings(li_product_sizes: pd.DataFrame) -> pd.DataFrame:
    return li_product_sizes.copy()
