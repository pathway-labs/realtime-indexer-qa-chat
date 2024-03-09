
# Build a chatbot with always updated data sources using Pathway + LlamaIndex + Streamlit

## Subtitle: Create a RAG application without a Vector DB, ETL pipelines or separate backend!


In this post, we explore how to build a RAG application that always has up-to-date information from your documents and sources stored in Google Drive, Dropbox, Sharepoint and more. 


## What is Pathway
Pathway is an open data processing framework. It allows you to easily develop data transformation pipelines and Machine Learning applications that work with live data sources and changing data. Pathway listens to our documents for changes, additions or removals. It handles loading and indexing without the need for an ETL. Specifically, we will use Pathway hosted offering that makes it particularly easy to launch advanced RAG applications with very little overhead.

(Meta note) select one:
- In this demo, you will use Pathway with LlamaIndex with Pathway's LlamaIndex integration which makes it particularly easy to create chatbots that have memory and can access our documents.

- In this demo, you will use LlamaIndex with the Pathway's LlamaIndex integration, and Pathway hosted index solution. Using Pathway and LlamaIndex is a quick way to create powerful chatbots that have memory and can access our documents.

- In this blog, we showcase the integration of LlamaIndex with Pathway's hosted index solution. You can effortlessly develop advanced chatbots with memory capabilities, providing easy real-time access to your documents.

## Why Pathway?

Pathway offers an indexing solution that is always up to date without the need for traditional ETL pipelines, which are needed in regular VectorDBs. It can monitor several data sources (files, S3 folders, cloud storage) and provide the latest information to your LLM application. 

This means you do not need to worry about:
- Checking files to see if there are any changes
- Parsing PDFs, word documents or other text files
- Transforming, embedding documents and loading them into a vector database

These are all handled by Pathway.

## App Overview

This demo consists of three parts. For always up-to-date knowledge and information retrieval from the documents in our folders, Pathway vector store is used.
LlamaIndex provides search capability to OpenAI LLM and combines functionalities such as chat memory, and OpenAI API calls for the app. Finally, Streamlit powers the easy-to-navigate user interface for easy access to the app.


## Tutorial: Creating always up-to-date RAG app with Pathway + LlamaIndex

```
Want to jump right in? Check out the app and the [code](https://github.com/pathway-labs/realtime-indexer-qa-chat).
```

## Prerequisites
- An OpenAI API Key (Only needed for OpenAI models)
- Pathway instance (Hosted version is provided free for the demo)

## Adding data to source
First, add example documents to your pipeline by uploading files to Google Drive that is registered to Pathway as a source. Pathway can listen to many sources simultaneously, such as local files, S3 folders, cloud storage and any data stream for data changes. For this demo, a Google Drive folder is provided for you to upload files. There is Pathway Github repository's readme that is provided in the folder. In this demo, we will ask our questions about Pathway our assistant and it will respond based on the available files in the Drive folder.

See [pathway-io](https://pathway.com/developers/api-docs/pathway-io) for more information on available connectors and how to implement custom connectors.

## Building Pathway Powered Chat Bot

### Retriever
First, import the necessary modules for the retriever.

```python
from llama_index.retrievers import PathwayRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.chat_engine.condense_question import CondenseQuestionChatEngine
```

Then, initialize the retriever with the hosted Pathway instance and create query engine:

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

Then,  print the messages both from the user and the assistant. Streamlit works in a way that resembles running a script, the whole file will be running each time there is a change in components, and the session state is the only component that has states. Making it powerful for saving and keeping elements that do not need to be re-initialized. That is why, all messages are printed iteratively.

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


## Running the App

### On Streamlit Community Cloud


### On your local machine

Clone this repository to your machine.
Create a `.env` file under the root folder, this will store your OpenAI API key, demo uses the OpenAI GPT model to answer questions.

You need a Pathway instance for vector search, for local deployment see the [vector store guide](https://pathway.com/developers/showcases/vectorstore_pipeline) and also [Pathway Deployment](https://pathway.com/developers/user-guide/deployment/docker-deployment). 

### With Docker

If you are on Windows or, you want to run the vector store in a `Docker` image, refer to [Document Indexing with Docker](https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/demo-document-indexing#running-with-docker), Docker file is provided [`here`](https://github.com/pathwaycom/llm-app/blob/main/examples/pipelines/demo-document-indexing/Dockerfile). 

Note that, if you want to create RAG application on your Google Drive, you need to set up a Google Service account, [refer to the instructions here](https://github.com/pathwaycom/llm-app/blob/main/examples/pipelines/demo-question-answering/README.md#create-a-new-project-in-the-google-api-console).
If you are not planning to use local files in your app, you can skip the `binding local volume` part explained in the llm-app instructions provided above. 

### Pathway hosted

For this demo, a free instance is provided that reads documents in [Google Drive](https://drive.google.com/drive/u/2/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) and [Sharepoint](https://navalgo.sharepoint.com/:f:/s/ConnectorSandbox/EgBe-VQr9h1IuR7VBeXsRfIBuOYhv-8z02_6zf4uTH8WbQ?e=YmlA05).

Open a terminal and run `streamlit run ui.py`. This will prompt you a URL, simply click and open the demo.

Congrats! Now you are ready to chat with your documents with updated knowledge provided by Pathway.

## Summing Up

In this tutorial, you learned how to create and deploy a simple yet powerful RAG application with always up-to-date knowledge of your documents, without ETL jobs and buffers to check and read documents for any changes. You also learned how to get started with LlamaIndex using Pathway vector store, and how easy it is to get going with hosted Pathway that handles the majority of hurdles for you.