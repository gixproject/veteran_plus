from abc import ABC, abstractmethod

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from src.settings.base import settings


class BaseVectorStore(ABC):
    """Abstract base class for vector stores to define
    basic methods.
    """

    client: VectorStore

    persist_directory = (
        settings.common.persist_storages_path / settings.common.vector_store.value / settings.common.provider.value
    )

    def __init__(self, embedder: Embeddings, collection_name: str):
        self.embedder = embedder
        self.collection_name = collection_name

    @abstractmethod
    def add_sample(self, text: str) -> None:
        """Add a single sample to the vector store."""

    @abstractmethod
    def search(self, query: str, n_results: int) -> list[Document]:
        """Abstract method to search for vectors in the vector store."""

    @abstractmethod
    def get_context(self, query: str, n_results: int = 3) -> str:
        """Retrieve relevant context from a vector store for a given query."""
