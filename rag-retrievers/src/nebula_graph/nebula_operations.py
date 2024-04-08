from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
from nebula3.data.ResultSet import ResultSet
from typing import Dict

import pandas as pd

import os

# define a config
config = Config()
config.max_connection_pool_size = 10
# init connection pool
connection_pool = ConnectionPool()
# if the given servers are ok, return true, else return false
ok = connection_pool.init([('127.0.0.1', 9669)], config)


from dotenv import load_dotenv
load_dotenv()

username, pwd = os.environ['NEBULA_USER'], os.environ['NEBULA_PASSWORD']





def result_to_df(result: ResultSet) -> pd.DataFrame:
    """
    build list for each column, and transform to dataframe
    """
    assert result.is_succeeded()
    columns = result.keys()
    d: Dict[str, list] = {}
    for col_num in range(result.col_size()):
        col_name = columns[col_num]
        col_list = result.column_values(col_name)
        d[col_name] = [x.cast() for x in col_list]
    return pd.DataFrame.from_dict(d, orient='columns')





def show_hosts():
    command = 'SHOW HOSTS'
    with connection_pool.session_context(username, pwd) as session:
        rsltset = session.execute(command)
            
    hosts_df = result_to_df(rsltset)
    
    return hosts_df






def add_hosts_if_not_available():
    #check if hosts exist and has an 'ONLINE' status
    hosts_df = show_hosts()
    if hosts_df.empty:
        with connection_pool.session_context(username, pwd) as session:
            session.execute('ADD HOSTS "storaged0":9779, "storaged1":9779, "storaged2":9779')
    else:
        for idx, row in hosts_df.iterrows():
            if row['Status'] != 'ONLINE':
                HOST = row['Host']
                with connection_pool.session_context(username, pwd) as session:
                    session.execute(f"DROP HOSTS {HOST}:9779")
                    session.exucute(f"ADD HOSTS {HOST}:9779")






def show_spaces():
    command = 'SHOW SPACES'
    with connection_pool.session_context(username, pwd) as session:
        rsltset = session.execute(command)  
        
    spaces_df = result_to_df(rsltset)
    
    return spaces_df






def drop_space_if_exists(space_name):
    command = f'DROP SPACE IF EXISTS {space_name}'
    with connection_pool.session_context(username, pwd) as session:
        rsltset = session.execute(command)  






def init_nebula_cluster(space_name):
    #drop space if it exists
    drop_space_if_exists(space_name)
    #create space
    cmd_init = f'CREATE SPACE {space_name}(vid_type=FIXED_STRING(256), partition_num=10, replica_factor=1)'
    #add schema
    
    cmd_schema = f"""
        CREATE TAG entity(name string);
        CREATE EDGE relationship(relationship string);
        CREATE TAG INDEX entity_index ON entity(name(256));
        """


    with connection_pool.session_context(username, pwd) as session:
        session.execute(cmd_init)
        session.execute(f'USE {space_name};')  
        session.execute(cmd_schema)


