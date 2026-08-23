from typing import Annotated
from pydantic import BaseModel, constr, conint
from fastapi import Query
from uuid import UUID



class Airport(BaseModel):
    name: Annotated[str, constr(max_length=255)]
    city: Annotated[str, constr(max_length=255)]
    country: Annotated[str, constr(max_length=255)]


class AirportResponse(BaseModel):
    name: Annotated[str, Query(max_length=20)]
    city: Annotated[str, Query(max_length=255)]
    country: Annotated[str, Query(max_length=255)]


class AirportInfo(Airport):
    flight_uuid: UUID


class AirportPaginatedResponse(BaseModel):
    page: Annotated[str, conint(ge=1)]
    pageSize: Annotated[int, conint(ge=1)]
    totalElements: Annotated[int, conint(ge=1)]
    items: list[AirportInfo]