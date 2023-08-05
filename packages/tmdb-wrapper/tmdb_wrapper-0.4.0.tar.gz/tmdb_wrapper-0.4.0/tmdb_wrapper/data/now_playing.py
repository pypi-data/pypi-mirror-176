from dataclasses import dataclass
from typing import Optional
from .media import Media
from .dates import Dates

@dataclass
class NowPlaying:
    page: Optional[int]
    results: Optional[list[Media]]
    dates: Optional[Dates]
    total_pages: Optional[int]
    total_results: Optional[int]