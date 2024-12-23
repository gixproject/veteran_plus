import asyncio
import logging.config
from functools import wraps

import typer
from rich import print as rprint

from src.llm import create_embedder
from src.settings.base import settings
from src.settings.logging import logging_config
from src.stores import create_vector_store
from src.trainers.web import AsyncHtmlLoader

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

app = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command()
@coro
async def main(file_name: str) -> None:
    """Loads training data into vector store."""

    embedder = create_embedder(provider=settings.common.provider)
    vector_store = create_vector_store(
        store_type=settings.common.vector_store,
        embedder=embedder,
        collection_name=settings.common.collection_name,
    )

    file_path = settings.common.training_data_path / file_name

    with open(file_path) as file:
        urls = file.readlines()

    urls = [url.strip() for url in urls]

    loader = AsyncHtmlLoader(
        urls=urls,
        vector_store=vector_store,
    )
    await loader.load()

    rprint("[green]Data successfully loaded.[/green]")


if __name__ == "__main__":
    asyncio.run(app())
