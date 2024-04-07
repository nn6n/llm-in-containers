from llama_index.core import StorageContext, load_index_from_storage, load_indices_from_storage
from typing import List



def rebuild_index(persist_dir, service_context=None):
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    # load index
    index = load_index_from_storage(storage_context=storage_context, service_context=service_context)

    return index

def rebuild_indices(persist_dir, service_context=None) -> List:
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    # load indices
    indices = load_indices_from_storage(storage_context=storage_context, service_context=service_context)

    return indices
