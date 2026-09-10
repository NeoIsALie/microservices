from uuid import uuid4

from sqlalchemy import Column, String, Integer, UUID, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from flights.utils.database import Base


class Ticket(Base):
    __tablename__ = "tickets_service"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    ticket_uid: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    flight_number: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), CheckConstraint("status in ('PAID', 'CANCELLED')"))
