from dataclasses import dataclass
from typing import Optional


@dataclass
class Status:
    status_code: Optional[int]
    status_message: Optional[str]