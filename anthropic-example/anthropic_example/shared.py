import streamlit as st
from anthropic_example.rag.embedding import EmbeddingGenerator
from anthropic_example.services.anthropic import AnthropicService
from anthropic_example.services.milvus import MilvusService
from anthropic_example.settings import settings


@st.cache_resource
def get_anthropic_service() -> AnthropicService:
    return AnthropicService(api_key=settings.anthropic_api_key)


@st.cache_resource
def get_milvus_service() -> MilvusService:
    return MilvusService(
        milvus_uri=settings.milvus_uri,
        embedding_generator=EmbeddingGenerator(model_path=settings.embedding_model_path),
        collection_name=settings.milvus_collection_name,
    )
