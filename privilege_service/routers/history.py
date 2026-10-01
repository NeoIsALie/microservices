from fastapi import Query
from typing import Annotated, Any

from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
from fastapi import status

from privilege_service.cruds.privilege_history import PrivilegeHistoryCrud
from privilege_service.schemas.privilege import PrivilegeHistory, PrivilegeHistoryResponse
from privilege_service.services.privilege_history import PrivilegeHistoryService
from privilege_service.utils.database import get_db


def get_privilege_service_crud() -> PrivilegeHistoryCrud:
    return PrivilegeHistoryCrud


def get_privilege_service(
        privilege_crud: Annotated[PrivilegeHistoryCrud, Depends(get_privilege_service_crud)],
        db: Annotated[Session, Depends(get_db)]
) -> PrivilegeHistoryService:
    return PrivilegeHistoryService(db, privilege_crud)


router = APIRouter(
    prefix="/privilege_service",
    tags=["PrivilegeHistorys rest api"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    }
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[PrivilegeHistoryResponse],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
    }
)
async def get_all_privilege_service(
    privilege_service: Annotated[PrivilegeHistoryService, Depends(get_privilege_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100
):
    return await privilege_service.get_all(
    page=page,
    size=size
)


@router.get(
    path="/{privilege_id}",
    status_code=status.HTTP_200_OK,
    response_model=PrivilegeHistoryResponse,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def get_privilege_by_id(
    privilege_service: Annotated[PrivilegeHistoryService, Depends(get_privilege_service)],
    privilege_id: int,
):
    return await privilege_service.get_by_id(privilege_id=privilege_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    responses={
        status.HTTP_201_CREATED: {"description": "Created"},
    }
)
async def create_privilege(
    privilege_service: Annotated[PrivilegeHistoryService, Depends(get_privilege_service)],
    privilege: PrivilegeHistory,
):
    privilege = await privilege_service.create(
        privilege=privilege,
    )
    return privilege


@router.patch(
    path="/{privilege_id}",
    status_code=status.HTTP_200_OK,
    response_model=PrivilegeHistory,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def update_privilege(
    privilege_service: Annotated[PrivilegeHistoryService, Depends(get_privilege_service)],
    privilege_id: int,
    privilege_update: dict[str, Any],
):
    return await privilege_service.patch(
        privilege_id=privilege_id,
        **privilege_update
    )


@router.delete(
    path="/{privilege_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def delete_privilege(
    privilege_service: Annotated[PrivilegeHistoryService, Depends(get_privilege_service)],
    privilege_id: int,
):
    return await privilege_service.delete(privilege_id=privilege_id)