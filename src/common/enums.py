from enum import Enum


class VectorStoreEnum(Enum):
    CHROMADB = "chromadb"


class LLMProviderEnum(Enum):
    OPENAI = "openai"
    BEDROCK = "bedrock"
