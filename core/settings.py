from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):

    PATH_TO_BACKUPS: str
    PATH_TO_ORG_LIST: str

    BOT_API_TOKEN: str
    MY_CHAT_ID: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()