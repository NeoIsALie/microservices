from typing import Type, Any

from sqlalchemy.orm import Session

from flights.models.flight import Flight


class FlightCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> list[Type[Flight]]:
        airports = self._db.query(Flight)
        return airports.offset(offset).limit(limit).all()

    async def get_by_id(self, flight_id: int) -> Flight | None:
        return self._db.query(Flight).filter(Flight.id == flight_id).first()

    async def create(self, airport: Flight) -> Flight | None:
        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except:
            self._db.rollback()

        return airport
    
    async def update(self, airport: Flight, update_fields: dict[str, Any]) -> Flight | None:
        for key, value in update_fields.items():
            setattr(airport, key, value)

        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except Exception:
            self._db.rollback()
            return None

        return airport

    async def delete(self, airport: Flight) -> None:
        self._db.delete(airport)
        self._db.commit()

    async def filter(self, filters: dict[str, Any]) -> list[Type[Flight]]:
        conditions = [
            getattr(Flight, column) == value
            for column, value in filters.items()
            if value
        ]
        return self._db.query(Flight).filter(*conditions).all()