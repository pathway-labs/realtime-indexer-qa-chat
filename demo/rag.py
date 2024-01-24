from dotenv import load_dotenv
from llama_index.chat_engine.condense_plus_context import \
    CondensePlusContextChatEngine
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import PathwayRetriever

PATHWAY_HOST = "api-pathway-indexer.staging.deploys.pathway.com"
PATHWAY_PORT = 80

load_dotenv()

retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)

query_engine = RetrieverQueryEngine.from_args(
    retriever,
)


chat_engine = CondensePlusContextChatEngine.from_defaults(
    retriever=retriever,
    system_prompt="IF QUESTION IS NOT RELATED TO CONTEXT DOCUMENTS, SAY IT'S NOT POSSIBLE TO ANSWER.",
    verbose=True,
)
