from typing import Literal

import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_example.controllers.tools import all_tools
from langchain_example.settings import settings
from langchain_openai import AzureChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. All your answers are concise and to the point."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = AzureChatOpenAI(
    azure_endpoint=str(settings.azure_openai_endpoint),
    model=settings.azure_openai_deployment_name,
    openai_api_version=settings.azure_openai_api_version,
    api_key=settings.azure_openai_api_key.get_secret_value(),
    temperature=0,
)

agent = create_tool_calling_agent(llm, all_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)


def initailize_session() -> None:
    if "history" not in st.session_state:
        st.session_state.history = ChatMessageHistory()


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
        response = agent_executor.invoke({"input": prompt, "chat_history": st.session_state.history.messages})
        display_and_append_message("assistant", response["output"])


def main() -> None:
    st.set_page_config(page_title=settings.app_name, page_icon="🤖")
    st.title(settings.app_name)
    initailize_session()
    chat()


if __name__ == "__main__":
    main()
