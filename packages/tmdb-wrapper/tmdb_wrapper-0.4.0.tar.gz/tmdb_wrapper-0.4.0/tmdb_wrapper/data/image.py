# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

@dataclass
class Image:
    aspect_ratio: Optional[float]
    file_path: Optional[str]
    height: Optional[int]
    iso_639_1: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    width: Optional[int]
    id: Optional[int]

@dataclass
class Images:
    id: Optional[int]
    backdrops: Optional[list[Image]]
    logos: Optional[list[Image]]
    posters: Optional[list[Image]]
    profiles: Optional[list[Image]]