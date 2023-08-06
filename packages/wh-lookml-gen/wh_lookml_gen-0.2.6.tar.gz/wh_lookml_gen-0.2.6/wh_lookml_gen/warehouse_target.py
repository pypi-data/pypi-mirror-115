import os
import yaml


path = os.path.expanduser('~')

profile_pass = os.path.join(path,".lookml_gen/profile.yaml")

with open(profile_pass) as f:
    lookml_config = yaml.load(f, Loader=yaml.FullLoader)

##global vars

project_name =  lookml_config['warehouse']['project_name']
schema_name =  lookml_config['warehouse']['schema_name']

test_schemas = lookml_config['warehouse']['test_schemas']

## warehouse schema

warehouse_schema =   """

with source as (

    select * from `{0}.{1}.INFORMATION_SCHEMA.COLUMNS`

    )

    select * from source

""".format(project_name,schema_name)

## warehouse test schemas

test_warehouse_schema =   """

        with source_1 as (

            select * from `{0}.{1}.INFORMATION_SCHEMA.COLUMNS`

            ),

        source_2 as (

        select * from `{0}.{2}.INFORMATION_SCHEMA.COLUMNS`
        
        ),
        
        source_3 as (

        select * from `{0}.{3}.INFORMATION_SCHEMA.COLUMNS`
        
        ),
        
        unioned as (

        select * from source_1
        
        union all
        
        select * from source_2
        
        union all
        
        select * from source_3
        
        )

        select * from unioned

""".format(project_name,test_schemas[0],test_schemas[1],test_schemas[2])
