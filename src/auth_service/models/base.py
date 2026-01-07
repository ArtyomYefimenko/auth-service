import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from uuid6 import uuid7

from auth_service.core.database import ModelBaseDeclarative


class BaseModel(ModelBaseDeclarative):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )


class BaseTimestampModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
