from google import genai  # type: ignore
from pydantic import SecretStr


class GeminiService:
    def __init__(self, api_key: SecretStr, model: str, temperature: float):
        self.model = model
        self.temperature = temperature
        self.client = genai.Client(api_key=api_key.get_secret_value())

    def generate(self, contents: str) -> str:
        response = self.client.models.generate_content(
            model=self.model, contents=contents, config={"temperature": self.temperature}
        )
        return response.text
