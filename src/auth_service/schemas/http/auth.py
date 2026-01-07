from pydantic import (
    BaseModel,
    Field,
)

from auth_service.schemas.custom_types import (
    PasswordStr,
    PhoneStr,
)


class SignUpRequestSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)
    phone: PhoneStr
    password: PasswordStr


class SignInRequestSchema(BaseModel):
    phone: PhoneStr
    password: PasswordStr


class TokenPairSchema(BaseModel):
    access_token: str  # jwt token
    refresh_token: str
    token_type: str = 'bearer'


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class LogoutRequestSchema(RefreshTokenRequestSchema):
    pass
