from uuid import uuid4
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, UUID, DateTime

from flights.utils.database import Base



class Privilege(Base):
    __tablename__ = 'privilege'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    status = Column(String(80), CheckConstraint("status in ('BRONZE', 'SILVER', 'GOLD')"), default='BRONZE')
    balance = Column(Integer, nullable=False)


class PrivilegeHistory(Base):
    __tablename__ = 'privilege_history'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    privilege_id = Column(Integer, ForeignKey('privilege.id'), nullable=False)
    ticket_uid = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False)
    balance_diff = Column(Integer, nullable=False)
    operation_type = Column(
        String(20), CheckConstraint("operation_type in ('FILL_IN_BALANCE', 'DEBIT_THE_ACCOUNT')", nullable=False)
    )