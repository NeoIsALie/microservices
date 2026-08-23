from typing import List, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from flights.enums.enums import RoleEnum, TokenType
from flights.schemas.user import UserPayloadDTO
from flights.utils.validation import validate_token_decode, validate_token_type

http_bearer = HTTPBearer(auto_error=False)

def __get_raw_payload(token: str | None) -> dict:
    raw = validate_token_decode(token)
    return raw


def __payload_to_dto(raw_payload: dict) -> UserPayloadDTO:
    validate_token_type(raw_payload, token_type=TokenType.ACCESS)
    try:
        payload = UserPayloadDTO.model_validate(raw_payload)
    except ValidationError as err:
        raise HTTPException(
            status_code=400,
            detail=err.message,
        )
    return payload


def get_current_user(
    token: HTTPAuthorizationCredentials | None = Depends(http_bearer)
) -> UserPayloadDTO:
    if not token:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    raw_payload = __get_raw_payload(token.credentials)

    return __payload_to_dto(raw_payload)

class RoleChecker:
    def __init__(self, allowed_roles: List[RoleEnum]):
        self.allowed_roles: List[RoleEnum] = allowed_roles

    def __call__(self, user: Annotated[UserPayloadDTO, Depends(get_current_user)]) -> bool:
        if user.role in self.allowed_roles:
            return True
        return False