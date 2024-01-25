import streamlit as st
from dotenv import load_dotenv

with st.sidebar:
    st.markdown(
        "[View code on GitHub.](https://github.com/pathwaycom/pathway)"
    )

    st.markdown(
        """Pathway pipelines ingest documents from [Google Drive](https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) and [Sharepoint](https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05). It automatically manages and syncs indexes enabling RAG applications."""
    )

    st.markdown(
        """Ready to build your own? 

Our [docs](https://pathway.com/developers/showcases/llamaindex-pathway/) walk through creating custom pipelines with LlamaIndex.

Want a hosted version?

Check out our [hosted document pipelines](https://pathway-indexer.staging.deploys.pathway.com/)."""
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

htm = """
<div style="display: flex; ">
  <a href="https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs">
    <figure style="text-align: center; margin-right: 10px;">
      <img src="./app/static/Google_Drive_logo.png" width="50" alt="Google Drive Logo">
      <figcaption>Upload to Google Drive</figcaption>
    </figure>
  </a>

  <a href="https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05">
    <figure style="text-align: center;">
      <img src="./app/static/sharepoint.png" width="50" alt="Google Drive Logo">
      <figcaption>Upload to Sharepoint</figcaption>
    </figure>
  </a>
</div>
"""

st.markdown(htm, unsafe_allow_html=True)


if "messages" not in st.session_state.keys():
    from rag import chat_engine

    st.session_state.messages = [{'role': msg.role, 'content': msg.content} for msg in chat_engine.chat_history]


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
