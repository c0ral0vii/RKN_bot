from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent
print(ROOT_DIR)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{ROOT_DIR}/.env")

    BOT_API: Optional[str]
    DB_BOT_LINK: Optional[str]

    API_UID: str

    DEBUG: bool = False


options = Settings()
print(options)
