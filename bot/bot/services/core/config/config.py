from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="bot/.env")

    BOT_API: Optional[str]
    DB_BOT_LINK: Optional[str]

    API_UID: str

    DEBUG: bool = False


options = Settings()
print(options)
