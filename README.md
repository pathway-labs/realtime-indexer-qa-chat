# Build a chatbot with always updated data sources using Pathway + LlamaIndex + Streamlit

## Create a RAG App without a Vector DB or fragmented ETL pipelines!

This repository will show you how to build a RAG App that always has up-to-date information from your documents and sources stored in Google Drive, Dropbox, Sharepoint and more. 

The setup guide below describes how to build your **App**. You then connect your App to a public **Pathway Vector Store**  sandbox, which is in sync with some public Google Drive and Sharepoint folders. Here, you can upload your own non-confidential files, and try out the App with the sandbox. Finally, we will show you how to quickly spin up your very own Pathway Vector Store which is kept in sync with your own private folders. 

> ℹ To run the full solution (your very own Pathway Vector Store + App) in a single go in production, with your own private folders, we recommend using this complete [🐋 Dockerized setup 🐋](https://github.com/pathwaycom/llm-app/blob/main/examples/pipelines/demo-document-indexing/README.md) directly.

## What is Pathway
Pathway is an open data processing framework. It allows you to easily develop data transformation pipelines and Machine Learning applications that work with live data sources and changing data. Pathway listens to our documents for changes, additions or removals. It handles loading and indexing without the need for an ETL. Specifically, we will use Pathway hosted offering that makes it particularly easy to launch advanced RAG applications with very little overhead.

In this repository, we showcase the integration of LlamaIndex with Pathway's Vector Store solution. You can effortlessly develop advanced chatbots with memory capabilities, providing easy real-time access to your documents. The instructions below are intended as a step-by-step tutorial for learning. 

## Why Pathway?

Pathway is a data processing framework allowing easy building of advanced data processing pipelines. Among others, it offers [Pathway Vector Store](https://pathway.com/developers/user-guide/llm-xpack/vectorstore_pipeline/), a document indexing solution that is always up to date without the need for traditional ETL pipelines, which are needed in regular VectorDBs. It can monitor several data sources (files, S3 folders, cloud storage) and provide the latest information to your LLM application. 

This means you do not need to worry about:
- Checking files to see if there are any changes
- Parsing PDFs, word documents or other text files
- Transforming, embedding documents and loading them into a vector database

These are all handled by Pathway.

## App Overview

This demo combines three technologies.
* For always up-to-date knowledge and information retrieval from the documents in our folders, **Pathway Vector Store** is used.
* **LlamaIndex** provides search capability to OpenAI LLM and combines functionalities such as chat memory, and OpenAI API calls for the app.
* Finally, **Streamlit** powers the easy-to-navigate user interface for easy access to the app.

## Tutorial: Creating always up-to-date RAG App with Pathway Vector Store + LlamaIndex

## Prerequisites
- An OpenAI API Key (Only needed for OpenAI models)
- Running Pathway Vector Store process (a hosted version is provided for the demo, instructoins to self-host one are provided below)

## Adding new documents
First, add example documents to the vector store by uploading files to Google Drive that is registered to Pathway Vector Store as a source. Pathway can listen to many sources simultaneously, such as local files, S3 folders, cloud storage and any data stream for data changes. For this demo, a public Google Drive folder is provided for you to upload file. It is pre-populated with Pathway Github repository's readme. In this demo, we will ask questions about Pathway to our assistant and it will respond based on the available files in the Drive folder.

See [pathway-io](https://pathway.com/developers/api-docs/pathway-io) for more information on available connectors and how to implement custom connectors.

## Building Pathway Powered Chat Bot

### Retriever
First, import the necessary modules for the retriever.

```python
from llama_index.retrievers import PathwayRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.chat_engine.condense_question import CondenseQuestionChatEngine
```

Then, initialize the retriever with the chosen Pathway Vector Store instance (for an easy start we point to the managed instance) and create the query engine:

```python
PATHWAY_HOST = "https://api-pathway-indexer.staging.deploys.pathway.com"
PATHWAY_PORT = ''

retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)

query_engine = RetrieverQueryEngine.from_args(
    retriever,
)
```

### Chat Engine
We use `CondenseQuestionChatEngine`, one advantage of this chat engine is that, it writes the search query smartly based on the conversation history.

For example, if the user is chatting about `Pathway` and asks a question such as `What are some of the advantages?`, the search query will be based on `Pathway's advantages` making the pipeline more optimized for retrieval. 

For further improvements on the pipeline, it is possible to modify chat engine type, prompt and other parameters. For simplicity, let's keep things default.

```python
chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
    verbose=True,
)
```

### Why Streamlit?
It is easy to set up and get started with Streamlit UI, making it a good choice for prototyping and testing LLM applications. Another reason is that the LlamaIndex chat engine allows easy integration with Streamlit elements.

### Creating the UI with Streamlit

First, create a title for the app and initialize the chat engine:

```python
st.title("Pathway + LlamaIndex")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, ask me a question. My knowledge is always up to date!"}
    ]
    from rag import chat_engine
    st.session_state.chat_engine = chat_engine
```

When the app is first run, `messages` will not be in the `st.session_state` and it will be initialized.

Then, print messages both from the user and the assistant. Streamlit works in a way that resembles running a script, the whole file will be running each time there is a change in components, and the session state is the only component that has states. Making it powerful for saving and keeping elements that do not need to be re-initialized. That is why, all messages are printed iteratively.

```python
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
```

Finally, when the last message is from `user`, meaning that the assistant is preparing an answer, create a spinning component that tells the user that the answer is being prepared. Then, add the message content and role to the messages list. 

```python
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)

```


## 1️⃣ Running the App

### On Streamlit Community Cloud

The demo is hosted on Streamlit Community Cloud [here](https://chat-realtime-sharepoint-gdrive.streamlit.app/). This version of the app uses Pathway's [hosted document pipelines](https://cloud.pathway.com/docindex).

### On your local machine

Clone this repository to your machine.
Create a `.env` file under the root folder, this will store your OpenAI API key, demo uses the OpenAI GPT model to answer questions.

You need access to a running Pathway Vector Store pipeline. For this demo, a public instance is provided that reads documents in [Google Drive](https://drive.google.com/drive/u/2/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) and [Sharepoint](https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05). However, it is easy to run our own locally. Please see the [vector store guide](https://pathway.com/developers/showcases/vectorstore_pipeline) and also [Pathway Deployment](https://pathway.com/developers/user-guide/deployment/docker-deployment). 

Open a terminal and run `streamlit run ui.py`. This will prompt you a URL, simply click and open the demo.

Congrats! Now you are ready to chat with your documents with updated knowledge provided by Pathway.

### Running with Docker

We provide a Dockerfile to run the application. From the root folder of the repository run 

```
docker build -t realtime_chat .
docker run -p 8501:8501 realtime_chat
```

We recommend running in docker when working on a Windows machine.

## 2️⃣ Running a local Pathway Vector Store

OK, so far you have managed to get the RAG App and running and it's working - but it still connects to the public demo folders! Let's fix that - we will now show you how to connect your very own folders, in a private deployment. This means you will need to spin up a light web server which provides the "Pathway Vector Store" service, responsible for the whole document ingestion and indexing pipeline.

The code for the Pathway Vector Store pipeline, along with a Dockerfile is provided in the [Pathway LLM examples repository](https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/demo-document-indexing). Please follow instructions to run only the vector store pipeline, or to run the pipeline and the Streamlit UI as a joint deployment using `docker compose`.

Note that if you want to create a RAG application connected to your Google Drive, you need to set up a Google Service account, [refer to the instructions here](https://github.com/pathwaycom/llm-app/blob/main/examples/pipelines/demo-question-answering/README.md#create-a-new-project-in-the-google-api-console).
Also, if you are not planning to use local files in your app, you can skip the `binding local volume` part explained in the llm-app instructions linked above. 

## Summing Up

In this tutorial, you learned how to create and deploy a simple yet powerful RAG application with always up-to-date knowledge of your documents, without ETL jobs and buffers to check and read documents for any changes. You also learned how to get started with LlamaIndex using Pathway vector store, and how easy it is to get going with hosted Pathway that handles the majority of hurdles for you.
