from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class DomainContract:
    """Contract for a data domain pipeline."""
    domain: str | None = None
    path: str | None = None
    sheet: str | None = None
    columns: Dict[str, Any]
    
    