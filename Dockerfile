FROM python:3.13-slim

WORKDIR /usr/src/app
RUN pip install --no-cache-dir pandas numpy sentence-transformers gradio python-dotenv chromadb
COPY . .
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "first.py"]