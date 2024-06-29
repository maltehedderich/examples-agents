from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_example.agent.tools import all_tools
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
