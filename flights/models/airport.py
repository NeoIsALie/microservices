from sqlalchemy import Column, String, Integer

from flights.utils.database import Base

class Airport(Base):
    __tablename__ = 'airport'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)