from enum import StrEnum


class RoleEnum(StrEnum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class PayloadEnum(StrEnum):
  SUB="sub"
  LOGIN="login"
  ROLE="role"
  EMAIL="email"
  LASTNAME="lastname"
  FIRSTNAME="firstname"
  PHONE="phone"
  TOKEN_TYPE="type"
  EXP="exp"
  IAT="iat"