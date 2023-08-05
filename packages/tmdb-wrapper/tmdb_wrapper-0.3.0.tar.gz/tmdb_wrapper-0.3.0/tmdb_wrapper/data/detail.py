from dataclasses import dataclass
from typing import Optional

@dataclass
class Gravatar:
    hash: Optional[str]

@dataclass
class Avatar:
    gravatar: Optional[Gravatar]

@dataclass
class Detail:
    avatar: Optional[Avatar]
    id: Optional[int]
    iso_639_1: Optional[str]
    iso_3166_1: Optional[str]
    name: Optional[str]
    include_adult: Optional[bool]
    username: Optional[str]
