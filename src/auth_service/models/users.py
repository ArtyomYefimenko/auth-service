from sqlalchemy import (
    Boolean,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from auth_service.models.base import BaseTimestampModel


class User(BaseTimestampModel):
    __tablename__ = 'users'

    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    phone: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
