FROM python:3.10-slim-bullseye
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt update && apt -y upgrade && apt -y install curl
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama start & sleep 10 ; OLLAMA_PID=$! ; ollama pull gemma2 ; kill $OLLAMA_PID; mv /root/.ollama/ /.ollama
EXPOSE 8501
COPY streamlit_app.py generate_players.py resources/* ./
CMD ollama start & sleep 10 ; streamlit run streamlit_app.py