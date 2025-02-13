import streamlit as st
from prompt_chain_example.chain import LegalReviewChain
from prompt_chain_example.models import Clause
from prompt_chain_example.services.gemini import GeminiService
from prompt_chain_example.settings import Settings

## Resources

settings = Settings()
gemini_service = GeminiService(settings.gemini_api_key, settings.model, settings.temperature)
chain = LegalReviewChain(gemini_service)


## Application UI

st.set_page_config(page_title="Legal Document Review", page_icon="📜")
st.title("Legal Document Review")

document = st.text_area("Enter the legal document text below:")
types = st.text_input(
    "Enter the the types of clauses to look for:", placeholder="e.g., liability, termination, payment"
)

if document and types:
    st.write("Generating a summary of the document...")
    result = chain.invoke(document, types)
    st.write(result)
