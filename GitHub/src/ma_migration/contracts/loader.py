from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

def _load_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
    except Exception as e:
        raise ImportError("PyYAML is required to load YAML contracts. Add dependency 'pyyaml'.") from e
    return yaml.safe_load(text)

def load_contract(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return _load_yaml(text)
    if path.suffix.lower() == ".json":
        import json
        return json.loads(text)
    raise ValueError(f"Unsupported contract format: {path.suffix}")

def load_contracts_from_dir(dir_path: str | Path, *, extensions: tuple[str, ...] = (".yaml", ".yml", ".json")) -> List[Dict[str, Any]]:
    d = Path(dir_path)
    contracts: List[Dict[str, Any]] = []
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.suffix.lower() in extensions:
            contracts.append(load_contract(p))
    return contracts
