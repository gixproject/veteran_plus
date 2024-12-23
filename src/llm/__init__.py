from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from src.common.enums import LLMProviderEnum
from src.llm.embedders import BaseEmbedder, AWSBedrockEmbedder
from src.settings.base import settings


def create_embedder(
    provider: LLMProviderEnum,
) -> BaseEmbedder:
    """Returns embedder for the specified provider."""

    match provider:
        case LLMProviderEnum.BEDROCK:
            return AWSBedrockEmbedder()
        case _:
            raise ValueError("Invalid provider type.")


def create_chat_model(
    provider: LLMProviderEnum,
    temperature: float = 0.5,
) -> BaseChatModel:
    """Returns chat model for the specified provider."""
    match provider:
        case LLMProviderEnum.BEDROCK:
            return init_chat_model(
                model=settings.aws.bedrock_chat_model,
                model_provider="bedrock",
                region=settings.aws.region,
                temperature=temperature,
            )
        case _:
            raise ValueError("Invalid provider type.")
