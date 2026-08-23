from typing import Type, Any
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from tickets.models.ticket import Ticket


class TicketCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 100,
    ):
        stmt = select(Ticket).offset(offset).limit(limit)
        return self._db.execute(stmt).all()

    async def get_by_uuid(self, ticket_uid: UUID) -> Ticket | None:
        stmt = select(Ticket).where(Ticket.ticket_uid == ticket_uid)
        return self._db.execute(stmt).first()

    async def create(self, ticket: Ticket) -> Ticket | None:
        try:
            self._db.add(ticket)
            self._db.commit()
            self._db.refresh(ticket)
        except:
            self._db.rollback()

        return ticket

    async def update(
        self, ticket: Ticket, update_fields: dict[str, Any]
    ) -> Ticket | None:
        for key, value in update_fields.items():
            setattr(ticket, key, value)

        try:
            self._db.add(ticket)
            self._db.commit()
            self._db.refresh(ticket)
        except Exception:
            self._db.rollback()
            return None

        return ticket

    async def delete(self, ticket: Ticket) -> None:
        stmt = delete(Ticket).where(Ticket.ticket_uid == ticket.ticket_uid)
        self._db.execute(stmt)
        self._db.commit()

    async def filter(self, filters: dict[str, Any]) -> list[Type[Ticket]]:
        conditions = [
            getattr(Ticket, column) == value
            for column, value in filters.items()
            if value
        ]
        return self._db.query(Ticket).filter(*conditions).all()
