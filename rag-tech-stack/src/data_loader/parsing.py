import markdown2
#import markdown
from markdownify import markdownify
import re
import pandas as pd
import numpy as np
from typing import List


from data_loader.splitting import text_2_Document
from data_loader.chunking import chunk_docs_standalone






def get_html(x):
  pos = x.find('|') #to make sure tables can be correctly tagged as <table> rather than part of <p>
  text_str = x[:pos]+'\n'+x[pos:]
  html_str = markdown2.markdown(text_str, extras=['tables'])
  #html_str = markdown.markdown(text_str, extension=['extra']) #'tables' and 'fenced_code' are included
  return html_str



def html_2_md(x):
    return markdownify(x, heading_style='ATX')


def extract_md_tables(df):
    dfc = df.copy(deep=True)
    #flag chunks containing tables; split into table + non-table parts respectively.
    dfc['is_table'] = np.where(dfc['text_html'].str.contains('<table>'), 1, 0)
    #get html 
    dfc.loc[dfc['is_table']==1, 'table_html'] = dfc.loc[dfc['is_table']==1]['text_html'].apply(lambda x: x[x.index('<table>'):x.index('</table>')+len('</table>')])
    dfc.loc[dfc['is_table']==1, 'remarks_html'] = dfc.loc[dfc['is_table']==1]['text_html'].apply(lambda x: x.split('<table>')[0]+x.split('</table>')[-1])
    dfc.loc[dfc['table_html'].notna(), 'text_html'] = dfc.loc[dfc['table_html'].notna(), 'remarks_html']
    
    
    #convert html to md
    dfc['text'] = dfc['text_html'].fillna('').apply(lambda x: html_2_md(x))
    dfc['table'] = dfc['table_html'].fillna('').apply(lambda x: html_2_md(x))
    dfc.drop(['remarks_html', 'table_html', 'text_html'], axis=1, inplace=True)

    dfc = dfc[dfc['text']!='']
    dfc.reset_index(drop=True, inplace=True)

    return dfc


class MDDF:
    def __init__(self, df: pd.DataFrame, remove_rows: List=None):
        self.df = df.fillna('')
        if remove_rows:
            self.df.drop(remove_rows, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
        #self.key_words, self.docs = self.construct_node_mappings()
        


    @staticmethod
    def remove_section_number(text):
        pattern = r'^\d+(\.\d+)*\s+'  # Matches section number followed by whitespace
        return re.sub(pattern, '', text)
    @property
    def get_shape(self):
        return self.df.shape
    
    
    def construct_node_mappings(self, chunk_size=1024, chunk_overlap=20, show_progress=True):
        ncol = self.get_shape[1]
        self.df[self.df.columns[:ncol-1]] = self.df[self.df.columns[:ncol-1]].map(MDDF.remove_section_number)
        

        self.df['key_words'] = self.df.iloc[:, :ncol-1].apply(
            lambda row: '文档标题、创建时间、标签和类别' if row.isna().all() or all(val == '' for val in row) else ', '.join(filter(bool, row.dropna())).strip(),
            axis=1
        )
        
        docs = {}
        key_words = []
        
        for idx, row in self.df.iterrows():
            kw = row['key_words']
            key_words.append(kw)
            docs[kw] = chunk_docs_standalone(
                documents=text_2_Document(strr=row['content'], meta={}),
                chunk_size=chunk_size, chunk_overlap=chunk_overlap, show_progress=show_progress)
        
        return key_words, docs

    
    
    @property
    def show_df(self):
        return self.df
    @property
    def show_mappings(self):
        return self.docs

