from typing import List

from sqlalchemy.orm import Session

from flights.models.flight import Flight


class FlightCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> List[Flight]:
        airports = self._db.query(Flight)
        return airports.offset(offset).limit(limit).all()

    async def get_by_id(self, id: int) -> Flight | None:
        return self._db.query(Flight).filter(Flight.id == id).first()

    async def create(self, airport: Flight) -> Flight | None:
        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except:
            self._db.rollback()

        return airport

    async def delete(self, airport: Flight) -> None:
        self._db.delete(airport)
        self._db.commit()

