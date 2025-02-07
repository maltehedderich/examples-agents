import streamlit as st
from prompt_chain_example.services.gemini import GeminiService
from prompt_chain_example.settings import Settings

## Resources

settings = Settings()
gemini_service = GeminiService(settings.gemini_api_key, settings.model, settings.temperature)


## Application UI

st.set_page_config(page_title="Legal Document Review", page_icon="📜")
st.title("Legal Document Review")

user_input = st.text_area("Enter the legal document text below:")

if user_input:
    st.write("Generating a summary of the document...")
    summary = gemini_service.generate(user_input)
    st.write(summary)
