from jwcrypto.jws import InvalidJWSSignature
from jwcrypto.jwt import JWTExpired

from flights.enums.enums import TokenType, PayloadEnum
from flights.utils.jwt import decode_jwt


def validate_token_decode(
    token: str | None
):
    if not token:
        return None
    try:
        user_raw = decode_jwt(token)
    except InvalidJWSSignature:
        return None
    except JWTExpired:
        return None
    return user_raw


def validate_token_type(
    payload: dict,
    token_type: TokenType
) -> None:
    try:
        if payload[PayloadEnum.TOKEN_TYPE] != token_type:
            return None
    except KeyError:
        return None
