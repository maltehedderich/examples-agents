from os import environ
from typing import Literal

import nest_asyncio
import streamlit as st
from guardrails_example.settings import settings
from nemoguardrails import LLMRails, RailsConfig
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
)
from tqdm import tqdm

tqdm(disable=True, total=0)  # initialise internal lock

nest_asyncio.apply()
config = RailsConfig.from_path("./config")
config.models[0].parameters["api_key"] = settings.azure_openai_api_key.get_secret_value()
rails = LLMRails(config=config)


def initailize_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_messages() -> None:
    for message in st.session_state.messages:
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


def chat() -> None:
    display_messages()
    if prompt := st.chat_input("How can I help you?"):
        display_and_append_message("user", prompt)
        response = rails.generate(messages=st.session_state.messages)
        display_and_append_message("assistant", response["content"])
        info = rails.explain()
        print("LLM Calls Summary:")
        info.print_llm_calls_summary()
        print("Colang History:")
        print(info.colang_history)


def main() -> None:
    st.set_page_config(page_title=settings.app_name, page_icon="🤖")
    st.title(settings.app_name)
    initailize_session()
    chat()


if __name__ == "__main__":
    main()
