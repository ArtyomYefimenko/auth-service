import re

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from auth_service.schemas.custom_types import (
    PasswordStr,
    PhoneStr,
)

NAME_REGEX = re.compile(r"^[A-Za-zА-Яа-яЁёІіЇїЄє'’-]+$")


class SignUpRequestSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)
    phone: PhoneStr
    password: PasswordStr

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Must not be empty')

        if not NAME_REGEX.match(value):
            raise ValueError('Only letters, hyphen (-) and apostrophe (’) are allowed')

        return value


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
