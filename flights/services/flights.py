from typing import Type, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from flights.cruds.flights import FlightCrud
from flights.models.flight import Flight


class FlightService:
    def __init__(self, db: Session, crud: Type[FlightCrud]):
        self._crud: FlightCrud = crud(db)

    async def get_all(
            self,
            page: int = 1,
            size: int = 100,
    ):
        return await self._crud.get_all(offset=(page - 1) * size, limit=size)

    async def get_by_id(self, flight_id: int):
        flight = await self._crud.get_by_id(flight_id)
        if not flight:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")

    async def create(self, flight: Flight):
        return await self._crud.create(flight)

    async def patch(self, flight_id: int, fields: dict[str, Any]):
        flight = await self._crud.get_by_id(flight_id=flight_id)
        if not flight:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        return await self._crud.update(flight, fields)

    async def delete(self, flight_id: int):
        flight = await self._crud.get_by_id(flight_id=flight_id)
        if not flight:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        return await self._crud.delete(flight)