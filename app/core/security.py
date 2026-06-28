from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()

class SecurityService:
  @staticmethod
  def hash_password(password: str) -> str:
    return password_hash.hash(password)

  @staticmethod
  def verify_password(
    plain_password: str,
    hashed_password: str,
  ) -> bool:
    return password_hash.verify(
      plain_password,
      hashed_password,
    )

  @staticmethod
  def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
      minutes=settings.access_token_expire_minutes,
    )
    payload = {
      "sub": subject,
      "exp": expire,
    }
    return jwt.encode(
      payload,
      settings.jwt_secret_key,
      algorithm=settings.jwt_algorithm,
    )

  @staticmethod
  def decode_access_token(token: str) -> dict:
    try:
      return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
      )
    except JWTError as exc:
      raise ValueError("Invalid access token.") from exc