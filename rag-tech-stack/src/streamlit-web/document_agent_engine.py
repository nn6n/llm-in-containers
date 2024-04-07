import warnings
warnings.filterwarnings('ignore')
import streamlit as st

import os
#st.write(os.getcwd())

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append("..")

#from local_models.llm import MyLLM, LlamaCPPLLM
from llama_index.llms.openai import OpenAI
from local_models.embeddings import get_embed_model
from llama_index.core import ServiceContext

from data_loader.parsing import MDDF
from data_loader.splitting import split_by_md_headers, text_2_Document
from data_loader.chunking import chunk_docs_standalone
from data_loader.load_from_dir import rebuild_index


#from llama_index.core import Document
import os, re
import pandas as pd

from typing import Dict, List
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, SummaryIndex
from llama_index.core import PromptTemplate
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.schema import IndexNode

from llama_index.agent.openai import OpenAIAgent
#from llama_index.core.agent import ReActAgent

from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine

from utils import load_prompt
import logging

load_dotenv(override=True)
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)




#format md as DF
df = split_by_md_headers('../../data/RAG-塞尔达王国之泪材料.md')
#construct node mappings
key_words, docs = MDDF(df, [1]).construct_node_mappings(show_progress=False)#remove useless contents

@st.cache_resource
def build_doc_agent_engine(similarity_top_k=2): #key_words, docs=None, 
    logger.info('loading llm and embed_model...')
    embed_model = get_embed_model(model_name=os.environ['embed_path'],  model_kwargs={'device': 'cpu'}, encode_kwargs = {'normalize_embeddings': True})

    llm = OpenAI(temperature=0)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)





    logger.info('building doc agent for each doc')
    ##Build Document Agent for each Document
    
    #build agents dict
    agents = {}
    nodes = []
    for i, kw in enumerate(key_words):

        #build vector index--first time
        #vector_index = VectorStoreIndex(docs[kw], embed_model=embed_model)
        #vector_index.storage_context.persist(persist_dir="db_stores/doc_agent_vector_index")

        #load from disk
        vector_index = rebuild_index(persist_dir=f'../../db_stores/doc_agent_vector_index/idx_{i}', service_context=service_context)


        #build keyword indexfirst time
        #kw_index = KeywordTableIndex.from_docunments(docs[kw])
        #summary_index = SummaryIndex(docs[kw], embed_model=embed_model)
        #summary_index.storage_context.persist(persist_dir="db_stores/doc_agent_summary_index")

        #load from disk
        summary_index = rebuild_index(persist_dir=f'../../db_stores/doc_agent_summary_index/idx_{i}', service_context=service_context)



        #define query engines
        vector_query_engine = vector_index.as_query_engine(llm=llm)

        
        #kw_query_engine = kw_index.as_query_engine()
        list_query_engine = summary_index.as_query_engine(llm=llm)


        #define tools
        query_engine_tools = [
            QueryEngineTool(
                query_engine=vector_query_engine,
                metadata=ToolMetadata(
                    name="vector_tool",
                    description=(
                        f"Useful for retrieving specific context from {kw}"
                    )
                )
            ),
            QueryEngineTool(
                #query_engine=kw_query_engine,
                query_engine=list_query_engine,
                metadata=ToolMetadata(
                    name="summary_tool",
                    description=(
                        f"Useful for summarization-wise questions related to {kw}"
                    )
                )
            )
        ]
        

        #build agents
        agent = OpenAIAgent.from_tools(
            query_engine_tools,
            llm=llm,
            embed_model=embed_model,
            verbose=True,
            #output_parser=output_parser, 
            
            system_prompt=f"""\
                Make sure to respond in Chinese.

                You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.
                Please refer to the summary_tool first if you inquire summarization-wise questions about {kw}
                If you need to fetch details about {kw}, please refer to the vector_tool first.
                """,
        )#ReActAgent
        agents[kw] = agent
    
    
        ##Build Composable Retriever over the agents
        #define top-level nodes
        instru =(
            "This content contains some introduction to The Legend of Zelda: Tears of the Kingdom"
             "on the following aspect {kw}, "
            f"Use this index if you need to look up specific facts about {kw}, "
            f"Do not use this index if you want to analyze aspects beyond {kw} "
        )

        node = IndexNode(
            text=instru, index_id=kw, obj= agent
            )
        nodes.append(node)
    
    #define top-level retriever
    top_vector_index = VectorStoreIndex(objects=nodes, embed_model=embed_model)
    query_engine = top_vector_index.as_query_engine(similarity_top_k=similarity_top_k, verbose=True)

    logger.info('Done...')
    return query_engine