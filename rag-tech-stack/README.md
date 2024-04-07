# RAG-TECH-STACK

## Overview

Through in-depth exploration of specific structured texts, we have found that retrievers with specific structures perform well when dealing with specific types of text and queries. However, their performance may not be as good as basic benchmark models when it comes to scenarios beyond these categories. This article will demonstrate the use of three different query engines for information retrieval, answering the same material from "The Legend of Zelda: Tears of the Kingdom", to showcase the different effects produced. To provide you with a more intuitive demonstration, we will compare the effects of three query engines based on:

Textual features (pure text tools or tabular tools)
Query intent (summary tools or vector tools)
Knowledge graph-based indexing

## Prerequisites

Before diving into this demo, please ensure that your system meets the following prerequisites:

Operating System: The demo is compatible with Linux operating systems and tested on Ubuntu 22.04.

Docker, unzip and wget: It's required to have docker installed on your system. Specifically, we have tested this demo with Docker Engine Community version 25.0.1 on Linux.

OpenAI API Key for ChatGPT: If you wish to use the ChatGPT functionality within this demo, an OpenAI API key is required. Please note that usage of this API is subject to OpenAI's pricing and usage policies.

## Quick Start

### Step-by-Step Instructions

1. git clone repo and cd into it
2. `conda create --name rag_zelda python=3.11`,`conda activate rag_zelda`
3. `pip install -r requirements.txt`
4. `mkdir models`
5. copy your `m3e-base` model to `models/`
6. `cd src/streamlit-web`
7. fill `<OPENAI-API-KEY>` with your own key in the `.env` file
8. run `streamlit run demo.py` in your cli

### Deploy using Docker

1. git clone repo and cd into it
2. `mkdir models`
3. copy your `m3e-base` model to `models/`
4. fill `<OPENAI-API-KEY>` with your own key in the `.env` file under `/src/streamlit-web`
5. `docker build -t my-image-name .`
6. `docker run --env-file=./src/streamlit-web/.env -p 8501:8501 my-image-name`
7. visit localhost:8501
