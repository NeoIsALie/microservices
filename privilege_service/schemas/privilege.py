from uuid import uuid4
from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, constr, conint


class Privilege(BaseModel):
    username: Annotated[str, constr(max_length=80)]
    status: Annotated[str, constr(max_length=80)]
    balance: Annotated[int, conint(ge=0)]


class PrivilegeResponse(BaseModel):
    username: Annotated[str, constr(max_length=80)]
    status: Annotated[str, constr(max_length=80)]
    balance: Annotated[int, conint(ge=0)]


class PrivilegeHistory(BaseModel):
    datetime: datetime
    ticket_uid: uuid4
    balance_diff: Annotated[int, conint(ge=0)]
    operation_type: Annotated[str, constr(max_length=80)]


class PrivilegeHistoryResponse(BaseModel):
    datetime: datetime
    ticket_uid: uuid4
    balance_diff: Annotated[int, conint(ge=0)]
    operation_type: Annotated[str, constr(max_length=80)]