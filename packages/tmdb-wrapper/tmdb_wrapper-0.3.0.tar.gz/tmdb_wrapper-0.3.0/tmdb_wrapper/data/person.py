from dataclasses import dataclass
from typing import Optional, Union

from tmdb_wrapper.data.credit import Credit
from tmdb_wrapper.data.media import Media


@dataclass 
class PersonData:
    biography: Optional[str]

@dataclass
class PersonTranslation:
    iso_639_1: Optional[str]
    iso_3166_1: Optional[str]
    name: Optional[str]
    data: Optional[PersonData]
    english_name: Optional[str]

@dataclass
class PersonTranslations:
    translations: Optional[list[PersonTranslation]]
    id: Optional[int]

@dataclass
class PersonProfile:
    file_path: Optional[str]
    aspect_ratio: Optional[str]
    height: Optional[int]
    iso_639_1: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    width: Optional[int]
    id: Optional[int]
    image_type: Optional[str]
    media: Optional[Media]
    media_type: Optional[str]

@dataclass
class PersonTaggedImages:
    id: Optional[int]
    page: Optional[int]
    results: Optional[list[PersonProfile]]
    total_pages: Optional[int]
    total_results: Optional[int]



@dataclass
class PersonOriginalValue:
    profile: Optional[PersonProfile]

@dataclass
class PersonItems:
    id: Optional[str]
    action: Optional[str]
    time: Optional[str]
    original_value: Optional[PersonOriginalValue]

@dataclass
class PersonChanges:
    key: Optional[str]
    items: Optional[PersonItems]

@dataclass
class PersonCredits:
    cast: Optional[list[Credit]]
    crew: Optional[list[Credit]]
    id: Optional[int]


@dataclass
class PersonExternalIds:
    imdb_id: Optional[str]
    facebook_id: Optional[str]
    freebase_mid: Optional[str]
    freebase_id: Optional[str]
    tvrage_id: Optional[int]
    twitter_id: Optional[str]
    id: Optional[int]
    instagram_id: Optional[str]


@dataclass
class Person:
    name: Optional[str]
    id: Optional[int]
    birthday: Optional[str]
    known_for_department: Optional[str]
    deathday: Optional[str]
    also_known_as: Optional[list[str]]
    gender: Optional[int]
    biography: Optional[str]
    popularity: Optional[float]
    place_of_birth: Optional[str]
    profile_path: Optional[str]
    adult: Optional[bool]
    imdb_id: Optional[str]
    homepage: Optional[set]


@dataclass
class GetCredits:
    id: Optional[str]
    credit_type: Optional[str]
    department: Optional[str]
    job: Optional[str]
    media: Optional[Media]
    media_type: Optional[str]
    person: Optional[Person]

@dataclass
class PersonPopular:

    adult: Optional[bool]
    gender: Optional[int]
    id: Optional[int]
    known_for: Optional[list[Media]]
    known_for_department: Optional[str]
    name: Optional[str]
    popularity: Optional[float]
    profile_path: Optional[str]
    credit_id: Optional[str]


@dataclass
class PersonPopulars:
    id: Optional[int]
    page: Optional[int]
    results: Optional[list[PersonPopular]]
    total_pages: Optional[int]
    total_results: Optional[int]
