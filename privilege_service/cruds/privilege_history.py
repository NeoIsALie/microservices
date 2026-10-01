from typing import Type, Any

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from privilege_service.models.privilege import PrivilegeHistory


class PrivilegeHistoryCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ):
        stmt = select(PrivilegeHistory).offset(offset).limit(limit)
        return self._db.execute(stmt).all()

    async def get_by_id(self, privilege_id: int) -> PrivilegeHistory | None:
        stmt = select(PrivilegeHistory).where(PrivilegeHistory.id == privilege_id)
        return self._db.execute(stmt).first()

    async def create(self, privilege: PrivilegeHistory) -> PrivilegeHistory | None:
        try:
            self._db.add(privilege)
            self._db.commit()
            self._db.refresh(privilege)
        except:
            self._db.rollback()

        return privilege

    async def update(self, privilege: PrivilegeHistory, update_fields: dict[str, Any]) -> PrivilegeHistory | None:
        for key, value in update_fields.items():
            setattr(privilege, key, value)

        try:
            self._db.add(privilege)
            self._db.commit()
            self._db.refresh(privilege)
        except Exception:
            self._db.rollback()
            return None

        return privilege


    async def delete(self, privilege: PrivilegeHistory) -> None:
        stmt = delete(PrivilegeHistory).where(PrivilegeHistory.id == privilege.id)
        self._db.execute(stmt)
        self._db.commit()

    async def filter(self, filters: dict[str, Any]) -> list[Type[PrivilegeHistory]]:
        conditions = [
            getattr(PrivilegeHistory, column) == value
            for column, value in filters.items()
            if value
        ]
        return self._db.query(PrivilegeHistory).filter(*conditions).all()
