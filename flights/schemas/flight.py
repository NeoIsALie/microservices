from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, constr, conint
from fastapi import Query
from uuid import UUID


class Flight(BaseModel):
    flight_number: Annotated[str, constr(max_length=20)]
    date: datetime
    from_airport_id: int
    to_airport_id: int
    price: int


class FlightResponse(BaseModel):
    flight_number: Annotated[str, Query(max_length=20)]
    from_airport: Annotated[str, Query(max_length=255)]
    to_airport: Annotated[str, Query(max_length=255)]
    date: datetime
    price: int


class FlightInfo(Flight):
    flight_uuid: UUID


class FlightPaginatedResponse(BaseModel):
    page: Annotated[str, conint(ge=1)]
    pageSize: Annotated[int, conint(ge=1)]
    totalElements: Annotated[int, conint(ge=1)]
    items: list[FlightInfo]