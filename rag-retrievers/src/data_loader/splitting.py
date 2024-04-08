from langchain.text_splitter import MarkdownHeaderTextSplitter
from llama_index.core import Document
import pandas as pd
import re
from typing import Dict





headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5")
]


def split_by_md_headers(path2md:str)-> pd.DataFrame:
    f = open(path2md, "r").read()
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(f)
    #format as DF
    rows = []
    def remove_html_tags(strr:str)-> str:
        return re.compile(r'<[^>]+>').sub('', strr).strip()
    for i in range(len(md_header_splits)):
        #remove html tags and format headers
        row = {'metadata': md_header_splits[i].metadata, 'content': remove_html_tags(md_header_splits[i].page_content)}
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df = pd.concat([df.drop('metadata', axis=1), df['metadata'].apply(pd.Series)], axis=1)
    

    #reorder columns
    column_to_move = df.pop("content")
    df.insert(df.shape[1], "content", column_to_move)
    df = df[df['content']!='']
    df.reset_index(drop=True, inplace=True)

    return df



def text_2_Document(strr:str, meta:Dict={})-> Document:
    return Document(text=strr, metadata=meta)






