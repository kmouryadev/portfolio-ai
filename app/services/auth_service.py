from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import SecurityService
from app.schemas.auth import TokenResponse


class AuthService:
    async def login(
        self,
        username: str,
        password: str,
    ) -> TokenResponse:
        if username != settings.admin_username:
            raise AppException(
                message="Invalid username or password.",
                status_code=401,
            )
        if not SecurityService.verify_password(
            password,
            settings.admin_password_hash,
        ):
            raise AppException(
                message="Invalid username or password.",
                status_code=401,
            )
        token = SecurityService.create_access_token(
            subject=username,
        )

        return TokenResponse(
            access_token=token,
        )
