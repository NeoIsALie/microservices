from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from flights.utils.database import Base

class Flight(Base):
    __tablename__ = 'flights'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    flight_number = Column(String(20), nullable=False)
    datetime = Column(DateTime, nullable=False)
    from_airport_id = Column(Integer, ForeignKey('airports.id'))
    to_airport_id = Column(Integer, ForeignKey('airports.id'))
    price = Column(Integer, nullable=False)