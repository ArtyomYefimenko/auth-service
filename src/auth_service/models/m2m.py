import time
import uuid
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from auth_service.core.config import settings
from auth_service.models.base import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = 'refresh_tokens'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
    )
    hashed_token: Mapped[str] = mapped_column(String(128), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
    )

    @property
    def is_expired(self) -> bool:
        return int(self.created_at.timestamp()) < time.time() - settings.refresh_token_life_time
