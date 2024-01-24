from dotenv import load_dotenv
from llama_index.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import PathwayRetriever

PATHWAY_HOST = "api-pathway-indexer.staging.deploys.pathway.com"
PATHWAY_PORT = 80

load_dotenv()

retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)

query_engine = RetrieverQueryEngine.from_args(
    retriever,
)

chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
    verbose=True,
)
