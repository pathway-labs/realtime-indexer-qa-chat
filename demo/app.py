import streamlit as st
from dotenv import load_dotenv

with st.sidebar:
    st.markdown(
        "[View the source code on GitHub](https://github.com/pathwaycom/pathway)"
    )

    st.markdown(
        """
        This demo showcases Pathway pipeline that is connected to a Google Drive Folder and Sharepoint. Pathway LlamaIndex integration powers the rag application by providing synced files to LLM. To see more about Pathway's LlamaIndex integration, see more about it in [this blog post](https://pathway.com/developers/showcases/llamaindex-pathway/) and LlamaIndex docs [Pathway Reader](https://docs.llamaindex.ai/en/stable/examples/data_connectors/PathwayReaderDemo.html#pathway-reader), [Pathway Retriever docs](https://docs.llamaindex.ai/en/stable/examples/retrievers/pathway_retriever.html#pathway-retriever).
        """
    )

    st.markdown(
        "Check out Pathway hosted index on [Pathway Indexer](https://pathway-indexer.staging.deploys.pathway.com/)"
    )

    st.markdown("""Add your documents 📄📩 to [Drive Folder](https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) 
                or [Sharepoint](https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05)""")

# Load environment variables
load_dotenv()


# Streamlit UI elements
st.title("Pathway 😺 + LlamaIndex 🦙")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, ask me a question. My knowledge is always up to date!",
        }
    ]
    from rag import chat_engine

    st.session_state.chat_engine = chat_engine


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
