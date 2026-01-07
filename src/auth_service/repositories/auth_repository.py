import uuid

from sqlalchemy.future import select

from auth_service.models.m2m import RefreshToken
from auth_service.models.users import User
from auth_service.repositories.base import BaseRepository
from auth_service.schemas.dto.users import UserCreateData


class AuthRepository(BaseRepository):
    async def get_user_by_phone(self, phone_number: str) -> User | None:
        result = await self.session.execute(select(User).where(User.phone == phone_number))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, data: UserCreateData) -> User:
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            hashed_password=data.hashed_password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_refresh_token(self, user_id: uuid.UUID, hashed_token: str):
        self.session.add(
            RefreshToken(
                user_id=user_id,
                hashed_token=hashed_token,
            )
        )
        await self.session.commit()

    async def get_refresh_token(self, hashed_token: str) -> RefreshToken | None:
        result = await self.session.execute(select(RefreshToken).where(RefreshToken.hashed_token == hashed_token))
        return result.scalar_one_or_none()

    async def delete_refresh_token(self, token: RefreshToken) -> None:
        await self.session.delete(token)
        await self.session.commit()
