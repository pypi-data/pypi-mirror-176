from dataclasses import dataclass
from typing import Optional

from tmdb_wrapper.data.author import AuthorDetails
from .media import Media

@dataclass
class Reviews:
    id: Optional[int]
    page: Optional[int]
    results: Optional[list[Media]]
    total_pages: Optional[int]
    total_results: Optional[int]


@dataclass
class Review:
    id: Optional[str]
    author: Optional[str]
    author_details: Optional[AuthorDetails]
    content: Optional[str]
    created_at: Optional[str]
    iso_639_1: Optional[str]
    media_id: Optional[int]
    media_title: Optional[str]
    media_type: Optional[str]
    updated_at: Optional[str]
    url: Optional[str] 