import logging.config

import streamlit as st
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from src.common.enums import LLMProviderEnum
from src.llm import create_embedder, create_chat_model
from src.llm.constants import INITIAL_PROMPT, BOT_DESCRIPTION
from src.llm.embedders import BaseEmbedder
from src.settings.base import settings
from src.settings.logging import logging_config
from src.stores import create_vector_store
from src.stores.base import BaseVectorStore

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

# Global config
TEMPERATURE = 0.5
st.set_page_config(
    page_title="Veteran+ Chat",
    page_icon="🤖",
)


# -------------------- Init resources --------------------


@st.cache_resource
def get_embedder() -> BaseEmbedder:
    return create_embedder(provider=settings.common.provider)


@st.cache_resource
def get_vector_store(_embedder: BaseEmbedder) -> BaseVectorStore:
    return create_vector_store(
        embedder=_embedder,
        store_type=settings.common.vector_store,
        collection_name=settings.common.collection_name,
    )


@st.cache_resource
def get_llm_model(provider: LLMProviderEnum = settings.common.provider, temperature: float = 0.5) -> BaseChatModel:
    return create_chat_model(provider=provider, temperature=temperature)


embedder = get_embedder()
vector_store = get_vector_store(_embedder=embedder)
llm = get_llm_model(provider=LLMProviderEnum.BEDROCK, temperature=TEMPERATURE)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", INITIAL_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ],
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
output_parser = StrOutputParser()
rag_chain = create_retrieval_chain(vector_store.client.as_retriever(), question_answer_chain)
# що ти знаєш про е-ветеран?

# Initialize langchain chain with history
history = StreamlitChatMessageHistory(key="chat_messages")

history_chain = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history",
    verbose=settings.common.debug,
)


def clear_chat_history():
    history.messages.clear()


# -------------------- Streamlit --------------------

st.header("Hello in the Veteran+! Let's chat 👋")
st.write(BOT_DESCRIPTION)

# Chat history sidebar
with st.sidebar:
    st.button("+ New chat", on_click=clear_chat_history, type="secondary")
    st.subheader("Recent chats")
    st.write("Not available now (in development)")
    st.divider()

    # Allows to change temperature
    st.subheader("Bot settings")
    new_temperature: float = st.slider("Creativity", min_value=0.0, max_value=1.0, value=TEMPERATURE, step=0.1)
    st.divider()

# Display first message from AI
if not history.messages:
    history.add_ai_message("How may I assist you today?")

# Render current messages from StreamlitChatMessageHistory
for msg in history.messages:
    st.chat_message(msg.type).write(msg.content)

# Chat input handler
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    config = {"configurable": {"session_id": "any", "temperature": new_temperature}}

    # Chain - Stream
    placeholder = st.empty()
    full_response = ""

    # start = time.time()
    for chunk in history_chain.stream({"input": prompt}, config):
        full_response += chunk.get("answer", "")
        placeholder.chat_message("ai").write(full_response)

    # logger.info("LLM invoke time: %s", time.time() - start)
    placeholder.chat_message("ai").write(full_response)
