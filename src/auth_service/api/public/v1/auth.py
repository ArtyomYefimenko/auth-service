import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from auth_service.api.dependencies import get_current_user_id
from auth_service.schemas.dto.users import UserCreateDTO
from auth_service.schemas.http.auth import (
    LogoutRequestSchema,
    RefreshTokenRequestSchema,
    SignInRequestSchema,
    SignUpRequestSchema,
    TokenPairSchema,
)
from auth_service.schemas.http.users import UserSchema
from auth_service.services.auth_service import AuthService

router = APIRouter(prefix='', tags=['Auth'])


@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
async def sign_up(
    data: SignUpRequestSchema,
    service: Annotated[AuthService, Depends()],
):
    await service.create_user(data=UserCreateDTO.model_validate(data))
    return {'detail': 'User created successfully'}


@router.post('/sign-in', response_model=TokenPairSchema)
async def sign_in(
    data: SignInRequestSchema,
    service: Annotated[AuthService, Depends()],
):
    token_data = await service.issue_token_pair(phone=data.phone, password=data.password)
    return TokenPairSchema.model_dump(token_data)


@router.get('/me', response_model=UserSchema)
async def get_user_profile(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[AuthService, Depends()],
):
    return await service.get_user_by_id(user_id=user_id)


@router.post('/refresh', response_model=TokenPairSchema)
async def refresh(
    data: RefreshTokenRequestSchema,
    service: Annotated[AuthService, Depends()],
):
    return await service.refresh_tokens(refresh_token=data.refresh_token)


@router.post('/logout')
async def logout(
    data: LogoutRequestSchema,
    service: Annotated[AuthService, Depends()],
):
    await service.delete_refresh_token(refresh_token=data.refresh_token)
    return {'detail': 'Logged out successfully'}
