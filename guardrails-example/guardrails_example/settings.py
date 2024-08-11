from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings, env_file=".env"):  # type: ignore
    app_name: str = "NeMo Guardrails Agent"

    azure_openai_endpoint: HttpUrl
    azure_openai_api_key: SecretStr
    azure_openai_deployment_name: str
    azure_openai_api_version: str = "2024-02-01"

    jira_base_url: HttpUrl
    jira_username: str
    jira_api_token: SecretStr
    jira_project_key: str


settings = Settings()
