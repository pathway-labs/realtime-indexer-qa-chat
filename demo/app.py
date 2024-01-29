import datetime
import sys
import time

import streamlit as st
from dotenv import load_dotenv

htm = """
<div style="display: flex; align-items: center; vertical-align: middle">
    <a href="https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs" style="text-decoration:none;">
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
<a href="https://pathway.com/?modal=getstarted" style="text-decoration:none;">
    <figure style="display: flex; vertical-align: middle; align-items: center; margin-right: 20px;">
    <button>Connect to your folders with Pathway</button>
    </figure>
</a>
"""


with st.sidebar:
    st.markdown("**Add Your Files**")
    st.markdown(htm, unsafe_allow_html=True)

    st.markdown("\n\n\n\n\n\n\n")
    st.markdown("\n\n\n\n\n\n\n")
    st.markdown("[View code on GitHub.](https://github.com/pathway-labs/chat-realtime-sharepoint-gdrive)")

    st.markdown(
        """Pathway pipelines ingest documents from [Google Drive](https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) and [Sharepoint](https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05). It automatically manages and syncs indexes enabling RAG applications."""
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
st.title("Chat with documents realtime ⚡ in Google Drive & Sharepoint")


htt = """
<p>
    <span> Built With: </span>
    <img src="./app/static/combinedhosted.png" width="300" alt="Google Drive Logo">
</p>
"""
st.markdown(htt, unsafe_allow_html=True)


image_width = 300
image_height = 200


def status_string() -> str:
    try:
        dt = st.session_state.vector_client.get_vectorstore_statistics()[
            "last_modified"
        ]
    except Exception as e:
        print(f"Failed to get status string: {e}", file=sys.stderr)
        return ""

    # If only static document collection is available, format a different str
    if time.time() - dt > 3600:
        return "No documents have been added by users yet"
    else:
        formatted_time = datetime.datetime.fromtimestamp(dt)
        return (
            f"Last document indexed at {formatted_time} UTC"
        )


if "messages" not in st.session_state.keys():
    from llama_index.llms.types import ChatMessage, MessageRole
    from rag import chat_engine, vector_client

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

    with st.sidebar:
        st.markdown(status_string())


if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)

    with st.sidebar:
        st.markdown(status_string())
