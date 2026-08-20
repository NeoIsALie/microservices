from typing import Any

from sqlalchemy import select, func
from sqlalchemy.orm import Session, aliased

from flights.models import Flight, Airport


class FlightCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ):
        FromAirport = aliased(Airport)
        ToAirport = aliased(Airport)
        stmt = (
            select(
                Flight.flight_number.label("flight_number"),
                func.concat(FromAirport.city, " ", FromAirport.name).label("from_airport"),
                func.concat(ToAirport.city, " ", ToAirport.name).label("to_airport"),
                Flight.datetime.label("date"),
                Flight.price
            )
            .join(
                FromAirport,
                Flight.from_airport_id == FromAirport.id,
            )
            .join(
                ToAirport,
                Flight.to_airport_id == ToAirport.id,
            )
            .limit(limit)
            .offset(offset)
        )
        return self._db.execute(stmt).all()

    async def get_by_id(self, flight_id: int):
        FromAirport = aliased(Airport)
        ToAirport = aliased(Airport)
        stmt = (
            select(
                Flight.flight_number.label("flight_number"),
                func.concat(FromAirport.city, " ", FromAirport.name).label("from_airport"),
                func.concat(ToAirport.city, " ", ToAirport.name).label("to_airport"),
                Flight.datetime.label("date"),
                Flight.price
            )
            .join(
                FromAirport,
                Flight.from_airport_id == FromAirport.id,
            )
            .join(
                ToAirport,
                Flight.to_airport_id == ToAirport.id,
            )
            .where(Flight.id == flight_id)
        )
        return self._db.execute(stmt).first()

    async def create(self, airport: Flight) -> Flight | None:
        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except:
            self._db.rollback()

        return airport
    
    async def update(self, flight: Flight, update_fields: dict[str, Any]) -> Flight | None:
        for key, value in update_fields.items():
            setattr(flight, key, value)

        try:
            self._db.add(flight)
            self._db.commit()
            self._db.refresh(flight)
        except Exception:
            self._db.rollback()
            return None

        return flight

    async def delete(self, airport: Flight) -> None:
        self._db.delete(airport)
        self._db.commit()

    async def filter(self, filters: dict[str, Any]):
        conditions = [
            getattr(Flight, column) == value
            for column, value in filters.items()
            if value
        ]
        stmt = select(Flight).filter(*conditions)
        return self._db.execute(stmt).all()