import os
import yaml
from contextlib import redirect_stdout
import sys
import ruamel.yaml

dict_file = {'warehouse': {'warehouse_name': None, 'project_name': None, 'schema_name': None, 'host': None, 'port': None, 'user': None, 'password': None, 'key_file': None}}

def wh_init():

    path = os.path.expanduser('~')

    profile_path = os.path.join(path,".lookml_gen_test")

    if not os.path.exists(profile_path):
       os.makedirs(profile_path)

    file_name = "profile.yaml"

    with open (os.path.join(profile_path,file_name), 'x') as file:

        with redirect_stdout(file):
            
            yaml = ruamel.yaml.YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)            
            yaml.dump(dict_file,file)

wh_init()