import pytest
from pydantic import ValidationError

from auth_service.schemas.http.auth import (
    SignInRequestSchema,
    SignUpRequestSchema,
)

VALID_SIGNUP_DATA = {
    'first_name': 'Mike ',
    'last_name': ' Ericsson ',
    'phone': '+48(071)-555-55-55',
    'password': '1qWze0!&',
}

VALID_SIGNIN_DATA = {
    'phone': '+48(071)-111-55-55',
    'password': '1qWze0!&',
}


@pytest.mark.parametrize('invalid_payload', [
    # first_name
    VALID_SIGNUP_DATA | {'first_name': '    '},
    VALID_SIGNUP_DATA | {'first_name': None},
    VALID_SIGNUP_DATA | {'first_name': 'Mike1'},

    # last_name
    VALID_SIGNUP_DATA | {'last_name': '    '},
    VALID_SIGNUP_DATA | {'last_name': None},
    VALID_SIGNUP_DATA | {'last_name': 'Ericsson1'},

    # phone
    VALID_SIGNUP_DATA | {'phone': None},
    VALID_SIGNUP_DATA | {'phone': '+48(071)0'},  # not enough digits
    VALID_SIGNUP_DATA | {'phone': '48(071)000-000-000-000'},  # too many digits

    # password
    VALID_SIGNUP_DATA | {'password': 'FqWzeO!&'},  # no digit
    VALID_SIGNUP_DATA | {'password': '1qwze0!&'},  # no uppercase char
    VALID_SIGNUP_DATA | {'password': '1QWZE0!&'},  # no lowercase char
    VALID_SIGNUP_DATA | {'password': '1qWze0iG'},  # no special char
    VALID_SIGNUP_DATA | {'password': '1qWze0!'},  # too short
    VALID_SIGNUP_DATA | {'password': None},

    # missing all fields
    {},
])
def test_sign_up_request_schema(invalid_payload):
    with pytest.raises(ValidationError):
        SignUpRequestSchema(**invalid_payload)


def test_sign_up_request_schema_success():
    schema = SignUpRequestSchema(**VALID_SIGNUP_DATA)

    assert schema.first_name == VALID_SIGNUP_DATA['first_name'].strip()
    assert schema.last_name == VALID_SIGNUP_DATA['last_name'].strip()
    assert schema.phone == '480715555555'
    assert schema.password == VALID_SIGNUP_DATA['password']


@pytest.mark.parametrize('invalid_payload', [
    # phone
    VALID_SIGNIN_DATA | {'phone': None},
    VALID_SIGNIN_DATA | {'phone': '+48(071)0'},  # not enough digits
    VALID_SIGNIN_DATA | {'phone': '48(071)000-000-000-000'},  # too many digits

    # password
    VALID_SIGNIN_DATA | {'password': 'FqWzeO!&'},  # no digit
    VALID_SIGNIN_DATA | {'password': '1qwze0!&'},  # no uppercase char
    VALID_SIGNIN_DATA | {'password': '1QWZE0!&'},  # no lowercase char
    VALID_SIGNIN_DATA | {'password': '1qWze0iG'},  # no special char
    VALID_SIGNIN_DATA | {'password': '1qWze0!'},  # too short
    VALID_SIGNIN_DATA | {'password': None},

    # missing all fields
    {},
])
def test_sign_in_request_schema(invalid_payload):
    with pytest.raises(ValidationError):
        SignInRequestSchema(**invalid_payload)


def test_sign_in_request_schema_success():
    schema = SignInRequestSchema(**VALID_SIGNIN_DATA)

    assert schema.phone == '480711115555'
    assert schema.password == VALID_SIGNUP_DATA['password']
