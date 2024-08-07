from typing import Literal

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings, env_file=".env"):  # type: ignore
    app_name: str = "Anthropic Agent"

    anthropic_api_key: SecretStr
    anthropic_model: Literal["claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"] = "claude-3-5-sonnet-20240620"

    jira_base_url: HttpUrl
    jira_username: str
    jira_api_token: SecretStr
    jira_project_key: str

    milvus_uri: HttpUrl = HttpUrl("http://localhost:19530")
    milvus_collection_name: str = "anthropic_example"

    chunk_size: int = 2000
    chunk_overlap: int = 500
    embedding_model_path: str = "Alibaba-NLP/gte-large-en-v1.5"


settings = Settings()
