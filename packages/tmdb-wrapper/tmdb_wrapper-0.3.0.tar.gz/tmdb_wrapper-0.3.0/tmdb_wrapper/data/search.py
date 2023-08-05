from ctypes import Union
from dataclasses import dataclass
from typing import List, Optional
from tmdb_wrapper.data.media import Media

from tmdb_wrapper.data.person import PersonPopular


@dataclass
class Search:
    page: Optional[int]
    results: Optional[list[Media]]
    total_pages: Optional[int]
    total_results: Optional[int]

@dataclass
class SearchMulti:
    page: Optional[int]
    results: Optional[List[PersonPopular]]
    total_pages: Optional[int]
    total_results: Optional[int]