from enum import Enum

from google import genai  # type: ignore
from google.genai.types import GenerateContentConfig, SchemaUnion  # type: ignore
from pydantic import BaseModel, SecretStr


class GeminiService:
    def __init__(self, api_key: SecretStr, model: str, temperature: float):
        self.model = model
        self.temperature = temperature
        self.client = genai.Client(api_key=api_key.get_secret_value())

    def generate(self, contents: str, response_schema: SchemaUnion | None = None) -> BaseModel | str:
        config: GenerateContentConfig = {"temperature": self.temperature}

        if response_schema:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = response_schema

        response = self.client.models.generate_content(model=self.model, contents=contents, config=config)
        return response.parsed if response_schema else response.text
