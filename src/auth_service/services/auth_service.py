import logging
import uuid
from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)

from auth_service.core.security import (
    create_access_token,
    create_hash,
    create_refresh_token,
    hash_password,
    verify_password,
)
from auth_service.models import User
from auth_service.repositories.auth_repository import AuthRepository
from auth_service.schemas.dto.auth import TokenPairDTO
from auth_service.schemas.dto.users import (
    UserCreateData,
    UserCreateDTO,
)

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, auth_repository: Annotated[AuthRepository, Depends()]):
        self.repo = auth_repository

    async def create_user(self, data: UserCreateDTO) -> User:
        exists_user = await self.repo.get_user_by_phone(phone_number=data.phone)
        if exists_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

        user_create_data = UserCreateData(
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            hashed_password=hash_password(password=data.password),
        )
        try:
            return await self.repo.create_user(data=user_create_data)
        except IntegrityError:  # if a parallel request occurred
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
        except SQLAlchemyError:
            logger.exception('Failed to create user')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to create user',
            )

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.repo.get_user_by_id(user_id=user_id)

    async def issue_token_pair(self, phone: str, password: str) -> TokenPairDTO:
        user = await self.repo.get_user_by_phone(phone)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

        return await self._generate_token_pair(user_id=user.id)

    async def refresh_tokens(self, refresh_token: str) -> TokenPairDTO:
        hashed_refresh_token = create_hash(refresh_token)
        token = await self.repo.get_refresh_token(hashed_token=hashed_refresh_token)
        if not token or token.is_expired:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired refresh token')

        user_id = token.user_id

        token_pair = await self._generate_token_pair(user_id=user_id)
        await self.repo.delete_refresh_token(token=token)
        return token_pair

    async def delete_refresh_token(self, refresh_token: str) -> None:
        hashed_refresh_token = create_hash(refresh_token)
        token = await self.repo.get_refresh_token(hashed_token=hashed_refresh_token)
        if not token or token.is_expired:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Refresh token not found or already expired',
            )
        await self.repo.delete_refresh_token(token=token)

    async def _generate_token_pair(self, user_id: uuid.UUID) -> TokenPairDTO:
        access_token = create_access_token(user_id=user_id)
        refresh_token = create_refresh_token()
        hashed_refresh_token = create_hash(refresh_token)

        await self.repo.create_refresh_token(
            user_id=user_id,
            hashed_token=hashed_refresh_token,
        )
        return TokenPairDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )
