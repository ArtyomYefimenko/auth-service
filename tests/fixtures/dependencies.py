import time
import uuid

import jwt
import pytest

from auth_service.core.config import settings
from auth_service.schemas.dto.auth import JwtSchema


def make_jwt_token(*, user_id: uuid.UUID, expires_timestamp: int = None) -> str:
    now = int(time.time())
    payload = JwtSchema(
        sub=user_id,
        jti=uuid.uuid4(),
        iat=now,
        exp=expires_timestamp or now + settings.access_token_life_time,
        token_type='access',
    )
    return jwt.encode(
        payload.model_dump(mode='json'),
        settings.jwt_secret,
        algorithm='HS256',
    )


@pytest.fixture
def auth_client():
    def factory(client, *, user_id: uuid.UUID, expires_timestamp: int = None):
        token = make_jwt_token(user_id=user_id, expires_timestamp=expires_timestamp)
        client.headers['Authorization'] = f'Bearer {token}'
        return client

    return factory
