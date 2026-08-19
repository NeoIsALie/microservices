from idlelib.query import Query
from typing import Annotated, Any

from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
from starlette import status

from flights.cruds.flights import FlightCrud
from flights.schemas.flight import Flight, FlightResponse
from flights.services.flights import FlightService
from flights.utils.database import get_db


def get_flights_crud() -> FlightCrud:
    return FlightCrud


def get_flight_service(
        flight_crud: Annotated[FlightCrud, Depends(get_flights_crud)],
        db: Annotated[Session, Depends(get_db)]
) -> FlightService:
    return FlightService(db, flight_crud)


router = APIRouter(
    prefix="/flights",
    tags=["Flights rest api"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    }
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[FlightResponse],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
    }
)
async def get_all_flights(
    flight_service: Annotated[FlightService, Depends(get_flight_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=100)] = 100
):
    return await flight_service.get_all(
    page=page,
    size=size
)


@router.get(
    path="/{flight_id}",
    status_code=status.HTTP_200_OK,
    response_model=FlightResponse,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def get_flight_by_id(
    flight_service: Annotated[FlightService, Depends(get_flight_service)],
    flight_id: int,
):
    return await flight_service.get_by_id(flight_id=flight_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    responses={
        status.HTTP_201_CREATED: {"description": "Created"},
    }
)
async def create_flight(
    flight_service: Annotated[FlightService, Depends(get_flight_service)],
    flight: Flight,
):
    flight = await flight_service.create(
        flight=flight,
    )
    return flight


@router.patch(
    path="/{flight_id}",
    status_code=status.HTTP_200_OK,
    response_model=Flight,
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def update_flight(
    flight_service: Annotated[FlightService, Depends(get_flight_service)],
    flight_id: int,
    flight_update: dict[str, Any],
):
    return await flight_service.patch(
        flight_id=flight_id,
        **flight_update
    )


@router.delete(
    path="/{flight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "OK"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    }
)
async def delete_flight(
    flight_service: Annotated[FlightService, Depends(get_flight_service)],
    flight_id: int,
):
    return await flight_service.delete(flight_id=flight_id)