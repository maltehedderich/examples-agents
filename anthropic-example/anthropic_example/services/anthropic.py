import json
from typing import Literal

from anthropic import Anthropic
from anthropic.types import Message, MessageParam, ToolResultBlockParam
from anthropic_example.agent import tools
from pydantic import SecretStr


class AnthropicService:
    def __init__(self, api_key: SecretStr):
        self._client = Anthropic(api_key=api_key.get_secret_value())
        self._tools = [
            {
                "name": "get_current_datetime",
                "description": "Get the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "name": "create_jira_issue",
                "description": "Create a new Jira issue with the provided summary and description.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string", "description": "The summary of the Jira issue."},
                        "description": {"type": "string", "description": "The description of the Jira issue."},
                    },
                    "required": ["summary", "description"],
                },
            },
            {
                "name": "delete_jira_issue",
                "description": "Delete a Jira issue with the provided issue key.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "issue_key": {"type": "string", "description": "The key of the Jira issue to delete."},
                    },
                    "required": ["issue_key"],
                },
            },
        ]

    def generate(
        self,
        system: str,
        messages: list[MessageParam],
        model: Literal["claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"],
        max_tokens: int = 2048,
    ) -> Message:
        assistant_response = self._client.messages.create(
            model=model, system=system, messages=messages, max_tokens=max_tokens, tools=self._tools
        )

        print("\nAnthropic Response Message:")
        print(assistant_response.model_dump_json(indent=4))

        # Step 2: Check if the response contains tool calls
        if not assistant_response.stop_reason == "tool_use":
            return assistant_response
        else:
            # Step 3: Iterate over the tool calls and execute the corresponding tool function
            tool_results: list[ToolResultBlockParam] = []
            # Extract the tool calls from the response, claude provides the reasoning message as well
            tool_calls = [tool_call for tool_call in assistant_response.content if tool_call.type == "tool_use"]
            for tool_call in tool_calls:
                tool_function = getattr(tools, tool_call.name)
                tool_response = tool_function(**tool_call.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": tool_response,
                    }
                )
            assistant_message: MessageParam = {"role": "assistant", "content": assistant_response.content}
            user_message: MessageParam = {"role": "user", "content": tool_results}
            # Step 4: Recursively call generate to update the response based on the tool calls
            return self.generate(system, messages + [assistant_message, user_message], model, max_tokens)
