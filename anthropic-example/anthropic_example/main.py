from typing import Literal

import streamlit as st
from anthropic_example.settings import settings
from anthropic_example.shared import get_anthropic_service


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
    st.session_state.messages.append({"role": role, "content": content})


def chat() -> None:
    anthropic_service = get_anthropic_service()
    display_messages()
    if prompt := st.chat_input("How can I help you?"):
        display_and_append_message("user", prompt)
        response = anthropic_service.generate(
            system="You are a helpful assistant. All your answers are concise and to the point.",
            messages=st.session_state.messages,
            model=settings.anthropic_model,
        )
        display_and_append_message("assistant", response.content[0].text)


def main() -> None:
    st.set_page_config(page_title=settings.app_name, page_icon="🤖")
    st.title(settings.app_name)
    initailize_session()
    chat()


if __name__ == "__main__":
    main()
