#######################################Import Modules#########################################
import warnings
warnings.filterwarnings('ignore')
import streamlit as st

import os
#st.write(os.getcwd())

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append("..")

#from src.local_models.llm import MyLLM, LlamaCPPLLM
from llama_index.llms.openai import OpenAI
from local_models.embeddings import get_embed_model

from data_loader.splitting import split_by_md_headers
from data_loader.parsing import get_html, extract_md_tables

from llama_index.core import Document
from data_loader.chunking import chunk_docs_standalone
from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate

from dotenv import load_dotenv
import os

from data_loader.load_from_dir import rebuild_index
from utils import load_prompt
from llama_index.core import PromptTemplate


from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent

import logging
###############################################################################################
load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)


@st.cache_resource
def build_table_n_text_engine():
    logger.info('loading llm and embed_model...')
    #set up llm and embed_model
    embed_model = get_embed_model(model_name=os.environ['embed_path'],  model_kwargs={'device': 'cpu'}, encode_kwargs = {'normalize_embeddings': True})
    #llm = MyLLM(pretrained_model_name_or_path=os.environ['llm_path'], device_map="mps", context_window=4096, num_output=512, model_name='chatglm3-6b')
    llm = OpenAI(temperature=0)
    #service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)






    logger.info('rebuilding storage context from disk...')
    #rebuild storage context from disk
    table_index = rebuild_index("../../db_stores/table_index")
    text_index = rebuild_index("../../db_stores/text_index")


    logger.info('building query engines...')
    #build query engines
    table_engine = table_index.as_query_engine()
 
    text_engine = text_index.as_query_engine()
   


    logger.info('building agents...')
    #define tools
    query_engine_tools = [
        QueryEngineTool(
            query_engine=table_engine,
            metadata=ToolMetadata(
                name="table_tool",
                description=(
                    "Useful for retriving specific context from tables"
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=text_engine,
            metadata=ToolMetadata(
                name="text_tool",
                description=(
                    "Useful for retriving specific context from plain text"
                ),
            ),
        ),

    ]

    # build agent
    agent = OpenAIAgent.from_tools(
        query_engine_tools,
        max_function_calls=3,
        verbose=True,
        system_prompt=f"""\
            Respond in Chinese.
            
            If you inquire general-purpose questions, refer to the text_tool as a priority.
            For questions involving numbers and figures, refer to the table_tool first.
            If you need to analyze problems demanding a higher degree of rigorous reasoning, such as step-by-step instructions, 
            please utilize both the text_tool and table_tool to synthesize your answer.
            
            You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
            """,
    )

    logger.info('Done...')
    #if "chat_engine" in st.session_state.keys():
        #st.session_state.clear()
        ##st.session_state.pop("chat_engine")
    #st.session_state.chat_engine = agent
    return agent








