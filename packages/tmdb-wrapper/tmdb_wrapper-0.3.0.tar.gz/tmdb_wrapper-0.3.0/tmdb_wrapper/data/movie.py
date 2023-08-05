from dataclasses import dataclass
from typing import Optional

from .collection import Collection
from .genre import Genre
from .company import Company
from .country import Country
from .language import Language
from .title import Titles
from .credit import Credits
from .image import Images
from .external_id import ExternalIDs
from .media import Media
from .video import Videos
from .provider import Providers
from .keyword import Keywords

@dataclass
class ModelMovies:
    page: Optional[int]
    results: Optional[list[Media]]
    total_pages: Optional[int]
    total_results: Optional[int]

    def __bool__(self) -> bool:
        return self.total_results > 0

    def __iter__(self) -> iter:
        return iter(self.results)

    def __getitem__(self, index: int) -> Media:
        return self.results[index]

@dataclass
class Movie:
    id: Optional[int]
    adult: Optional[bool]
    backdrop_path: Optional[str]
    belongs_to_collection: Optional[Collection]
    budget: Optional[int]
    genres: Optional[list[Genre]]
    homepage: Optional[str]
    imdb_id: Optional[str]
    original_language: Optional[str]
    original_title: Optional[str]
    overview: Optional[str]
    popularity: Optional[float]
    poster_path: Optional[str]
    production_companies: Optional[list[Company]]
    production_countries: Optional[list[Country]]
    release_date: Optional[str]
    revenue: Optional[int]
    runtime: Optional[int]
    spoken_languages: Optional[list[Language]]
    status: Optional[str]
    tagline: Optional[str]
    title: Optional[str]
    video: Optional[bool]
    vote_average: Optional[float]
    vote_count: Optional[int]
    alternative_titles: Optional[Titles]
    credits: Optional[Credits]
    external_ids: Optional[ExternalIDs]
    images: Optional[Images]
    keywords: Optional[Keywords]
    recommendations: Optional[ModelMovies]
    similar: Optional[ModelMovies]
    videos: Optional[Videos]
    watch_providers: Optional[Providers]



