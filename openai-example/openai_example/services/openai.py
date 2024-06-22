from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from pydantic import HttpUrl, SecretStr


class OpenAIService:
    def __init__(self, azure_endpoint: HttpUrl, api_key: SecretStr, api_version: str, deployment_name: str):
        self._client = AzureOpenAI(
            api_key=api_key.get_secret_value(),
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )
        self.deployment_name = deployment_name

    def generate(self, messages: list[ChatCompletionMessageParam]) -> ChatCompletionMessage:
        chat_completion = self._client.chat.completions.create(messages=messages, model=self.deployment_name)
        return chat_completion.choices[0].message
