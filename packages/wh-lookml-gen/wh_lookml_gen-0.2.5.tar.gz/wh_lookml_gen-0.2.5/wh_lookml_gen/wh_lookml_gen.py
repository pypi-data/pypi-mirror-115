import lkml as looker
from pprint import pprint
from google.oauth2 import service_account
import pandas_gbq
from contextlib import redirect_stdout
import pandas as pd
import pandas
import os
import json
import sys
import yaml

from wh_lookml_gen import warehouse_target
from wh_lookml_gen import config


import git

pd.options.mode.chained_assignment = None

credentials = config.service_account

warehouse_name = config.warehouse_name
lookml_project = config.project_name

sql = warehouse_target.warehouse_schema

if warehouse_name == 'big_query':

    # Run a Standard SQL query with the project set explicitly
    project_id = lookml_project
    df = pandas.read_gbq(sql, dialect='standard', project_id=lookml_project, credentials=credentials)


    df1 = df[['table_name','column_name','data_type']]

    df1['data_type'] = df1['data_type'].str.replace('TIMESTAMP','timestamp')
    df1['data_type'] = df1['data_type'].str.replace('DATE','date')
    df1['data_type'] = df1['data_type'].str.replace('INT64','number')
    df1['data_type'] = df1['data_type'].str.replace('FLOAT64','number')
    df1['data_type'] = df1['data_type'].str.replace('NUMERIC','number')
    df1['data_type'] = df1['data_type'].str.replace('STRING','string')
    df1['data_type'] = df1['data_type'].str.replace('BOOL','yesno')

def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:,1:]) for k,g in grouped}
    return d


d1 = (recur_dictify(df1))
    
def get_all_values(nested_dictionary):

    
    for key,value in nested_dictionary.items():

        explore = {


            "explore": key,
                
            "{ hidden": "yes }"
                
            }
            
        
        yield(looker.dump(explore))
        
    for key,value in nested_dictionary.items():

        view = {


            "view": key+" {",
                    
            "sql_table_name": key
                                
            }

        yield(looker.dump(view))
        

        for key, value in value.items():
            
            if "pk" not in key and "fk" not in key and "date" not in value and "timestamp" not in value:

                if type(value) is dict:
                    get_all_values(value)
                else:

                    dimension = {
                        
                        "dimension": {
                            "type": value,
                            "sql": "${TABLE}."+key,
                            "name": key
                        }
                    }

                    yield(looker.dump(dimension))

            elif "pk" in key:

                if type(value) is dict:
                    get_all_values(value)
                else:

                    dimension = {
                        
                        "dimension": {
                            "primary_key": "yes",
                            "hidden": "yes",
                            "type": value,
                            "sql": "${TABLE}."+key,
                            "name": key
                        }
                    }

                    yield(looker.dump(dimension))

            elif "date" in value:

                if type(value) is dict:
                    get_all_values(value)
                else:

                    dimension = {
                        
                        "dimension_group": {

                                "timeframes": "[raw,date,week,month,quarter,year]",

                            "type": "time",
                            "datatype": value,
                            "sql": "${TABLE}."+key,
                            "name": key
                        }
                    }

                    yield(looker.dump(dimension))

            elif "timestamp" in value:

                if type(value) is dict:
                    get_all_values(value)
                else:

                    dimension = {
                        
                        "dimension_group": {

                                "timeframes": "[time,raw,date,week,month,quarter,year]",

                            "type": "time",
                            "datatype": value,
                            "sql": "${TABLE}."+key,
                            "name": key
                        }
                    }


                    yield(looker.dump(dimension))

            else:

                if type(value) is dict:
                    get_all_values(value)
                else:

                    dimension = {
                        
                        "dimension": {
                            "hidden": "yes ",
                            "type": value,
                            "sql": "${TABLE}."+key,
                            "name": key
                        }
                    }

                    yield(looker.dump(dimension))
                
                
        for key,value in nested_dictionary.items():

            syntax = "}"


        yield(syntax)
                

nested_dictionary = d1

get_all_values(nested_dictionary)

def get_git_root(path):

        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        return (git_root)

git_def_path = get_git_root(os.getcwd())

def output():
    
    git_path = git_def_path

    rel_path = "base"

    path = os.path.join(git_path, rel_path)

    if not os.path.exists(path):
        os.makedirs(path)
        
    filename = '_basic.layer.lkml'

    with open(os.path.join(path, filename), 'w') as file:

        with redirect_stdout(file):

            for value in get_all_values(nested_dictionary):

                print(value)

output()
    