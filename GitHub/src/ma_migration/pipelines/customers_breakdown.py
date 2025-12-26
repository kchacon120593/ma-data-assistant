from __future__ import annotations
import pandas as pd
from ma_migration.core.types import SourceConfig
from ma_migration.core.io import read_excel, read_csv, read_many_excels

from ma_migration.domains.customers.pipeline import prepare_customers
from ma_migration.domains.finishing_method.pipeline import prepare_finishing_methods
from ma_migration.domains.customer_master_merge.pipeline import prepare_customer_master_file
from ma_migration.domains.invoicing_customers.pipeline import prepare_invoicing_customers
from ma_migration.domains.lockers_wearers.pipeline import load_active_garments_from_excels, validate_active_garments, prepare_lockers_and_wearers
from ma_migration.domains.product_features.pipeline import prepare_product_catalog, prepare_product_size_mappings
from ma_migration.domains.products_sizes.pipeline import prepare_product_sizes

def run_from_dataframes(
    *,
    customers_master: pd.DataFrame,
    finishing_methods: pd.DataFrame,
    pieces_in_circulation: pd.DataFrame,
    lockers_wearers_ref: pd.DataFrame,
    active_garments: pd.DataFrame,
    product_sizes: pd.DataFrame | None = None,
    li_product_catalog: pd.DataFrame | None = None,
    li_product_sizes: pd.DataFrame | None = None,
    strict: bool = True,
) -> dict[str, pd.DataFrame]:
    """Run the full Customers Breakdown pipeline using in-memory DataFrames.

    This module is intentionally thin: it orchestrates domain pipelines
    in the same conceptual order as the notebook.
    """
    cust_res = prepare_customers(customers_master, strict=strict)
    customers_expanded = cust_res.data["customers_expanded"]

    fm_uq = prepare_finishing_methods(finishing_methods, customers_expanded)
    cm_out = prepare_customer_master_file(customers_expanded, fm_uq)
    inv_out = prepare_invoicing_customers(cust_res.data["customers_for_invoicing"])

    lw_df = prepare_lockers_and_wearers(
        pieces_in_circulation,
        lockers_wearers_ref,
        cust_res.data["customers_for_lockers_wearers"],
        customers_master,
        active_garments,
    )

    outputs: dict[str, pd.DataFrame] = {}
    outputs.update(cm_out)
    outputs.update(inv_out)
    outputs["lockers_wearers"] = lw_df

    if product_sizes is not None:
        outputs["product_sizes"] = prepare_product_sizes(product_sizes)
    if li_product_catalog is not None:
        outputs["li_product_catalog"] = prepare_product_catalog(li_product_catalog)
    if li_product_sizes is not None:
        outputs["li_product_sizes"] = prepare_product_size_mappings(li_product_sizes)

    return outputs

def run_from_sources(cfg: SourceConfig, *, strict: bool = True) -> dict[str, pd.DataFrame]:
    """Run pipeline from configured sources (paths/sheets/headers)."""
    if cfg.customers_masterfile_path is None:
        raise ValueError("customers_masterfile_path required")
    if cfg.finishing_methods_path is None:
        raise ValueError("finishing_methods_path required")
    if cfg.pieces_in_circulation_path is None:
        raise ValueError("pieces_in_circulation_path required")
    if cfg.lockers_wearers_ref_path is None:
        raise ValueError("lockers_wearers_ref_path required")
    if cfg.active_garments_glob is None:
        raise ValueError("active_garments_glob required")

    customers_master = read_excel(cfg.customers_masterfile_path, sheet_name=cfg.customers_sheet, header=cfg.customers_header)
    finishing_methods = read_excel(cfg.finishing_methods_path)
    pieces = read_csv(cfg.pieces_in_circulation_path, sep=cfg.pieces_in_circulation_sep, encoding=cfg.pieces_in_circulation_encoding, lineterminator=cfg.pieces_in_circulation_lineterminator)
    ref = read_csv(cfg.lockers_wearers_ref_path, sep=cfg.lockers_wearers_ref_sep, encoding=cfg.lockers_wearers_ref_encoding, lineterminator=cfg.lockers_wearers_ref_lineterminator)

    files = read_many_excels(cfg.active_garments_glob)
    active = load_active_garments_from_excels(files)
    validate_active_garments(active)

    product_sizes = read_excel(cfg.product_sizes_path, sheet_name=cfg.product_sizes_sheet) if cfg.product_sizes_path else None
    li_product_catalog = read_excel(cfg.li_product_catalog_path, sheet_name=cfg.li_product_catalog_sheet, header=cfg.li_product_catalog_header) if cfg.li_product_catalog_path else None
    li_product_sizes = read_excel(cfg.li_product_sizes_path, sheet_name=cfg.li_product_sizes_sheet) if cfg.li_product_sizes_path else None

    return run_from_dataframes(
        customers_master=customers_master,
        finishing_methods=finishing_methods,
        pieces_in_circulation=pieces,
        lockers_wearers_ref=ref,
        active_garments=active,
        product_sizes=product_sizes,
        li_product_catalog=li_product_catalog,
        li_product_sizes=li_product_sizes,
        strict=strict,
    )
