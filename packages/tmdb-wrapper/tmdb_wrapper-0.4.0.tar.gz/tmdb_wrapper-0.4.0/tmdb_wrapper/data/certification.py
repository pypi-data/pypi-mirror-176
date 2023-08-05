from dataclasses import dataclass
from typing import Optional


@dataclass
class USCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class CACertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class DECertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class GBCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class AUCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class BRCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class FRCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class NZCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class INCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class THCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class KRCertification:
    certification: Optional[str]
    meaning: Optional[str]
    order: Optional[int]

@dataclass
class Certification:
    '''
    certification data class
    '''
    US: Optional[USCertification]
    CA: Optional[CACertification]
    DE: Optional[DECertification]
    GB: Optional[GBCertification]
    AU: Optional[AUCertification]
    BR: Optional[BRCertification]
    FR: Optional[FRCertification]
    NZ: Optional[NZCertification]
    IN: Optional[INCertification]
    TH: Optional[THCertification]
    KR: Optional[KRCertification]