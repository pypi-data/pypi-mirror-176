from dataclasses import dataclass
from typing import Optional

@dataclass
class Dates:
    maximum: Optional[str]
    minimum: Optional[str]