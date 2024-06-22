from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings, env_file=".env"):  # type: ignore
    app_name: str = "OpenAI Agent"
    app_icon: str = "🤖"

    azure_openai_endpoint: HttpUrl
    azure_openai_api_key: SecretStr
    azure_openai_deployment_name: str
    azure_openai_api_version: str = "2024-02-01"
