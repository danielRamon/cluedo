FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt update && apt -y upgrade && apt -y install curl
RUN curl -fsSL https://ollama.com/install.sh | sh
ENV OLLAMA_HOME=/app/.ollama
RUN ollama start & OLLAMA_PID=$! ; ollama pull gemma2 ; kill $OLLAMA_PID
EXPOSE 8501
COPY streamlit_app.py generate_players.py resources/* ./
CMD ollama start & streamlit run streamlit_app.py