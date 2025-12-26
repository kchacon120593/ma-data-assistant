from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd

@dataclass
class DomainResult:
    data: Dict[str, pd.DataFrame] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def raise_if_strict(self, strict: bool):
        if strict and self.errors:
            raise ValueError("\n".join(self.errors))
