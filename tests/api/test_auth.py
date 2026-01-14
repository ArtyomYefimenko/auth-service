import time
import uuid

import pytest
from fastapi import status


async def test_sign_up(client):
    request_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '48(071)-555-55-55',
        'password': '1qWze0!&',
    }

    response = await client.post('/api/v1/sign-up', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['detail'] == 'User created successfully'


async def test_sign_up_when_another_phone_user_exists(client, mock_user):
    request_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': mock_user.phone,
        'password': '1qWze0!&',
    }

    response = await client.post('/api/v1/sign-up', json=request_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == 'User already exists'


@pytest.mark.parametrize(
    'mock_user',
    [
        {'password': 'Pwd12345!'},
    ],
    indirect=True,
)
async def test_sign_in(client, mock_user):
    request_data = {
        'phone': mock_user.phone,
        'password': 'Pwd12345!',
    }

    response = await client.post('/api/v1/sign-in', json=request_data)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['access_token']
    assert data['refresh_token']
    assert data['token_type']


@pytest.mark.parametrize(
    'mock_user',
    [
        {'password': 'Pwd12345!'},
    ],
    indirect=True,
)
async def test_sign_in_with_another_phone(client, mock_user):
    request_data = {
        'phone': mock_user.phone + '1',
        'password': 'Pwd12345!',
    }

    response = await client.post('/api/v1/sign-in', json=request_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'


@pytest.mark.parametrize(
    'mock_user',
    [
        {'password': 'Pwd12345!'},
    ],
    indirect=True,
)
async def test_sign_in_with_invalid_password(client, mock_user):
    request_data = {
        'phone': mock_user.phone,
        'password': 'pWd12345!',
    }

    response = await client.post('/api/v1/sign-in', json=request_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'


async def test_get_profile(client, auth_client, mock_user):
    client = auth_client(
        client,
        user_id=mock_user.id,
    )
    response = await client.get('/api/v1/me')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['id'] == str(mock_user.id)
    assert data['first_name'] == mock_user.first_name
    assert data['last_name'] == mock_user.last_name
    assert data['phone'] == mock_user.phone


async def test_get_profile_when_token_missed(client, mock_user):
    response = await client.get('/api/v1/me')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Authorization header missing'


async def test_get_profile_when_token_expired(client, auth_client, mock_user):
    now = int(time.time())
    client = auth_client(
        client,
        user_id=mock_user.id,
        expires_timestamp=now - 100,
    )
    response = await client.get('/api/v1/me')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Token expired'


async def test_get_profile_when_user_not_found(client, auth_client, mock_user):
    client = auth_client(
        client,
        user_id=uuid.uuid4(),
    )
    response = await client.get('/api/v1/me')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'
