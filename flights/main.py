import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from flights.routers.api import router as api_router

from flights.config import get_settings

settings = get_settings()


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_credentials=True,
  allow_origins=['*'],
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(api_router, prefix="/api/v1")


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.service.host,
        port=settings.service.port,
        log_level=settings.service.log_level,
        reload=settings.service.reload,
    )