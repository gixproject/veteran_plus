from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings as _BaseSettings

from src.common.enums import LLMProviderEnum, VectorStoreEnum


class BaseSettings(
    _BaseSettings,
    env_file=".env",
    extra="ignore",
):
    pass


class CommonSettings(BaseSettings):
    debug: bool
    collection_name: str = "veteran_plus"
    provider: LLMProviderEnum
    vector_store: VectorStoreEnum

    training_data_path: Path = Path(__file__).parent.parent.parent / "resources"
    persist_storages_path: Path = Path(__file__).parent.parent.parent / ".stores"


class AWSSettings(BaseSettings, env_prefix="aws_"):
    region: str
    bedrock_chat_model: str
    bedrock_embeddings_model: str


class Settings(BaseSettings):
    # Specific services settings
    aws: AWSSettings = Field(default_factory=AWSSettings)  # type: ignore[arg-type]
    common: CommonSettings = Field(default_factory=CommonSettings)  # type: ignore[arg-type]


settings = Settings()
