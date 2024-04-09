# Running Rag Retrievers on Docker Containers

## Overview

Through in-depth exploration of specific structured texts, we have found that retrievers with specific structures perform well when dealing with specific types of text and queries. However, their performance may not be as good as basic benchmark models when it comes to scenarios beyond these categories. This demo demonstrates the use of three different query engines for information retrieval, answering the same material from "The Legend of Zelda: Tears of the Kingdom" (Fan-made), showcasing the different effects produced.

Below are explanations of the three query engines:

- **Textual Features (Table+Text: Table-Tool & Text-Tool)**
  - Information retrieval is performed based on user queries using either table tools or text tools, and the results of multiple retrievals are integrated.
  - This query engine completely separates pure text and tabular data, enabling large models to consider data from two different sources while minimizing information conflicts as much as possible.
- **Query Intent (Document Agent: Summary_Tool & Vector_Tool)**
  - User query intent is analyzed. For general questions, simple keywords are set to guide the query and summary processing is performed to meet the requirements. For analytical or numerical queries, more rigorous and precise vector retrieval is used.
  - This query engine distinguishes user query intents, performing summary processing to meet general queries or requiring rigorous and precise retrieval.
- **Graph Rag (KGI-Based)**
  - Used to display output results in graph format and is suitable for complex entity relationships. Specific strategies based on knowledge graph indexing have not yet been experimented with, and further consideration will be given to related models.

## Prerequisites

Before diving into this demo, please ensure that your system meets the following prerequisites:

1. **Operating System**: The demo is compatible with Linux operating systems and tested on Ubuntu 22.04.
2. **Docker**: It's required to have `docker` installed on your system.
3. **OpenAI API Key for ChatGPT**: If you wish to use the ChatGPT functionality within this demo, an OpenAI API key is required. Please note that usage of this API is subject to OpenAI's pricing and usage policies. We use OpenAI text generation models to optimize the parsing of some special components like titles or tables etc. Without this API key, you can still try all three approaches.

## Quick Start

### Running the Zelda Demo

1. Start by cloning this repository to your instance with Docker installed:

   ```shell
   git clone https://github.com/LinkTime-Corp/llm-in-containers.git
   cd llm-in-containers/rag-retrievers
   ```

2. Replace `<YOUR-OPENAI-API-KEY>` with your own API key in the .env file under the `/src/streamlit-web` directory.

3. Launch the demo:

   ```shell
   bash run.sh
   ```

    Visit the UI at http://{IP of Host instance}:8501. On the UI, you can choose any of the three query engines - "Table+Text", "Document Agent", or "Graph Rag (KGI-Based)" to explore the actual query results for the material "The Legend of Zelda: Tears of the Kingdom" (Fan-made).

4. Shut down the demo:

   ```shell
   bash shutdown.sh
   ```

### Using Your Own Markdown Files

1. Start by cloning this repository to your instance with Docker installed:

   ```shell
   git clone https://github.com/LinkTime-Corp/llm-in-containers.git
   cd llm-in-containers/rag-retrievers
   ```

2. Install dependencies in your local environment:

    ```shell
    pip install -r requirements.txt
    ```

3. Replace with your documents:
    Add your markdown format file under `/rag-retrievers/data`.
    Replace all occurrences of `/RAG-Zelda-Tears-of-the-Kingdom(Fan-made).md` with the new filename throughout in project.

4. Create a .env file in the rag-retrievers directory:

   ```shell
   echo "data_path=../data\nOPENAI_API_KEY=<YOUR-OPENAI-API-KEY>\nTOKENIZERS_PARALLELISM=False\nNEBULA_USER=root\nNEBULA_PASSWORD=nebula\nNEBULA_ADDRESS=<YOUR-IP-ADDRESS:9669>" > .env
   ```

   Replace `<YOUR-OPENAI-API-KEY>` with your own API key in the `.env` file under the `/rag-retrievers` directory.

5. Generate preprocessing `db_stores` required for Textual Features and Query Intent engines:

    Execute the code blocks in Jupyter Notebooks `exp_table.ipynb` and `exp_recursive.ipynb` under `/rag-retrievers/notebooks`, making sure to modify the system_prompt to match your file content beforehand, for regenerating parsed contents under `db_stores` and testing.

6. Generate preprocessing `db_stores` required for Graph Rag (KGI-Based) engine:

   - Install NebulaGraph locally. Refer to the installation instructions for Docker Desktop here. Once installed, click Studio in Browser to use NebulaGraph. Replace <YOUR-IP-ADDRESS:9669> with your own IP address in the `.env` file under the `/rag-retrievers` directory.
   - Execute the code blocks in Jupyter Notebook `exp_kg.ipynb` under `/rag-retrievers/notebooks`, and conduct testing with appropriate questions.

7. Fill in your own `<YOUR-OPENAI-API-KEY>` in the `.env` file under the `/src/streamlit-web` directory.

8. Launch the demo:

   ```shell
   cd src/streamlit-web
   streamlit run demo.py
   ```

    Visit the UI at http://{IP of Host instance}:8501. On the UI, you can choose any of the three query engines - "Table+Text", "Document Agent", or "Graph Rag (KGI-Based)" to explore the actual query results for your own material.
