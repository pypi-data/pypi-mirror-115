"""revtel fastapi package"""

from fastel.authorizers import (
    ClientIdAuth,
    ClientSecretAuth,
    Credential,
    JWBaseAuth,
    StaticClientAuth,
    StaticJWTAuth,
    StaticSecretAuth,
)
from fastel.exceptions import APIException

__version__ = "1.1.2"
__all__ = [
    "APIException",
    "ClientIdAuth",
    "ClientSecretAuth",
    "Credential",
    "JWBaseAuth",
    "StaticClientAuth",
    "StaticSecretAuth",
    "StaticJWTAuth",
]
