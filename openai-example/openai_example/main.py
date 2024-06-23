from typing import Literal

import streamlit as st
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from openai_example.services.openai import OpenAIService
from openai_example.settings import settings

openai_service = OpenAIService(
    azure_endpoint=settings.azure_openai_endpoint,
    api_key=settings.azure_openai_api_key,
    api_version=settings.azure_openai_api_version,
    deployment_name=settings.azure_openai_deployment_name,
)


def initailize_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            ChatCompletionSystemMessageParam(
                content="You are a helpful assistant. All your answers are concise and to the point.",
                role="assistant",
            )
        ]


def display_messages() -> None:
    for message in st.session_state.messages[1:]:  # Skip the first message as it is the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def display_and_append_message(role: Literal["assistant", "user"], content: str) -> None:
    # Display the message
    with st.chat_message(role):
        st.markdown(content)

    # Add the message to the session state
    if role == "user":
        st.session_state.messages.append(ChatCompletionUserMessageParam(content=content, role="user"))
    elif role == "assistant":
        st.session_state.messages.append(ChatCompletionAssistantMessageParam(content=content, role="assistant"))
    else:
        raise ValueError(f"Invalid role: {role}")


def chat() -> None:
    display_messages()
    if prompt := st.chat_input("How can I help you?"):
        display_and_append_message("user", prompt)
        response = openai_service.generate(messages=st.session_state.messages)
        display_and_append_message("assistant", response.content)


def main() -> None:
    st.set_page_config(page_title=settings.app_name, page_icon="🤖")
    st.title("OpenAI Agent")
    initailize_session()
    chat()


if __name__ == "__main__":
    main()
