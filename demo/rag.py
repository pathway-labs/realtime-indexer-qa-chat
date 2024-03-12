import os

from dotenv import load_dotenv
from llama_index.chat_engine.condense_plus_context import CondensePlusContextChatEngine
from llama_index.llms.openai import OpenAI
from llama_index.llms.types import ChatMessage, MessageRole
from llama_index.retrievers import PathwayRetriever
# from traceloop.sdk import Traceloop




from pathway.xpacks.llm.vector_store import VectorStoreClient

load_dotenv()


# Traceloop.init(app_name=os.environ.get("APP_NAME", "PW - LlamaIndex (Streamlit)"))

DEFAULT_PATHWAY_HOST = "demo-document-indexing.pathway.stream"

PATHWAY_HOST = os.environ.get("PATHWAY_HOST", DEFAULT_PATHWAY_HOST)

PATHWAY_PORT = int(os.environ.get("PATHWAY_PORT", "80"))



class ImportVariables:
    def __init__(self) -> None:
        vector_client = VectorStoreClient(PATHWAY_HOST, PATHWAY_PORT)
        self.vector_client = vector_client

        pathway_explaination = "Pathway is a high-throughput, low-latency data processing framework that handles live data & streaming for you."
        self.DEFAULT_MESSAGES = [
            ChatMessage(role=MessageRole.USER, content="What is Pathway?"),
            ChatMessage(role=MessageRole.ASSISTANT, content=pathway_explaination),
        ]

        self._init_chat_engine()

        self.DEFAULT_PATHWAY_HOST = DEFAULT_PATHWAY_HOST
        self.PATHWAY_HOST = PATHWAY_HOST

    def _init_chat_engine(self):
        retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)

        llm = OpenAI(model="gpt-3.5-turbo")

        self.chat_engine = CondensePlusContextChatEngine.from_defaults(
            retriever=retriever,
            system_prompt="""You are RAG AI that answers users questions based on provided sources.
            IF QUESTION IS NOT RELATED TO ANY OF THE CONTEXT DOCUMENTS, SAY IT'S NOT POSSIBLE TO ANSWER USING PHRASE `The looked-up documents do not provde information about...`""",
            verbose=True,
            chat_history=self.DEFAULT_MESSAGES,
            llm=llm,
        )

        # self.chat_engine.chat_history.clear()

        # for msg in self.DEFAULT_MESSAGES:
        #     self.chat_engine.chat_history.append(msg)


