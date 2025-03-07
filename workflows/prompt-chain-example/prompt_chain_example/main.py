import asyncio

import streamlit as st
from prompt_chain_example.services.gemini import GeminiService
from prompt_chain_example.settings import Settings
from prompt_chain_example.workflow import LegelReviewFlow

## Resources

settings = Settings()
gemini_service = GeminiService(settings.gemini_api_key, settings.model, settings.temperature)
workflow = LegelReviewFlow(gemini_service, timeout=120, verbose=True)


## Application UI

st.set_page_config(page_title="Legal Document Review", page_icon="📜")
st.title("Legal Document Review")

document = st.text_area("Enter the legal document text below:")
types = st.text_input(
    "Enter the the types of clauses to look for:",
    placeholder="e.g., liability, termination, payment",
)


async def process_document(document: str, types: str) -> str:
    return await workflow.run(document=document, types=types)


if document and types:
    st.write("Generating a summary of the document...")
    result = asyncio.run(process_document(document, types))
    st.write(result)
