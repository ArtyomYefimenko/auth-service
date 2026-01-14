from typing import AsyncGenerator

import pytest

from auth_service.core.security import hash_password
from auth_service.models import User


@pytest.fixture
async def mock_user(session, request) -> AsyncGenerator[User]:
    params: dict = getattr(request, 'param', {}) or {}
    user = User(
        first_name='John',
        last_name='Wilson',
        phone=params.get('phone', '48547475446'),
        hashed_password=hash_password(params.get('password', 'Password123!')),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    yield user
