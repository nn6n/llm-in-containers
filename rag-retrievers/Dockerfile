FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt


COPY data data
COPY db_stores db_stores
COPY models models
# COPY prompt_bank prompt_bank
COPY src src

RUN cd /app/src/streamlit-web
CMD ["streamlit", "run", "src/streamlit-web/demo.py"]