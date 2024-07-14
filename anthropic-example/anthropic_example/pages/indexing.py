import streamlit as st
from anthropic_example.rag.loading import load_pdf
from anthropic_example.rag.splitter import TextSplitter
from anthropic_example.settings import settings
from anthropic_example.shared import get_milvus_service

splitter = TextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)


def add_file() -> None:
    milvus_service = get_milvus_service()
    st.title("Indexing")
    st.markdown(
        f"Collection **{settings.milvus_collection_name}** contains **{st.session_state.milvus_service.get_num_documents()} documents**."
    )
    with st.expander("Add File to Index"):
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
        if uploaded_file:
            # Load the file
            if uploaded_file.type == "application/pdf":
                text, file_name = load_pdf(uploaded_file)
                st.info("PDF loaded successfully!")
            elif uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode("utf-8")
                file_name = uploaded_file.name
                st.info("Text loaded successfully!")

            # Split the text
            chunks = splitter.split_text(text)
            st.info(f"Text split into {len(chunks)} chunks.")

            # Index the chunks
            num_indexed = milvus_service.index_document(chunks, source=file_name, source_type=uploaded_file.type)
            st.info(f"Indexed {num_indexed} chunks.")


add_file()
