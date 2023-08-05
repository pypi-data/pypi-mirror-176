from dataclasses import dataclass
from typing import Optional

@dataclass
class Change:
    id: Optional[int]
    action: Optional[str]
    time: Optional[str]
    iso_639_1: Optional[str]
    value: Optional[str]
    original_value: Optional[str]
    
@dataclass
class Changes:
    key: Optional[int]
    items: Optional[Change]
    