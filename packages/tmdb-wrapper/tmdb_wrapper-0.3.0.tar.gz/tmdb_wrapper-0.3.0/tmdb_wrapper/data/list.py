from dataclasses import dataclass
from typing import Optional, Union

from tmdb_wrapper.data.media import Media


@dataclass
class ListResponse:
    status_message: Optional[str]
    success: Optional[bool]
    status_code: Optional[int]
    list_id: Optional[int]

@dataclass
class ListStatus:
    id: Optional[str]
    item_present: Optional[bool]


@dataclass
class ListModel:
    created_by: Optional[str]
    description: Optional[str]
    favorite_count: Optional[int]
    id: Union[int, str]
    items: Optional[list[Media]]
    item_count: Optional[int]
    iso_639_1: Optional[str]
    name: Optional[str]
    poster_path: Optional[str]
