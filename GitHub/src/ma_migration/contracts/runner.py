from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd

from .report import ContractReport, RuleResult
from .rules import Rule, RULE_DISPATCH
from .loader import load_contract

def _parse_rules(contract: Dict[str, Any]) -> List[Rule]:
    rules: List[Rule] = []
    for r in (contract.get("rules", []) or []):
        rules.append(Rule(
            id=str(r.get("id")),
            severity=str(r.get("severity", "error")).lower(),
            type=str(r.get("type")),
            column=r.get("column"),
            columns=r.get("columns"),
            values=r.get("values"),
            equals=r.get("equals"),
            pattern=r.get("pattern"),
            max_length=r.get("max_length"),
        ))

    cols_block = contract.get("columns", {}) or {}
    for col, spec in cols_block.items():
        sev = str(spec.get("severity", "error")).lower()
        if spec.get("required") is True:
            rules.append(Rule(id=f"{col}__REQUIRED", severity=sev, type="not_null", column=col))
        if spec.get("unique") is True:
            rules.append(Rule(id=f"{col}__UNIQUE", severity=sev, type="unique", column=col))
        if "max_length" in spec:
            rules.append(Rule(id=f"{col}__MAX_LENGTH", severity=str(spec.get("severity", "warning")).lower(), type="max_length", column=col, max_length=int(spec["max_length"])))
        if "allowed_values" in spec:
            rules.append(Rule(id=f"{col}__ALLOWED", severity=sev, type="allowed_values", column=col, values=list(spec["allowed_values"])))

    required_cols = contract.get("required_columns", []) or []
    for col in required_cols:
        rules.append(Rule(id=f"{col}__PRESENT", severity="error", type="column_present", column=str(col)))

    return rules

def run_contract(df: pd.DataFrame, contract: Dict[str, Any], *, contract_name: str = "<in-memory>", strict: bool = True, sample_failures: int = 50) -> ContractReport:
    dataset = str(contract.get("dataset") or contract.get("domain") or "<unknown>")
    report = ContractReport(contract_name=contract_name, dataset=dataset, version=str(contract.get("version")) if contract.get("version") is not None else None)

    for rule in _parse_rules(contract):
        if rule.type == "column_present":
            if rule.column not in df.columns:
                report.results.append(RuleResult(rule_id=rule.id, severity=rule.severity, message=f"Missing required column: {rule.column}", failed_rows=None))
            continue

        # Ensure referenced columns exist
        cols_needed = []
        if rule.columns:
            cols_needed = list(rule.columns)
        elif rule.column:
            cols_needed = [rule.column]
        if any(c not in df.columns for c in cols_needed):
            report.results.append(RuleResult(rule_id=rule.id, severity=rule.severity, message=f"Column(s) not found for rule: {cols_needed}", failed_rows=None))
            continue

        fn = RULE_DISPATCH.get(rule.type)
        if fn is None:
            report.results.append(RuleResult(rule_id=rule.id, severity="error", message=f"Unknown rule type: {rule.type}", failed_rows=None))
            continue

        mask = fn(df, rule)
        if int(mask.sum()) == 0:
            continue

        failed = df.loc[mask].copy()
        if sample_failures is not None and len(failed) > sample_failures:
            failed = failed.head(sample_failures)

        report.results.append(RuleResult(
            rule_id=rule.id,
            severity=rule.severity,
            message=f"Rule failed: {rule.type} on {rule.column or rule.columns} (failed_rows={int(mask.sum())})",
            failed_rows=failed,
        ))

    report.raise_if_strict(strict)
    return report

def run_contracts(df: pd.DataFrame, contract_paths: List[str | Path], *, strict: bool = True) -> List[ContractReport]:
    reports: List[ContractReport] = []
    for p in contract_paths:
        c = load_contract(p)
        reports.append(run_contract(df, c, contract_name=str(p), strict=strict))
    return reports
