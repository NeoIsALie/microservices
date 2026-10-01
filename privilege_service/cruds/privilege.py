from typing import Type, Any

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from privilege_service.models.privilege import Privilege


class PrivilegeCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ):
        stmt = select(Privilege).offset(offset).limit(limit)
        return self._db.execute(stmt).all()

    async def get_by_id(self, privilege_id: int) -> Privilege | None:
        stmt = select(Privilege).where(Privilege.id == privilege_id)
        return self._db.execute(stmt).first()

    async def create(self, privilege: Privilege) -> Privilege | None:
        try:
            self._db.add(privilege)
            self._db.commit()
            self._db.refresh(privilege)
        except:
            self._db.rollback()

        return privilege

    async def update(self, privilege: Privilege, update_fields: dict[str, Any]) -> Privilege | None:
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


    async def delete(self, privilege: Privilege) -> None:
        stmt = delete(Privilege).where(Privilege.id == privilege.id)
        self._db.execute(stmt)
        self._db.commit()

    async def filter(self, filters: dict[str, Any]) -> list[Type[Privilege]]:
        conditions = [
            getattr(Privilege, column) == value
            for column, value in filters.items()
            if value
        ]
        return self._db.query(Privilege).filter(*conditions).all()
