from uuid import uuid4

from sqlalchemy import Column, String, Integer, UUID, CheckConstraint

from flights.utils.database import Base


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ticket_uid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    username = Column(String(80), nullable=False, unique=True)
    flight_number = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(String(20), CheckConstraint("status in ('PAID', 'CANCELLED')"))
