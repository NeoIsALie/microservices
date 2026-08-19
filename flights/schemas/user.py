from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from dataclasses import dataclass
from uuid import UUID

from flights.enums.enums import RoleEnum


@dataclass(frozen=True)
class UserPayloadDTO(BaseModel):
    sub: UUID
    login: str
    role: RoleEnum
    email: EmailStr | None
    phone: PhoneNumber | None
    lastname: str | None
    firstname: str | None
    exp: datetime
    iat: datetime