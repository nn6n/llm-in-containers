import pandas as pd
import re, ast

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl 
mpl.rcParams['font.sans-serif'] = ['Heiti TC']
mpl.rcParams['axes.unicode_minus']=False





#ToDo: query engines
#
#
#
#
#
#
#
#
#





#get response and kg_rel_texts (for Query Engine only, not for Chat Engine)
def get_response_n_kg_rel_query(resp_obj):
    """:params resp_obj: Response Object"""
    response = resp_obj.response

    meta = resp_obj.metadata
    keys = list(meta.keys())
    try:
        _key = [keys[i] for i in range(len(keys)) if 'kg_rel_texts' in meta [keys[i]].keys()][0]
        kg_rel_texts = meta[_key]['kg_rel_texts']
    except:
        kg_rel_texts = None

    return response, kg_rel_texts

#get response, source_texts and source_kg (for Chat Engine only)
def get_response_n_kg_rel_chat(resp_obj):
    """
    :params resp_obj: Response Object
    :output response: str
    :output sources_text: list (non-empty)
    :output sources_kg: list (can be empty)


    """
    response = resp_obj.response

    sources = resp_obj.source_nodes
    num_s = len(sources)
    

    sources_text = [sources[i].text for i in range(num_s-1)]

    sources_kg_map = sources[-1].metadata['kg_rel_map']
    kw_keys = list(sources_kg_map.keys())
    sources_kg = []
    for i in range(len(kw_keys)):
        sources_kg.extend(sources_kg_map[kw_keys[i]])
    

    


    return response, sources_text, sources_kg











def chat_upon_query(chat_engine, query, llm):
    resp_obj = chat_engine.chat(query)
    response, sources_text, sources_kg =get_response_n_kg_rel_chat(resp_obj)
    print(response)
    print(sources_kg)

    #coerce to simple chat mode for non-
    if not sources_kg:
        response = llm.complete(query).text
        


    return response, sources_kg      


#format ER triplets (unidirectional)
def extract_triplets(data):
    """:params data: List(kg_rel_texts)"""
    triplets = [ast.literal_eval(data[i]) for i in range(len(data))]
    
    #remove duplicates
    unique_triplets = [list(tpl) for tpl in set([tuple(lst) for lst in triplets])]
    #format as DF
    tri_df = pd.DataFrame(unique_triplets).rename(columns={0: 'e1', 1: 'r', 2: 'e2'})

    return tri_df




#format ER triplets (unidirectional)
def extract_triplets_deprecated(data):
    """:params data: List(kg_rel_texts)"""
    """
    triplets = []
    for item in data:
        #pattern = r'([^<>\s]+{[^{}]+})\s*-(\[[^\[\]]+\])->\s*([^<>\s]+(?:\s+[^<>\s]+)*{[^{}]+})'
        matches_fwd = re.findall(r'([^<>\s]+{[^{}]+})\s*-(\[[^\[\]]+\])->\s*([^<>\s]+(?:\s+[^<>\s]+)*{[^{}]+})', item)
        #matches_rev = re.findall(r'([^<>\s]+{[^{}]+})\s*<-(\[[^\[\]]+\])-\s*([^<>\s]+(?:\s+[^<>\s]+)*{[^{}]+})', item)
        matches_rev = re.findall(r'([^<>\s]+(?:\s+[^<>\s]+)*{[^{}]+})\s*<-(\[[^\[\]]+\])-\s*([^<>\s]+{[^{}]+})', item)
       
          
        
        for match in matches_fwd:
            
            try:
                entity1, relationship, entity2 = match
                triplet = [re.findall(r'{([^{}]+)}', elem)[0].split(': ')[-1] for elem in [entity1, relationship, entity2]]
                
                triplets.append(triplet)
                #match = [re.findall(r'{([^{}]+)}', match[i])[0].split(': ')[-1] for i in range(len(match))]
                
                
            except:
                pass
        
        for match in matches_rev:
            
            
            try:
                entity1, relationship, entity2 = match
                triplet = [re.findall(r'{([^{}]+)}', elem)[0].split(': ')[-1] for elem in [entity2, relationship, entity1]]
                
                triplets.append(triplet)
                #match = [re.findall(r'{([^{}]+)}', match[i])[0].split(': ')[-1] for i in range(len(match))]
                
                
                
            except:
                pass
    """

    triplets = [ast.literal_eval(data[i]) for i in range(len(data))]
    
    #remove duplicates
    unique_triplets = [list(tpl) for tpl in set([tuple(lst) for lst in triplets])]
    #format as DF
    tri_df = pd.DataFrame(unique_triplets).rename(columns={0: 'e1', 1: 'r', 2: 'e2'})

    return tri_df
    
    #remove duplicates
    unique_triplets = [list(tpl) for tpl in set([tuple(lst) for lst in triplets])]
    #format as DF
    tri_df = pd.DataFrame(unique_triplets).rename(columns={0: 'e1', 1: 'r', 2: 'e2'})

    return tri_df





def df_to_fig(df, show_fig=False):
    """:params df: DF"""
    cols = list(df.columns)
    # Create a knowledge graph
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row[cols[0]], row[cols[2]], label=row[cols[1]])

    # Visualize the knowledge graph
    pos = nx.spring_layout(G, seed=42, k=0.9)
    labels = nx.get_edge_attributes(G, 'label')
    fig = plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color='lightblue', edge_color='gray', alpha=0.6)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, label_pos=0.3, verticalalignment='baseline')
    #plt.title('Knowledge Graph')
    if show_fig:
        plt.show()
    
    return plt








