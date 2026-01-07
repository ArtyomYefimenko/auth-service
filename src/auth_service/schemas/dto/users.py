from pydantic import (
    BaseModel,
    ConfigDict,
)


class UserCreateDTO(BaseModel):
    first_name: str
    last_name: str
    phone: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateData(BaseModel):
    first_name: str
    last_name: str
    phone: str
    hashed_password: str
