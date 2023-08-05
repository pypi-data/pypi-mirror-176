# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

@dataclass
class ReleaseDate:
    certification: Optional[str]
    iso_639_1: Optional[str]
    release_date: Optional[str]
    type: Optional[int]
    note: Optional[str]

@dataclass
class ReleaseDateResult:
    iso_3166_1: Optional[str]
    release_dates: Optional[list[ReleaseDate]]

@dataclass
class ReleaseDates:
    id: Optional[int]
    results: Optional[list[ReleaseDateResult]]