from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd

DataFrame = pd.DataFrame

@dataclass(frozen=True)
class SourceConfig:
    """Central config for paths/sheets/headers used by loaders.

    Keep it intentionally small: only paths/sheet names/header rows/globs.
    Column names and mappings live in each domain config.
    """
    customers_masterfile_path: Path | None = None
    customers_sheet: str = "Customer Master File"
    customers_header: int = 2

    #contractlines_masterfile_path: Path | None = None
    #finishing_methods_path: Path | None = None

    #pieces_in_circulation_path: Path | None = None
    #pieces_in_circulation_sep: str = "\t"
    #pieces_in_circulation_encoding: str = "UTF-8"
    #pieces_in_circulation_lineterminator: str = "\r"

    #lockers_wearers_ref_path: Path | None = None
    #lockers_wearers_ref_sep: str = "\t"
    #lockers_wearers_ref_encoding: str = "latin-1"
    #lockers_wearers_ref_lineterminator: str = "\r"

    #active_garments_glob: str | None = None

    #employees_info_path: Path | None = None

    #pcs_lockers_masterfile_path: Path | None = None
    #pcs_lockers_sheet: str = "PcsInCirculation_Lockers"
    #pcs_lockers_skiprows: int = 1

    #product_sizes_path: Path | None = None
    #product_sizes_sheet: str = "v3_sizes"

    #li_product_catalog_path: Path | None = None
    #li_product_catalog_sheet: str = "Product to export"
    #li_product_catalog_header: int = 2

    #li_product_sizes_path: Path | None = None
    #li_product_sizes_sheet: str = "ProductSize Mappings_v3"
