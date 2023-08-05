from dataclasses import dataclass
from typing import Optional
from tmdb_wrapper.data.image import Image

from tmdb_wrapper.data.media import Media


@dataclass
class Company:
    name: Optional[str]
    id: Optional[int]
    logo_path: Optional[str]
    origin_country: Optional[str]
    description: Optional[str]
    headquartes: Optional[str]
    homepage: Optional[str]
    parent_company: Optional[str]

@dataclass
class CompanyAlternativeNames:
    id: Optional[int]
    results: Optional[Media]


@dataclass
class CompanyImage:
    id: Optional[int]
    logos: Optional[Image]


    