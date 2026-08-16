from typing import Type, Any

from sqlalchemy.orm import Session

from flights.models.airport import Airport


class AirportCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> list[Type[Airport]]:
        airports = self._db.query(Airport)
        return airports.offset(offset).limit(limit).all()

    async def get_by_id(self, airport_id: int) -> Airport | None:
        return self._db.query(Airport).filter(Airport.id == airport_id).first()

    async def create(self, airport: Airport) -> Airport | None:
        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except:
            self._db.rollback()

        return airport

    async def update(self, airport: Airport, update_fields: dict[str, Any]) -> Airport | None:
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


    async def delete(self, airport: Airport) -> None:
        self._db.delete(airport)
        self._db.commit()

    async def filter(self, filters: dict[str, Any]) -> list[Type[Airport]]:
        conditions = [
            getattr(Airport, column) == value
            for column, value in filters.items()
            if value
        ]
        return self._db.query(Airport).filter(*conditions).all()
