from typing import List

from sqlalchemy.orm import Session

from flights.models.airport import Airport


class AirportCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> List[Airport]:
        airports = self._db.query(Airport)
        return airports.offset(offset).limit(limit).all()

    async def get_by_id(self, id: int) -> Airport | None:
        return self._db.query(Airport).filter(Airport.id == id).first()

    async def create(self, airport: Airport) -> Airport | None:
        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except:
            self._db.rollback()

        return airport

    async def delete(self, airport: Airport) -> None:
        self._db.delete(airport)
        self._db.commit()

