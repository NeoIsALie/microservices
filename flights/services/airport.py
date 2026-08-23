from typing import Type, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from flights.cruds.airport import AirportCrud
from flights.models.airport import Airport


class AirportService:
    def __init__(self, db: Session, crud: Type[AirportCrud]):
        self._crud: AirportCrud = crud(db)

    async def get_all(
            self,
            page: int = 1,
            size: int = 100,
    ):
        return await self._crud.get_all(offset=(page - 1) * size, limit=size)

    async def get_by_id(self, airport_id: int):
        airport = await self._crud.get_by_id(airport_id)
        if not airport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
        return airport

    async def create(self, airport: Airport):
        return await self._crud.create(airport)

    async def patch(self, airport_id: int, fields: dict[str, Any]):
        airport = await self._crud.get_by_id(airport_id=airport_id)
        if not airport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
        return await self._crud.update(airport, fields)

    async def delete(self, airport_id: int):
        airport = await self._crud.get_by_id(airport_id=airport_id)
        if not airport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
        return await self._crud.delete(airport)