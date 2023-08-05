from dataclasses import dataclass
from typing import Optional
from tmdb_wrapper.data.collection import Collection
from tmdb_wrapper.data.credit import Credits

from tmdb_wrapper.data.genre import Genre
from tmdb_wrapper.data.image import Images
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.data.network import Network
from tmdb_wrapper.data.company import Company
from tmdb_wrapper.data.country import Country
from tmdb_wrapper.data.person import PersonPopular
from tmdb_wrapper.data.language import Language
from tmdb_wrapper.data.review import Review
from tmdb_wrapper.data.title import Titles
from tmdb_wrapper.data.external_id import ExternalIDs
from tmdb_wrapper.data.keyword import Keywords
from tmdb_wrapper.data.credit import Credit
from tmdb_wrapper.data.translation import Translation
from tmdb_wrapper.data.video import Video


@dataclass
class TvEpisode:
    air_date: Optional[str]
    episode_number: Optional[int]
    id: Optional[int]
    name: Optional[str]
    overview: Optional[str]
    production_code: Optional[str]
    season_number: Optional[int]
    still_path: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]

@dataclass
class Tv:
    id: Optional[int]
    adult: Optional[bool]
    backdrop_path: Optional[str]
    belongs_to_collection: Optional[Collection]
    budget: Optional[int]
    created_by: Optional[list[PersonPopular]]
    genre_ids: Optional[list[int]]
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
    episode_run_time: Optional[list[int]]
    first_air_date: Optional[str]
    in_production: Optional[bool]
    languages: Optional[list[str]]
    last_air_date: Optional[str]
    last_episode_to_air: Optional[TvEpisode]
    name: Optional[str]
    next_episode_to_air: Optional[str]
    networks: Optional[list[Network]]
    number_of_episodes: Optional[int]
    number_of_seasons: Optional[int]
    origin_country: Optional[list[str]]
    original_name: Optional[str]
    seasons: Optional[list[TvEpisode]]
    favorite: Optional[int]
    rated: Optional[bool]
    watchlist: Optional[bool]
    
@dataclass
class TvAccountState:
     id: Optional[int]
     favorite: Optional[int]
     rated: Optional[bool]
     watchlist: Optional[bool]

@dataclass
class TvCredits:
     id: Optional[int]
     cast: Optional[list[Credit]]
     crew: Optional[list[Credit]]

@dataclass
class TvAlternativeTitle:
    title: Optional[str]
    iso_3166_1: Optional[str]
    type: Optional[str]


@dataclass
class TvAlternativeTitles:
    id: Optional[int]
    results: Optional[list[TvAlternativeTitle]]

@dataclass
class TvItems:
    id: Optional[str]
    action: Optional[str]
    time: Optional[str]


@dataclass
class TvChange:
    key: Optional[str]
    items: Optional[list[TvItems]]

@dataclass
class TvChanges:
    changes: Optional[list[TvChange]]

@dataclass
class TvRating:
    iso_3166_1: Optional[str]
    rating: Optional[str]

@dataclass
class TvRatings:
    id: Optional[int]
    results: Optional[list[TvRating]]


@dataclass
class TvEpisodeGroup:
    description: Optional[str]
    episode_count: Optional[int]
    group_count: Optional[int]
    id: Optional[str]
    name: Optional[str]
    network: Optional[Network]
    type: Optional[int]

@dataclass
class TvEpisodeGroups:
    results: Optional[list[TvEpisodeGroup]]
    id: Optional[int]

@dataclass
class TvRecommendations:
    page: Optional[int]
    results: Optional[list[Tv]]
    total_pages: Optional[int]
    total_results: Optional[int]

@dataclass
class TvReviews:
    id: Optional[int]
    page: Optional[int]
    results: Optional[list[Review]]
    total_pages: Optional[int]
    total_results: Optional[int]


@dataclass
class TvScreen:
    id: Optional[int]
    episode_number: Optional[int]
    season_number: Optional[int]

@dataclass
class TvScreens:
    id: Optional[int]
    results: Optional[list[TvScreen]]

@dataclass
class TvSimilars:
    page: Optional[int]
    results: Optional[list[Tv]]
    total_pages: Optional[int]
    total_results: Optional[int]

@dataclass
class TvTranslations:
    id: Optional[int]
    translations: Optional[list[Translation]]

@dataclass
class TvVideos:
    id: Optional[int]
    results: Optional[list[Video]]

@dataclass
class TvResponse:
    status_code: Optional[int]
    status_message: Optional[str]

@dataclass
class TvAiring:
    page: Optional[int]
    results: Optional[list[Tv]]
    total_pages: Optional[int]
    total_results: Optional[int]