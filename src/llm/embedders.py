import boto3
from langchain_aws import BedrockEmbeddings
from langchain_core.embeddings import Embeddings

from src.settings.base import settings


class BaseEmbedder(Embeddings):
    """Base class for embedders."""

    embedder: Embeddings

    def embed_query(self, text: str) -> list[float]:
        result = self.embedder.embed_query(text)
        return result

    def embed_documents(self, texts: list) -> list[list[float]]:
        result = self.embedder.embed_documents(texts)
        return result


class AWSBedrockEmbedder(BaseEmbedder):
    """AWS Bedrock Embedder."""

    def __init__(self) -> None:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.aws.region,
        )

        self.embedder = BedrockEmbeddings(
            client=bedrock_client,
            model_id=settings.aws.bedrock_embeddings_model,
            region_name=settings.aws.region,
        )
