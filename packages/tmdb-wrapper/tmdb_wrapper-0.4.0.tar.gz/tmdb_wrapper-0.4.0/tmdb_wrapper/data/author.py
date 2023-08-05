from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthorDetails:
    name: Optional[str]
    username: Optional[str]
    avatar_path: Optional[str]
    rating: Optional[float]