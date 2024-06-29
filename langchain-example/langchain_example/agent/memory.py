from typing import Annotated

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_example.settings import settings
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field


class KnowledgeBase(BaseModel):
    first_name: str = Field(
        "unknown", description="The first name of the user which is used to personalize the responses."
    )
    last_name: str = Field(
        "unknown", description="The last name of the user which is used to personalize the responses."
    )
    discussion_summary: str = Field(
        "unknown", description="Summary of the discussion including points discussed and possible action items."
    )
    open_problems: list[str] = Field([], description="Topics of the conversation that are still not resolved.")
    current_goals: list[str] = Field([], description="Current goal of the agent to address.")


knowledge_parser = PydanticOutputParser(pydantic_object=KnowledgeBase)

# This is an internal prompt used to update the knowledge base with information from the recent conversation.

update_knowledge_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=(
                    "You are an assistant for a chat agent."
                    " Your task is to update the knowledge base with the latest information."
                    "\n\n{format_instructions}"
                ),
                input_variables=[],
                partial_variables={"format_instructions": knowledge_parser.get_format_instructions()},
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=(
                    "OLD KNOWLEDGE BASE: {knowledge_base}\n\n"
                    "USER MESSAGE: {input}\n\n"
                    "ASSISTANT RESPONSE: {output}\n\n"
                    "NEW KNOWLEDGE BASE: "
                ),
                input_variables=["knowledge_base", "input", "output"],
            )
        ),
    ]
)

llm = AzureChatOpenAI(
    azure_endpoint=str(settings.azure_openai_endpoint),
    model=settings.azure_openai_deployment_name,
    openai_api_version=settings.azure_openai_api_version,
    api_key=settings.azure_openai_api_key.get_secret_value(),
    model_kwargs={"response_format": {"type": "json_object"}},
    temperature=0,
)

update_knowledge_chain = update_knowledge_prompt | llm | knowledge_parser
