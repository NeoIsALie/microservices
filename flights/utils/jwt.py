import json

from fastapi import requests
from jwcrypto.jwt import JWT
from jwcrypto.jwk import JWKSet, JWK

from flights.config import get_settings

settings = get_settings()

def __jwks_auth_url(
    host=settings.jwk.host,
    port=settings.jwk.port,
) -> str:
    return f"http://{host}:{port}/api/v1/user/.well-known/jwks.json"


def dict_to_jwks(jwks_dict: dict) -> JWKSet:
  return JWKSet.from_json(keyset=json.dumps(jwks_dict, sort_keys=True))


def __get_jwks() -> JWKSet:
    url: __jwks_auth_url()
    response = requests.get(url)
    return dict_to_jwks(response.json())


def decode_jwt(token: str | bytes)  -> dict:
    jwks = __get_jwks()

    jwt = JWT()
    jwt.deserialize(token, jwks)

    return json.loads(jwt.claims)