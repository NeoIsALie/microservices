from idlelib.query import Query
from typing import Annotated, Any

from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
from starlette import status

from flights.cruds.airport import AirportCrud
from flights.schemas.airport import Airport
from flights.services.airport import AirportService
from flights.utils.database import get_db


def get_airports_crud() -> AirportCrud:
    return AirportCrud


def get_airport_service(
        airport_crud: Annotated[AirportCrud, Depends(get_airports_crud)],
        db: Annotated[Session, Depends(get_db)]
) -> AirportService:
    return AirportService(db, airport_crud)


router = APIRouter(
    prefix="/airports",
    tags=["Airports rest api"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    }
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[Airport],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
    }
)
async def get_all_airports(
    airport_service: Annotated[AirportService, Depends(get_airport_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=100)] = 100
):
    return await airport_service.get_all(
    page=page,
    size=size
)


@router.get(
    path="/{airport_id}",
    status_code=status.HTTP_200_OK,
    response_model=Airport,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def get_airport_by_id(
    airport_service: Annotated[AirportService, Depends(get_airport_service)],
    airport_id: int,
):
    return await airport_service.get_by_id(airport_id=airport_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    responses={
        status.HTTP_201_CREATED: {"description": "Created"},
    }
)
async def create_airport(
    airport_service: Annotated[AirportService, Depends(get_airport_service)],
    airport: Airport,
):
    airport = await airport_service.create(
        airport=airport,
    )
    return airport


@router.patch(
    path="/{airport_id}",
    status_code=status.HTTP_200_OK,
    response_model=Airport,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def update_airport(
    airport_service: Annotated[AirportService, Depends(get_airport_service)],
    airport_id: int,
    airport_update: dict[str, Any],
):
    return await airport_service.patch(
        airport_id=airport_id,
        **airport_update
    )