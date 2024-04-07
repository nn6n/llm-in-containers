from langchain.embeddings.huggingface import HuggingFaceEmbeddings




def get_embed_model(model_name, model_kwargs = {'device': 'cpu'}, encode_kwargs = {'normalize_embeddings': False}):

    embed_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embed_model

#embed_model = get_embed_model()