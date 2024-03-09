FROM python:3.11

WORKDIR /app

RUN git clone https://github.com/pathway-labs/realtime-indexer-qa-chat.git
WORKDIR /app/realtime-indexer-qa-chat

RUN pip install --pre -U --no-cache-dir -r demo/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "demo/app.py", "--server.port", "8501", "--server.fileWatcherType", "none"]
