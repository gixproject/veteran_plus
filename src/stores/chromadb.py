import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.stores.base import BaseVectorStore

logger = logging.getLogger(__name__)


class ChromaVectorStore(BaseVectorStore):
    client: Chroma

    def __init__(self, embedder: Embeddings, collection_name: str = "default"):
        super().__init__(embedder=embedder, collection_name=collection_name)

        self.client = Chroma(
            embedding_function=self.embedder,
            collection_name=self.collection_name,
            persist_directory=str(self.persist_directory),
        )

    def search(self, query: str, n_results: int = 5) -> list[Document]:
        results = self.client.similarity_search(query, k=n_results)
        return results

    def add_sample(self, text: str) -> None:
        self.client.add_texts([text])
        logger.info(f"Added sample to vector store: {text}")

    def get_context(self, query: str, n_results: int = 3) -> str:
        """Retrieve relevant context from ChromaDB for a given query."""

        search_results = self.client.similarity_search(query, k=n_results)

        # Extract context from search results
        context = "\n".join([doc.page_content for doc in search_results])
        return context
