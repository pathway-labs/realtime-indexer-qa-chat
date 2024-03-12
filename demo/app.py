import json
import logging
import os
import uuid

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from endpoint_utils import get_inputs
from llama_index.llms.types import ChatMessage, MessageRole
from log_utils import init_pw_log_config
from rag import DEFAULT_PATHWAY_HOST, PATHWAY_HOST, chat_engine, vector_client
from streamlit.web.server.websocket_headers import _get_websocket_headers
from traceloop.sdk import Traceloop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

init_pw_log_config()

DRIVE_URL = os.environ.get(
    "GDRIVE_FOLDER_URL",
    "https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs",
)
htm = f"""
<div style="display: flex; align-items: center; vertical-align: middle">
    <a href="{DRIVE_URL}" style="text-decoration:none;">
      <figure style="display: flex; vertical-align: middle; margin-right: 20px; align-items: center;">
        <img src="./app/static/Google_Drive_logo.png" width="30" alt="Google Drive Logo">
        <figcaption>Upload</figcaption>
      </figure>
    </a>
    <a href="https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05" style="text-decoration:none;">
      <figure style="display: flex; vertical-align: middle; align-items: center; margin-right: 20px;">
        <img src="./app/static/sharepoint.png" width="30" alt="Google Drive Logo">
        <figcaption>Upload</figcaption>
      </figure>
    </a>
</div>
<div style="font-size: 10px">* These are public folders. Please do not upload confidential files.</div>
<div><br></div>
<a href="https://cloud.pathway.com/?modal=getstarted" style="text-decoration:none;">
    <figure style="display: flex; vertical-align: middle; align-items: center; margin-right: 20px;">
    <button>Connect to your folders with Pathway</button>
    </figure>
</a>
"""

st.set_page_config(
    page_title="Realtime Document AI pipelines", page_icon="./app/static/favicon.ico"
)

with st.sidebar:
    if PATHWAY_HOST == DEFAULT_PATHWAY_HOST:
        st.markdown("**Add Your Files**")

        st.markdown(htm, unsafe_allow_html=True)

        st.markdown("\n\n\n\n\n\n\n")
        st.markdown("\n\n\n\n\n\n\n")
        st.markdown(
            "[View code on GitHub.](https://github.com/pathway-labs/chat-realtime-sharepoint-gdrive)"
        )
        st.markdown(
            """Pathway pipelines ingest documents from [Google Drive](https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) and [Sharepoint](https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05) simultaneously. It automatically manages and syncs indexes enabling RAG applications."""
        )
    else:
        st.markdown(f"**Connected to:** {PATHWAY_HOST}")
        st.markdown(
            "[View code on GitHub.](https://github.com/pathway-labs/chat-realtime-sharepoint-gdrive)"
        )

    st.markdown(
        """**Ready to build your own?**

Our [docs](https://pathway.com/developers/showcases/llamaindex-pathway/) walk through creating custom pipelines with LlamaIndex.

**Want a hosted version?**

Check out our [hosted document pipelines](https://cloud.pathway.com/docindex)."""
    )


# Load environment variables
load_dotenv()


# Streamlit UI elements
st.write(
    "## Chat with all your enterprise documents realtime ⚡ in Google Drive & Sharepoint"
)


htt = """
<p>
    <span> Built With: </span>
    <img src="./app/static/combinedhosted.png" width="300" alt="Google Drive Logo">
</p>
"""
st.markdown(htt, unsafe_allow_html=True)


image_width = 300
image_height = 200


if "messages" not in st.session_state.keys():
    if "session_id" not in st.session_state.keys():
        session_id = "uuid-" + str(uuid.uuid4())

        logging.info(json.dumps({"_type": "set_session_id", "session_id": session_id}))
        Traceloop.set_association_properties({"session_id": session_id})
        st.session_state["session_id"] = session_id

    headers = _get_websocket_headers()
    logging.info(
        json.dumps(
            {
                "_type": "set_headers",
                "headers": headers,
                "session_id": st.session_state.get("session_id", "NULL_SESS"),
            }
        )
    )

    pathway_explaination = "Pathway is a high-throughput, low-latency data processing framework that handles live data & streaming for you."
    DEFAULT_MESSAGES = [
        ChatMessage(role=MessageRole.USER, content="What is Pathway?"),
        ChatMessage(role=MessageRole.ASSISTANT, content=pathway_explaination),
    ]
    chat_engine.chat_history.clear()

    for msg in DEFAULT_MESSAGES:
        chat_engine.chat_history.append(msg)

    st.session_state.messages = [
        {"role": msg.role, "content": msg.content} for msg in chat_engine.chat_history
    ]
    st.session_state.chat_engine = chat_engine
    st.session_state.vector_client = vector_client


results = get_inputs()

last_modified_time, last_indexed_files = results


df = pd.DataFrame(last_indexed_files, columns=[last_modified_time, "status"])
if df.status.isna().any():
    del df["status"]

df.set_index(df.columns[0])
st.dataframe(df, hide_index=True, height=150, use_container_width=True)

cs = st.columns([1, 1, 1, 1], gap="large")

with cs[-1]:
    st.button("⟳ Refresh", use_container_width=True)


if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    logging.info(
        json.dumps(
            {
                "_type": "user_prompt",
                "prompt": prompt,
                "session_id": st.session_state.get("session_id", "NULL_SESS"),
            }
        )
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)

            sources = []

            try:
                for source in response.source_nodes:
                    full_path = source.metadata.get("path", source.metadata.get("name"))
                    if full_path is None:
                        continue
                    if "/" in full_path:
                        name = f"`{full_path.split('/')[-1]}`"
                    else:
                        name = f"`{full_path}`"
                    if name not in sources:
                        sources.append(name)
            except AttributeError:
                logging.error(
                    json.dumps(
                        {
                            "_type": "error",
                            "error": f"No source (`source_nodes`) was found in response: {str(response)}",
                            "session_id": st.session_state.get(
                                "session_id", "NULL_SESS"
                            ),
                        }
                    )
                )

            sources_text = ", ".join(sources)

            logging.info(
                json.dumps(
                    {
                        "_type": "llm_response",
                        "response": str(response),
                        "session_id": st.session_state.get("session_id", "NULL_SESS"),
                        "sources": sources,
                    }
                )
            )

            response_text = (
                response.response
                + f"\n\nDocuments looked up to obtain this answer: {sources_text}"
            )

            st.write(response_text)

            message = {"role": "assistant", "content": response_text}
            st.session_state.messages.append(message)
