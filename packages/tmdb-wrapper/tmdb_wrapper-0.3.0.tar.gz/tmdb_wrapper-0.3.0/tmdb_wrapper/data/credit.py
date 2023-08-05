# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class Role:
    credit_id: Optional[str]
    character: Optional[str]
    episode_count: Optional[int]

@dataclass
class Job:
    credit_id: Optional[str]
    job: Optional[str]
    episode_count: Optional[int]

@dataclass
class Credit:
    id: Optional[int]
    adult: Optional[bool]
    cast_id: Optional[int]
    character: Optional[str]
    credit_id: Optional[str]
    department: Optional[str]
    gender: Optional[int]
    job: Optional[str]
    jobs: Optional[list[Job]]
    known_for_department: Optional[str]
    name: Optional[str]
    order: Optional[int]
    original_name: Optional[str]
    popularity: Optional[float]
    profile_path: Optional[str]
    title: Optional[str]
    release_date: Optional[str]
    vote_count: Optional[int]
    video: Optional[bool]
    vote_average: Optional[Union[int, float]]
    genre_ids: Optional[list[int]]
    original_language: Optional[str]
    original_title: Optional[str]
    backdrop_path: Optional[str]
    overview: Optional[str]
    poster_path: Optional[str]
    episode_count: Optional[int]
    origin_country: Optional[list[str]]
    media_type: Optional[str]
    first_air_drop: Optional[str]
    roles: Optional[Union[Role,list[Role]]]
    



    def __str__(self) -> str:
        return self.name or self.original_name

    @property
    def profile(self) -> Optional[str]:
        if self.profile_path:
            return f"https://image.tmdb.org/t/p/w1280{self.profile_path}"

    def is_director(self) -> bool:
        return self.job == "Director"

@dataclass
class Credits:
    id: Optional[int]
    cast: Optional[list[Credit]]
    crew: Optional[list[Credit]]

    def __bool__(self) -> bool:
        return bool(self.cast or self.crew)

    @property
    def directors(self) -> Optional[list[str]]:
        if self.crew:
            return [str(person) for person in self.crew if person.is_director()]





