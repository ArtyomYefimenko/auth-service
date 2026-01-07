import uuid
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class UserSchema(BaseModel):
    id: uuid.UUID
    phone: str
    first_name: str
    last_name: str
    is_active: bool
    is_phone_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
