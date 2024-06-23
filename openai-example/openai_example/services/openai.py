import json

from openai import AzureOpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.shared_params import FunctionDefinition
from openai_example.controllers.tools import get_current_datetime
from pydantic import HttpUrl, SecretStr


class OpenAIService:
    def __init__(self, azure_endpoint: HttpUrl, api_key: SecretStr, api_version: str, deployment_name: str):
        self._client = AzureOpenAI(
            api_key=api_key.get_secret_value(),
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )
        self._deployment_name = deployment_name
        self._tools = [
            ChatCompletionToolParam(
                type="function",
                function=FunctionDefinition(
                    name="get_current_datetime",
                    description="Get the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.",
                ),
            )
        ]
        self.tools_map = {"get_current_datetime": get_current_datetime}

    def generate(self, messages: list[ChatCompletionMessageParam]) -> ChatCompletionMessage:
        # Step 1: Generate a response from the OpenAI model
        chat_completion = self._client.chat.completions.create(
            messages=messages, model=self._deployment_name, tools=self._tools
        )
        initial_response = chat_completion.choices[0].message
        print("\nOpenAI Response Message:")
        print(initial_response.model_dump_json(indent=4))

        # Step 2: Check if the response contains tool calls
        if not initial_response.tool_calls:
            return initial_response
        else:
            # Step 3: Iterate over the tool calls and execute the corresponding tool function
            tool_messages: list[ChatCompletionToolMessageParam] = []
            for tool_call in initial_response.tool_calls:
                tool_response = self.tools_map[tool_call.function.name](**json.loads(tool_call.function.arguments))
                tool_messages.append(
                    ChatCompletionToolMessageParam(
                        tool_call_id=tool_call.id,
                        role="tool",
                        name=tool_call.function.name,
                        content=tool_response,
                    )
                )
            # Step 4: Recursively call generate to update the response based on the tool calls
            return self.generate(messages + [initial_response] + tool_messages)
