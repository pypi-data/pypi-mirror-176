from dataclasses import dataclass
from typing import Optional


@dataclass
class Season:
    air_date: Optional[str]
    poster_path: Optional[str]
    season_number: Optional[int]
