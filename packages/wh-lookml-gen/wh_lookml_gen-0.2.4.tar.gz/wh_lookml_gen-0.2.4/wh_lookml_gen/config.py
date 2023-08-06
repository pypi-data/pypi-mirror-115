from google.oauth2 import service_account
import os
import yaml

## source vars

path = os.path.expanduser('~')

profile_pass = os.path.join(path,".lookml_gen/profile.yaml")

with open(profile_pass) as f:
    lookml_config = yaml.load(f, Loader=yaml.FullLoader)

## global vars

warehouse_name =  lookml_config['warehouse']['warehouse_name']
project_name =  lookml_config['warehouse']['project_name']

## big_query vars

service_account_path = lookml_config['warehouse']['key_file']

service_account = service_account.Credentials.from_service_account_file(
    service_account_path,
)

## red_shift vars

red_shift_project =  lookml_config['warehouse']['project_name']
red_shift_host =  lookml_config['warehouse']['host']
red_shift_port =  lookml_config['warehouse']['port']
red_shift_user =  lookml_config['warehouse']['user']
red_shift_password =  lookml_config['warehouse']['password']