from dataclasses import dataclass
from typing import Optional


@dataclass
class GuestAuthentication:
    success: Optional[bool]
    guest_session_id: Optional[str]
    expires_at: Optional[str]

@dataclass
class RequestTokenAuthentication:
    success: Optional[bool]
    expires_at: Optional[str]
    request_token: Optional[str]

@dataclass
class SessionAuthentication:
    success: Optional[bool]
    session_id: Optional[str]