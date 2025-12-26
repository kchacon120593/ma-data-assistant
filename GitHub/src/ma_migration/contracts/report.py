from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional
import pandas as pd

@dataclass
class RuleResult:
    rule_id: str
    severity: str  # "error" | "warning"
    message: str
    failed_rows: Optional[pd.DataFrame] = None

@dataclass
class ContractReport:
    contract_name: str
    dataset: str
    version: str | None = None
    results: List[RuleResult] = field(default_factory=list)

    def errors(self) -> List[RuleResult]:
        return [r for r in self.results if r.severity.lower() == "error"]

    def warnings(self) -> List[RuleResult]:
        return [r for r in self.results if r.severity.lower() == "warning"]

    def is_ok(self) -> bool:
        return len(self.errors()) == 0

    def summary(self) -> dict[str, Any]:
        return {
            "contract": self.contract_name,
            "dataset": self.dataset,
            "version": self.version,
            "rules_total": len(self.results),
            "errors": len(self.errors()),
            "warnings": len(self.warnings()),
        }

    def raise_if_strict(self, strict: bool = True) -> None:
        if strict and not self.is_ok():
            msgs = [f"[{r.severity.upper()}] {r.rule_id}: {r.message}" for r in self.errors()]
            raise ValueError("\n".join(msgs))
