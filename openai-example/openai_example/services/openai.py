import json

import openai_example.controllers.tools as tools
from openai import AzureOpenAI
from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionNamedToolChoiceParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.shared_params import FunctionDefinition
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
            ),
            ChatCompletionToolParam(
                type="function",
                function=FunctionDefinition(
                    name="create_jira_issue",
                    description="Create a new Jira issue with the provided summary and description.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "The summary of the Jira issue."},
                            "description": {"type": "string", "description": "The description of the Jira issue."},
                        },
                        "required": ["summary", "description"],
                    },
                ),
            ),
            ChatCompletionToolParam(
                type="function",
                function=FunctionDefinition(
                    name="delete_jira_issue",
                    description="Delete a Jira issue with the provided issue key.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "issue_key": {"type": "string", "description": "The key of the Jira issue to delete."},
                        },
                        "required": ["issue_key"],
                    },
                ),
            ),
        ]

    def generate(
        self, messages: list[ChatCompletionMessageParam], tools_choice: ChatCompletionNamedToolChoiceParam = "auto"
    ) -> ChatCompletionMessage:
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
                tool_function = getattr(tools, tool_call.function.name)
                tool_response = tool_function(**json.loads(tool_call.function.arguments))
                tool_messages.append(
                    ChatCompletionToolMessageParam(
                        tool_call_id=tool_call.id,
                        role="tool",
                        name=tool_call.function.name,
                        content=tool_response,
                    )
                )
            # Step 4: Recursively call generate to update the response based on the tool calls
            # By passing tools_choice="none", we ensure there are no more tool calls in the next response
            return self.generate(messages + [initial_response] + tool_messages, tools_choice="none")
