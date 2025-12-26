# ma-migration (generalized + strict mode + contracts + docs + main notebook)

This package generalizes logic from the `Customers_Breakdown.ipynb` notebook into reusable domain pipelines.

## What’s included
- Domain pipelines under `src/ma_migration/domains/`
- Thin orchestration under `src/ma_migration/pipelines/`
- Strict mode: `strict=True|False` per domain/pipeline
- Data contracts (YAML/JSON) under `contracts/`
- Contract engine under `src/ma_migration/contracts/`
- Markdown docs generator under `docs/generate_docs.py`
- Team-facing main notebook template under `notebooks/main_customers_breakdown.ipynb`

## Quickstart

Install (editable):
```bash
pip install -e .
```

Run pipeline:
```python
from pathlib import Path
from ma_migration.core.types import SourceConfig
from ma_migration.pipelines.customers_breakdown import run_from_sources

cfg = SourceConfig(
    customers_masterfile_path=Path("INPUT/Customers_MasterFile.xlsx"),
    finishing_methods_path=Path("INPUT/FinishingMethods.xlsx"),
    pieces_in_circulation_path=Path("INPUT/PiecesInCirculation.txt"),
    lockers_wearers_ref_path=Path("INPUT/PcsInCirculation_LockersWearers_Ref.txt"),
    active_garments_glob="INPUT/ActiveGarments/*.xlsx",
)

outputs = run_from_sources(cfg, strict=False)
```

Validate MATO output with a contract:
```python
from ma_migration.contracts.loader import load_contract
from ma_migration.contracts.runner import run_contract

contract = load_contract("contracts/mato/customer_master.yaml")
report = run_contract(outputs["customer_master"], contract, strict=False)
print(report.summary())
```

Generate Markdown docs:
```bash
python docs/generate_docs.py
```

## Main notebook adoption
Use `notebooks/main_customers_breakdown.ipynb` as the team’s entry point while the API/UI is developed.
Keep it thin: config → run → validate → review.
