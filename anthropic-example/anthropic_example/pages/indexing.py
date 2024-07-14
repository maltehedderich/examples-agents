import streamlit as st
from anthropic_example.rag.embedding import EmbeddingGenerator
from anthropic_example.rag.indexing import Indexer
from anthropic_example.rag.loading import load_pdf
from anthropic_example.rag.splitter import TextSplitter
from anthropic_example.settings import settings

splitter = TextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
embedding_generator = EmbeddingGenerator(model_path=settings.embedding_model_path)
indexer = Indexer(
    milvus_uri=settings.milvus_uri,
    embedding_generator=embedding_generator,
    collection_name=settings.milvus_collection_name,
)


def add_file() -> None:
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
            num_indexed = indexer.index_document(chunks, source=file_name, source_type=uploaded_file.type)
            st.info(f"Indexed {num_indexed} chunks.")


st.title("Indexing")
st.markdown(f"Collection **{settings.milvus_collection_name}** contains **{indexer.get_num_documents()} documents**.")
add_file()
