from dataclasses import dataclass
from typing import Optional


@dataclass
class DataResourceSchema:
    type: str
    name: str
    description: str
    fileFormat: Optional[str]
