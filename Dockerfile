FROM python:3.11

WORKDIR /app

COPY demo/requirements.txt demo/

RUN pip install --pre -U --no-cache-dir -r demo/requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "demo/app.py", "--server.port", "8501", "--server.fileWatcherType", "none"]
