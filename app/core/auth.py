from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AppException
from app.core.security import SecurityService

security = HTTPBearer()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    try:
        payload = SecurityService.decode_access_token(
            credentials.credentials,
        )
        return payload["sub"]
    except Exception as exc:
        raise AppException(
            message="Invalid or expired access token.",
            status_code=401,
        ) from exc
