from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flights.config import get_settings


settings = get_settings()

POSTGRES_URL = (
    f"postgresql://{settings.database.username}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.db_name}"
)


engine = create_engine(
    POSTGRES_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
