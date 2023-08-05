from dataclasses import dataclass
from typing import Optional

from tmdb_wrapper.data.media import Media


@dataclass
class Discover:
    page: Optional[int]
    results: Optional[list[Media]]
    total_pages: Optional[int]
    total_results: Optional[int]