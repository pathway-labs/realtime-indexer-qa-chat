import os

from dotenv import load_dotenv
from llama_index.chat_engine.condense_plus_context import CondensePlusContextChatEngine
from llama_index.llms.openai import OpenAI
from llama_index.llms.types import ChatMessage, MessageRole
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import PathwayRetriever
from traceloop.sdk import Traceloop

from pathway.xpacks.llm.vector_store import VectorStoreClient

load_dotenv()


Traceloop.init(app_name=os.environ.get("APP_NAME", "PW - LlamaIndex (Streamlit)"))

DEFAULT_PATHWAY_HOST = "demo-document-indexing.pathway.stream"

PATHWAY_HOST = os.environ.get("PATHWAY_HOST", DEFAULT_PATHWAY_HOST)

PATHWAY_PORT = int(os.environ.get("PATHWAY_PORT", "80"))


def get_additional_headers():
    headers = {}
    key = os.environ.get("PATHWAY_API_KEY")
    if key is not None:
        headers = {"X-Pathway-API-Key": key}
    return headers


vector_client = VectorStoreClient(
    PATHWAY_HOST,
    PATHWAY_PORT,
    additional_headers=get_additional_headers(),
)


retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)
retriever.client = VectorStoreClient(
    host=PATHWAY_HOST, port=PATHWAY_PORT, additional_headers=get_additional_headers()
)

llm = OpenAI(model="gpt-3.5-turbo")

query_engine = RetrieverQueryEngine.from_args(
    retriever,
)

pathway_explaination = "Pathway is a high-throughput, low-latency data processing framework that handles live data & streaming for you."
DEFAULT_MESSAGES = [
    ChatMessage(role=MessageRole.USER, content="What is Pathway?"),
    ChatMessage(role=MessageRole.ASSISTANT, content=pathway_explaination),
]

chat_engine = CondensePlusContextChatEngine.from_defaults(
    retriever=retriever,
    system_prompt="""You are RAG AI that answers users questions based on provided sources.
    IF QUESTION IS NOT RELATED TO ANY OF THE CONTEXT DOCUMENTS, SAY IT'S NOT POSSIBLE TO ANSWER USING PHRASE `The looked-up documents do not provde information about...`""",
    verbose=True,
    chat_history=DEFAULT_MESSAGES,
    llm=llm,
)
