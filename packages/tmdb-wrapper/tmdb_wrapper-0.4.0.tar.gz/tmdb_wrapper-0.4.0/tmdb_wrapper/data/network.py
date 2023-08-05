from ctypes import Union
from dataclasses import dataclass
from typing import Optional

@dataclass
class NetworkAlternativeNamesResult:
    name: Optional[str]
    type: Optional[str]

@dataclass
class NetworkAlternativeNames:
    id: Optional[int]
    results: Optional[list[NetworkAlternativeNamesResult]]

@dataclass
class Network:
    headquarters: Optional[str]
    homepage: Optional[str]
    id: Optional[int]
    logo_path: Optional[str]
    name: Optional[str]
    origin_country: Optional[str]

@dataclass
class NetworkLogo:
    aspect_ratio: Optional[float]
    file_path: Optional[str]
    height: Optional[int]
    id: Optional[str]
    file_type: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    width: Optional[int]

@dataclass
class NetworkImage:
    id: Optional[int]
    logos: Optional[list[NetworkLogo]]
