from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, conint

from tickets_service.enums.enums import PaymentStatus


class TicketResponse(BaseModel):
    ticket_uid: UUID
    flight_number: str
    from_airport: str
    to_airport: str
    date: datetime
    price: int
    status: PaymentStatus

class TicketPaginatedResponse(BaseModel):
    page: Annotated[str, conint(ge=1)]
    pageSize: Annotated[int, conint(ge=1)]
    totalElements: Annotated[int, conint(ge=1)]
    items: list[TicketResponse]
