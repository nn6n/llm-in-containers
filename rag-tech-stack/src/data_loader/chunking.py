from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


#standalone usage
def chunk_docs_standalone(documents: Document, chunk_size=1024, chunk_overlap=20, show_progress=True):

    node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    nodes = node_parser.get_nodes_from_documents(
        [documents], show_progress=show_progress
    )

    return nodes


#To-do: index usage
#Up to index type




