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
    if isinstance(result, str):
        st.error(result)
    else:
        clauses, risk_levels = result
        st.write("### Extracted Clauses")
        for clause in clauses:
            st.write(f"- **{clause.clause_id}**:")
            st.write(f"- **{clause.name}**:")
            st.write(clause.text)

        st.write("### Risk Assessment")
        for risk_level in risk_levels:
            st.write(f"- **{risk_level.risk_level.value.capitalize()} Risk**:")
            st.write(f"  - Clause ID: {risk_level.clause_id}")
            st.write(f"  - Risk Category: {risk_level.risk_category}")
            st.write(f"  - Risk Description: {risk_level.risk_description}")
