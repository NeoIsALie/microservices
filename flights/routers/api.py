from fastapi import APIRouter

from flights.routers import flight, airport

router = APIRouter()
router.include_router(airport.router)
router.include_router(flight.router)