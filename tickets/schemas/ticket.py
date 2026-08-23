from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, conint

from tickets.enums.enums import PaymentStatus


class TicketResponse(BaseModel):
    ticket_uid: UUID
    flight_number: str
    from_airport: str
    to_airport: str
    date: datetime
    price: int
    status: PaymentStatus


class TicketPurchaseResponse(TicketResponse):
    paidByMoney: conint(gt=0)
    paidByBonuses: conint(gt=0)
    privilege: dict[str, Any]


class TicketPaginatedResponse(BaseModel):
    page: Annotated[str, conint(ge=1)]
    pageSize: Annotated[int, conint(ge=1)]
    totalElements: Annotated[int, conint(ge=1)]
    items: list[TicketResponse]
