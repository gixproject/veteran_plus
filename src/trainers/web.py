import logging

import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from src.stores.base import BaseVectorStore

logger = logging.getLogger(__name__)


class AsyncHtmlLoader:
    def __init__(
        self,
        urls: list[str],
        vector_store: BaseVectorStore,
    ):
        self.urls = urls
        self.vector_store = vector_store

    @staticmethod
    async def fetch_content(url: str) -> str | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.is_success:
                return response.text

        return None

    @staticmethod
    def _build_metadata(soup: BeautifulSoup, url: str) -> dict:
        """Build metadata from BeautifulSoup output."""

        metadata = {"source": url}
        if title := soup.find("title"):
            metadata["title"] = title.get_text()
        if description := soup.find("meta", attrs={"name": "description"}):
            metadata["description"] = description.get("content", "No description found.")
        if html := soup.find("html"):
            metadata["language"] = html.get("lang", "No language found.")
        return metadata

    async def parse_web_content(self, url: str) -> Document:
        content = await self.fetch_content(url)

        if content is None:
            logger.warning(f"Page {url} has no valid content. Skipping.")

        soup = BeautifulSoup(content, "html.parser")
        metadata = self._build_metadata(soup, url)

        paragraphs = soup.find_all("p")
        body = " ".join([p.get_text() for p in paragraphs])

        return Document(page_content=body, metadata=metadata)

    async def store_document(self, document: Document) -> None:
        await self.vector_store.client.add_documents([document])
        logger.info("Saved document: %s", document.metadata)

    async def load(self):
        """Load documents from web pages into vector store."""

        for url in self.urls:
            document = await self.parse_web_content(url)
            await self.store_document(document)
