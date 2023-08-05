# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import date
from optparse import Option
from typing import Optional, Union

from tmdb_wrapper.data.author import AuthorDetails
from tmdb_wrapper.data.season import Season


@dataclass
class Media:
    id: Optional[Union[int, float]]
    adult: Optional[bool]
    author: Optional[str]
    author_details: Optional[AuthorDetails]
    air_date: Optional[date]
    backdrop_path: Optional[str]
    character: Optional[str]
    content: Optional[str]
    created_at: Optional[str]
    description: Optional[str]
    episodes: Optional[list[str]]
    episode_count: Optional[int]
    episode_number: Optional[int]
    first_air_date: Optional[str]
    favourite_count: Optional[int]
    genre_ids: Optional[list[Union[int, float]]]
    item_count: Optional[int]
    iso_639_1: Optional[str]
    media_type: Optional[str]
    name: Optional[str]
    list_type: Optional[str]
    origin_country: Optional[Union[list[str],str]]
    original_language: Optional[str]
    original_name: Optional[str]
    original_title: Optional[str]
    overview: Optional[str]
    popularity: Optional[float]
    poster_path: Optional[str]
    production_code: Optional[str]
    release_date: Optional[str]
    seasons: Optional[Season]
    season_number: Optional[int]
    still_path: Optional[str]
    title: Optional[str]
    updated_at: Optional[str]
    url: Optional[str]
    video: Optional[bool]
    vote_average: Optional[float]
    vote_count: Optional[Union[int, float]]
    type: Optional[str]