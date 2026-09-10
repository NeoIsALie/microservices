from uuid import UUID

from fastapi import Query
from typing import Annotated, Any

from fastapi import Depends, APIRouter, Response, status
from sqlalchemy.orm import Session

from tickets_service.cruds.tickets import TicketCrud
from tickets_service.models.ticket import Ticket
from tickets_service.schemas.ticket import TicketResponse
from tickets_service.services.ticket import TicketService
from tickets_service.utils.database import get_db


def get_tickets_crud() -> TicketCrud:
    return TicketCrud


def get_ticket_service(
        ticket_crud: Annotated[TicketCrud, Depends(get_tickets_crud)],
        db: Annotated[Session, Depends(get_db)]
) -> TicketService:
    return TicketService(db, ticket_crud)


router = APIRouter(
    prefix="/tickets_service",
    tags=["Tickets rest api"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    }
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[TicketResponse],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
    }
)
async def get_all_tickets(
        ticket_service: Annotated[TicketService, Depends(get_ticket_service)],
        filters: dict[str, Any],
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=1)] = 100
):
    return await ticket_service.get_all(
        filters=filters,
        page=page,
        size=size
    )


@router.get(
    path="/{ticket_id}",
    status_code=status.HTTP_200_OK,
    response_model=TicketResponse,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def get_ticket_by_id(
        ticket_service: Annotated[TicketService, Depends(get_ticket_service)],
        ticket_id: UUID,
):
    return await ticket_service.get_by_uuid(ticket_uid=ticket_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    responses={
        status.HTTP_201_CREATED: {"description": "Created"},
    }
)
async def create_ticket(
        ticket_service: Annotated[TicketService, Depends(get_ticket_service)],
        ticket: Ticket,
):
    ticket = await ticket_service.create(
        ticket=ticket,
    )
    return ticket


@router.patch(
    path="/{ticket_id}",
    status_code=status.HTTP_200_OK,
    response_model=Ticket,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def update_ticket(
        ticket_service: Annotated[TicketService, Depends(get_ticket_service)],
        ticket_id: UUID,
        ticket_update: dict[str, Any],
):
    return await ticket_service.patch(
        ticket_uid=ticket_id,
        **ticket_update
    )


@router.delete(
    path="/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def delete_ticket(
        ticket_service: Annotated[TicketService, Depends(get_ticket_service)],
        ticket_id: UUID,
):
    return await ticket_service.delete(ticket_uid=ticket_id)
