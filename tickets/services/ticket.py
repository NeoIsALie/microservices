from typing import Type, Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from tickets.cruds.tickets import TicketCrud
from tickets.models.ticket import Ticket


class TicketService:
    def __init__(self, db: Session, crud: Type[TicketCrud]):
        self._crud: TicketCrud = crud(db)

    async def get_all(
            self,
            page: int = 1,
            size: int = 100,
    ):
        return await self._crud.get_all(offset=(page - 1) * size, limit=size)

    async def get_by_uuid(self, ticket_uid: UUID):
        ticket = await self._crud.get_by_uuid(ticket_uid=ticket_uid)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return ticket

    async def create(self, ticket: Ticket):
        return await self._crud.create(ticket)

    async def patch(self, ticket_uid: UUID, fields: dict[str, Any]):
        ticket = await self._crud.get_by_uuid(ticket_uid=ticket_uid)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return await self._crud.update(ticket, fields)

    async def delete(self, ticket_uid: UUID):
        ticket = await self._crud.get_by_uuid(ticket_uid=ticket_uid)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return await self._crud.delete(ticket)