from dataclasses import dataclass
from typing import Optional
from .image import Image, Images
from .media import Media
from .translation import Translation

@dataclass
class CollectionTranslation:
    id: Optional[int]
    translations: Optional[Translation]


@dataclass
class CollectionImage:
    id: Optional[int]
    backdrops: Optional[Image]
    posters: Optional[Image]

@dataclass
class Collection:
    id: Optional[int]
    adult: Optional[bool]
    backdrop_path: Optional[str]
    images: Optional[Images]
    name: Optional[str]
    original_language: Optional[str]
    original_name: Optional[str]
    overview: Optional[str]
    parts: Optional[list[Media]]
    poster_path: Optional[str]
    translations: Optional[list[Translation]]



    