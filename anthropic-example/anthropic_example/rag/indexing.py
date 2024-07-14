from anthropic_example.rag.embedding import EmbeddingGenerator
from numpy import ndarray
from pydantic import HttpUrl
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    MilvusClient,
    connections,
)


class Indexer:
    def __init__(self, milvus_uri: HttpUrl, embedding_generator: EmbeddingGenerator, collection_name: str):
        self.client: MilvusClient = MilvusClient(uri=str(milvus_uri))
        self.embedding_generator: EmbeddingGenerator = embedding_generator
        self.collection_name: str = collection_name

        connections.connect(uri=str(milvus_uri))

    def get_schema(self) -> CollectionSchema:
        return CollectionSchema(
            fields=[
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(
                    name="text", dtype=DataType.VARCHAR, description="The text of the document", max_length=10000
                ),
                FieldSchema(
                    name="source",
                    dtype=DataType.VARCHAR,
                    description="The source of the document, usally a file name or URL",
                    max_length=1000,
                ),
                FieldSchema(
                    name="source_type",
                    dtype=DataType.VARCHAR,
                    description="MimeType of the source document, e.g. 'text/plain' or 'application/pdf'",
                    max_length=100,
                ),
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=self.embedding_generator.dim,
                    description="The embedding of the document",
                ),
            ]
        )

    def get_or_create_collection(self) -> Collection:
        schema = self.get_schema()
        collection = Collection(name=self.collection_name, schema=schema)

        # Create the collection if it does not exist
        if not self.client.has_collection(collection.name):
            self.client.create()

        return collection

    def get_num_documents(self) -> int:
        collection = self.get_or_create_collection()
        return collection.num_entities

    def index_document(self, chunks: list[str], source: str, source_type: str) -> int:
        collection = self.get_or_create_collection()
        embeddings: ndarray = self.embedding_generator.generate_embeddings(chunks).numpy()

        entries = []
        for chunk, embedding in zip(chunks, embeddings):
            entries.append(
                {
                    "text": chunk,
                    "source": source,
                    "source_type": source_type,
                    "embedding": embedding,
                }
            )
        self.client.insert(collection_name=collection.name, data=entries)
        collection.flush()
        return len(entries)
