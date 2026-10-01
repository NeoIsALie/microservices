from typing import Type, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from privilege_service.cruds.privilege import PrivilegeCrud
from privilege_service.models.privilege import Privilege


class PrivilegeService:
    def __init__(self, db: Session, crud: Type[PrivilegeCrud]):
        self._crud: PrivilegeCrud = crud(db)

    async def get_all(
            self,
            page: int = 1,
            size: int = 100,
    ):
        return await self._crud.get_all(offset=(page - 1) * size, limit=size)

    async def get_by_id(self, privilege_id: int):
        privilege = await self._crud.get_by_id(privilege_id)
        if not privilege:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Privilege not found")
        return privilege

    async def create(self, privilege: Privilege):
        return await self._crud.create(privilege)

    async def patch(self, privilege_id: int, fields: dict[str, Any]):
        privilege = await self._crud.get_by_id(privilege_id=privilege_id)
        if not privilege:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Privilege not found")
        return await self._crud.update(privilege, fields)

    async def delete(self, privilege_id: int):
        privilege = await self._crud.get_by_id(privilege_id=privilege_id)
        if not privilege:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Privilege not found")
        return await self._crud.delete(privilege)