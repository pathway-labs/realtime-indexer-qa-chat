from dotenv import load_dotenv
from llama_index.chat_engine.condense_plus_context import \
    CondensePlusContextChatEngine
from llama_index.llms.types import ChatMessage, MessageRole
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import PathwayRetriever
from pathway.xpacks.llm.vector_store import VectorStoreClient

PATHWAY_HOST = "api-pathway-indexer.staging.deploys.pathway.com"
PATHWAY_PORT = 80

vector_client = VectorStoreClient(PATHWAY_HOST, PATHWAY_PORT)

load_dotenv()

retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)

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
    system_prompt="IF QUESTION IS NOT RELATED TO CONTEXT DOCUMENTS, SAY IT'S NOT POSSIBLE TO ANSWER USING PHRASE `The looked-up documents do not provde information about...`",
    verbose=True,
    chat_history=DEFAULT_MESSAGES,
)
