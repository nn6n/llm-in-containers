import warnings
warnings.filterwarnings('ignore')
import streamlit as st

import os
#st.write(os.getcwd())

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append("..")

from llama_index.llms.openai import OpenAI
from local_models.embeddings import get_embed_model


from llama_index.core.retrievers import VectorIndexRetriever, KGTableRetriever
from retrievers.retrieval import CustomRetriever
from data_loader.load_from_dir import rebuild_index

#from nebula_graph.nebula_operations import show_hosts, add_hosts_if_not_available, show_spaces, init_nebula_cluster
from nebula_graph.text_2_graph import df_to_fig, extract_triplets, get_response_n_kg_rel_query

#from llama_index.core import Document
import os, re, ast
import pandas as pd

from typing import Dict, List
from dotenv import load_dotenv



from llama_index.graph_stores.nebula import NebulaGraphStore
from llama_index.core import KnowledgeGraphIndex, VectorStoreIndex, SimpleDirectoryReader

from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import PromptTemplate
import logging

load_dotenv(override=True)
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)


@st.cache_resource
def build_graph_rag_engine():

    #first-time build
    #add_hosts_if_not_available()
    #space_name = "kdp_whitepaper"
    #init_nebula_cluster(space_name)
    #edge_types, rel_prop_names = ["relationship"], ["relationship"] # default, could be omit if create from an empty kg
    #tags = ["entity"]

    #graph_store = NebulaGraphStore(
        #space_name=space_name,
        #edge_types=edge_types,
        #rel_prop_names=rel_prop_names,
        #tags=tags,
    #)
    #documents = SimpleDirectoryReader('../../data/产品白皮书/').load_data()
    #kg_index = KnowledgeGraphIndex.from_documents(
        #documents,
        #max_triplets_per_chunk=10,
        #space_name=space_name,
        #edge_types=edge_types,
        #rel_prop_names=rel_prop_names,
        #tags=tags,
    #)

    #kg_index.storage_context.persist(persist_dir="db/kg_index")

    logger.info('loading llm and embed_model...')
    embed_model = get_embed_model(model_name=os.environ['embed_path'],  model_kwargs={'device': 'cpu'}, encode_kwargs = {'normalize_embeddings': True})

    llm = OpenAI()


    logger.info('rebuilding storage context from disk...')
    kg_index = rebuild_index('../../db_stores/kg_index')


    logger.info('constructing graph rag engine...')
    kg_rag_query_engine = kg_index.as_query_engine(
        include_text=True,
        retriever_mode="hybrid",
        response_mode="tree_summarize",
        llm=llm,
        embed_model=embed_model,
        
    )

    logger.info('Done...')

    #if "chat_engine" in st.session_state.keys():
        #st.session_state.clear()
        ##st.session_state.pop("chat_engine")
    
    #st.session_state.chat_engine = kg_rag_query_engine
    return kg_rag_query_engine
