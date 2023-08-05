from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfigurationImage:
    base_url: Optional[str]
    secure_base_url: Optional[str]
    backdrop_sizes: Optional[list[str]]
    logo_sizes: Optional[list[str]]
    poster_sizes: Optional[list[str]]
    profile_sizes: Optional[list[str]]
    still_sizes: Optional[list[str]]


@dataclass
class Configuration:
    images: Optional[ConfigurationImage]
    change_keys: Optional[list[str]]

@dataclass
class ConfigurationCountry:
    iso_3166_1: Optional[str]
    english_name: Optional[str]

@dataclass
class ConfigurationJobs:
    department: Optional[str]
    jobs: Optional[list[str]]

@dataclass
class ConfigurationLanguage:
    iso_3166_1: Optional[str]
    english_name: Optional[str]
    name: Optional[str]

@dataclass
class ConfigurationPrimTranslations:
    pass

@dataclass
class ConfigurationTimezones:
    iso_3166_1: Optional[str]
    zones: Optional[list[str]]