from __future__ import annotations
from pathlib import Path
import pandas as pd

def export_excel(outputs: dict[str, pd.DataFrame], out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, df in outputs.items():
        if isinstance(df, pd.DataFrame):
            df.to_excel(out_dir / f"{name}.xlsx", index=False)
