import pytest

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import SecurityService
from app.services.auth_service import AuthService


class TestAuthService:
    @pytest.mark.asyncio
    async def test_login_success(self, monkeypatch):

        service = AuthService()

        monkeypatch.setattr(
            settings,
            "admin_username",
            "karun",
        )

        monkeypatch.setattr(
            settings,
            "admin_password_hash",
            SecurityService.hash_password("AriseMonarch"),
        )

        response = await service.login(
            username="karun",
            password="AriseMonarch",
        )

        assert response.access_token
        assert response.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_username(self):

        service = AuthService()

        with pytest.raises(AppException):
            await service.login(
                username="wrong",
                password="AriseMonarch",
            )

    @pytest.mark.asyncio
    async def test_login_invalid_password(
        self,
        monkeypatch,
    ):

        service = AuthService()

        monkeypatch.setattr(
            settings,
            "admin_username",
            "karun",
        )

        monkeypatch.setattr(
            settings,
            "admin_password_hash",
            SecurityService.hash_password("AriseMonarch"),
        )

        with pytest.raises(AppException):
            await service.login(
                username="karun",
                password="WrongPassword",
            )
