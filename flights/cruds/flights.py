from typing import Type, Any

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from flights.models import Flight, Airport
from flights.schemas.flight import FlightResponse


class FlightCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> list[Flight]:
        FromAirport = aliased(Airport)
        ToAirport = aliased(Airport)
        stmt = (
            select(
                Flight.flight_number.label("flight_number"),
                FromAirport.name.label("from_airport"),
                ToAirport.name.label("to_airport"),
                Flight.datetime.label("date"),
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
        result = [
            FlightResponse(**row)
            for row in self._db.execute(stmt).mappings()
        ]
        return result

    async def get_by_id(self, flight_id: int) -> FlightResponse | None:
        FromAirport = aliased(Airport)
        ToAirport = aliased(Airport)
        stmt = (
            select(
                Flight.flight_number.label("flight_number"),
                FromAirport.name.label("from_airport"),
                ToAirport.name.label("to_airport"),
                Flight.datetime.label("date"),
            )
            .join(
                FromAirport,
                Flight.from_airport_id == FromAirport.id,
            )
            .join(
                ToAirport,
                Flight.to_airport_id == ToAirport.id,
            )
            .where(Flight.flight_number == flight_id)
        )
        result = self._db.execute(stmt).first().mappings()
        return FlightResponse(**result)

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