from llama_index.core import SimpleDirectoryReader

def load_data(path_2_dir=None, input_files=None):
    if path_2_dir is None and input_files is None:
        raise ValueError("Exactly one of 'path_2_dir' and 'input_files' can be specified.")
    if path_2_dir is not None and input_files is not None:
        raise ValueError("Only one of 'path_2_dir' and 'input_files' can be specified.")
    reader = SimpleDirectoryReader(input_dir=path_2_dir, input_files=input_files)
    docs = reader.load_data()

    return docs