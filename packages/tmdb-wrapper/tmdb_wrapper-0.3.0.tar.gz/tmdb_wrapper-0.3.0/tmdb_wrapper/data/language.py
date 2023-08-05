from dataclasses import dataclass
from typing import Optional


@dataclass
class Language:
    iso_639_1: Optional[str]
    name: Optional[str]

    