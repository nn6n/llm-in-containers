#!/bin/bash
set -e -u

docker build -t rag-retrievers:1.0 .
docker run --env-file=./src/streamlit-web/.env -p 8501:8501 -d --name rag-retrievers rag-retrievers:1.0 