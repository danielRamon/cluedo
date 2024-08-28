FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt update && apt -y upgrade && apt -y install curl
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama start & sleep 5 & ollama pull gemma2
EXPOSE 8501
COPY streamlit_app.py generate_players.py resources/* ./
ENTRYPOINT ollama start & streamlit run streamlit_app.py