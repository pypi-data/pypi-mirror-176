from dataclasses import dataclass
from typing import Optional


@dataclass
class Account:
    id: Optional[int]
    favourite: Optional[bool]
    rated: Optional[Rated]
    watchlist: Optional[bool]



    