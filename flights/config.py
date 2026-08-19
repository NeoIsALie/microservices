from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class ServiceSettings(BaseModel):
    host: str = None
    port: int = None
    log_level: str = None
    reload: bool = None


class DatabaseSettings(BaseModel):
    user: str = None
    password: str = None
    host: str = None
    port: int = None
    database: str = None


class JWKSettings(BaseModel):
  host: str = None
  port: int = None
  kid: str = None


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__"
    )

    service: ServiceSettings = ServiceSettings()
    db: DatabaseSettings = DatabaseSettings()
    jwk: JWKSettings = JWKSettings()



settings = Settings()