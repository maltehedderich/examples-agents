from typing import Literal

import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage
from langchain_example.agent.core import agent_executor
from langchain_example.agent.memory import KnowledgeBase, update_knowledge_chain
from langchain_example.settings import settings


def initailize_session() -> None:
    if "history" not in st.session_state:
        st.session_state.history = ChatMessageHistory()
    if "knowledge_base" not in st.session_state:
        st.session_state.knowledge_base = KnowledgeBase()


def display_messages() -> None:
    for message in st.session_state.history.messages:  # Skip the first message as it is the system message
        role = "assistant" if isinstance(message, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(message.content)


def display_and_append_message(role: Literal["assistant", "user"], content: str) -> None:
    # Display the message
    with st.chat_message(role):
        st.markdown(content)

    # Add the message to the session state
    if role == "user":
        st.session_state.history.add_user_message(content)
    elif role == "assistant":
        st.session_state.history.add_ai_message(content)
    else:
        raise ValueError(f"Invalid role: {role}")


def chat() -> None:
    display_messages()
    if prompt := st.chat_input("How can I help you?"):
        display_and_append_message("user", prompt)

        # Invoke the agent to generate a response
        response = agent_executor.invoke(
            {
                "input": prompt,
                "chat_history": st.session_state.history.messages,
                "knowledge_base": st.session_state.knowledge_base,
            }
        )
        display_and_append_message("assistant", response["output"])

        # Update the knowledge base
        st.session_state.knowledge_base = update_knowledge_chain.invoke(
            {
                "knowledge_base": st.session_state.knowledge_base,
                "input": prompt,
                "output": response["output"],
            }
        )
        print(st.session_state.knowledge_base)


def main() -> None:
    st.set_page_config(page_title=settings.app_name, page_icon="🤖")
    st.title(settings.app_name)
    initailize_session()
    chat()


if __name__ == "__main__":
    main()
