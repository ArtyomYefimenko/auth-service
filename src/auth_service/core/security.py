import hashlib
import time
import uuid

import jwt
from passlib.context import CryptContext

from auth_service.core.config import settings
from auth_service.schemas.dto.auth import JwtSchema

_pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)


def create_access_token(user_id: uuid.UUID) -> str:
    now = int(time.time())
    payload = JwtSchema(
        sub=user_id,
        jti=uuid.uuid4(),
        iat=now,
        exp=now + settings.access_token_life_time,
        token_type='access',
    )
    return jwt.encode(
        payload.model_dump(mode='json'),
        settings.jwt_secret,
        algorithm='HS256',
    )


def create_refresh_token() -> str:
    return uuid.uuid4().hex


def decode_access_token(token: str) -> JwtSchema:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=['HS256'], options={'require': ['exp', 'iat', 'sub', 'jti', 'iss']}
        )
    except jwt.PyJWTError:
        raise

    if payload.get('iss') != 'auth-service':
        raise jwt.InvalidTokenError('Invalid token issuer')

    return JwtSchema.model_validate(payload)


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if hash of plain_password matches hashed_password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    try:
        return _pwd_context.verify(plain_password, hashed_password)
    except Exception:  # noqa: B902
        return False


def create_hash(value: str) -> str:
    """Return SHA-256 hash of the given string."""
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
