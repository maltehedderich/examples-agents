from typing import TypeVar

from google import genai  # type: ignore
from google.genai.types import GenerateContentConfig  # type: ignore
from pydantic import BaseModel, SecretStr

T = TypeVar("T", bound=BaseModel)


class GeminiService:
    def __init__(self, api_key: SecretStr, model: str, temperature: float):
        self.model = model
        self.temperature = temperature
        self.client = genai.Client(api_key=api_key.get_secret_value())

    async def generate(self, contents: str) -> str:
        config = GenerateContentConfig(
            temperature=self.temperature,
        )

        response = await self.client.aio.models.generate_content(model=self.model, contents=contents, config=config)

        return response.text

    async def generate_structured(
        self,
        contents: str,
        model: type[T] | type[list[T]],
    ) -> T | list[T]:
        config = GenerateContentConfig(
            temperature=self.temperature,
            response_mime_type="application/json",
            response_schema=model,
        )

        response = await self.client.aio.models.generate_content(model=self.model, contents=contents, config=config)

        assert response.parsed is not None, f"Failed to parse response: {response}"
        return response.parsed
