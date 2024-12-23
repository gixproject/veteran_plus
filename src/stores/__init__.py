from langchain_core.embeddings import Embeddings

from src.common.enums import VectorStoreEnum
from src.settings.base import settings
from src.stores.chromadb import ChromaVectorStore


def create_vector_store(
    embedder: Embeddings,
    collection_name: str,
    store_type: VectorStoreEnum,
) -> ChromaVectorStore:
    """Returns vector storage instance for given data store type."""

    collection_name = collection_name or f"{settings.common.provider}-default"

    match store_type:
        case VectorStoreEnum.CHROMADB:
            return ChromaVectorStore(
                embedder=embedder,
                collection_name=collection_name,
            )
        case _:
            raise ValueError(f"{store_type} vector store is not supported.")
