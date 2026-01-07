import re
from typing import Any

from pydantic_core import core_schema as pydantic_core_schema

from auth_service.core.config import settings

PHONE_MIN_LENGTH = 10
PHONE_MAX_LENGTH = 15


class PhoneStr(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any):
        field_schema = handler(core_schema)
        field_schema.update(
            type='string', format='tel', minLength=PHONE_MIN_LENGTH, description='Phone number with country code'
        )
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any):
        return pydantic_core_schema.no_info_after_validator_function(cls._validate, pydantic_core_schema.str_schema())

    @classmethod
    def _validate(cls, value: str, /) -> str:
        phone_number = re.sub(r'\D', '', value)
        if len(phone_number) < PHONE_MIN_LENGTH:
            raise ValueError(f'Phone number must have at least {PHONE_MIN_LENGTH} digits.')
        if len(phone_number) > PHONE_MAX_LENGTH:
            raise ValueError(f'Phone number must have at most {PHONE_MAX_LENGTH} digits.')
        return phone_number


class PasswordStr(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any):
        field_schema = handler(core_schema)
        field_schema.update(
            type='string',
            format='password',
            minLength=settings.password_min_length,
            description=f'Password with min {settings.password_min_length} chars, upper/lower/digit/special',
        )
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any):
        return pydantic_core_schema.no_info_after_validator_function(cls._validate, pydantic_core_schema.str_schema())

    @classmethod
    def _validate(cls, value: str, /) -> str:
        if len(value) < settings.password_min_length:
            raise ValueError(f'Password must be at least {settings.password_min_length} characters long.')
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character.')
        return value
