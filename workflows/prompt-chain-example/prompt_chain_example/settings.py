from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: SecretStr

    model: str = "gemini-2.0-flash"
    temperature: float = 0.0

    model_config = SettingsConfigDict(env_file=(".env"))
