
"""
    Title: init.py
    Author: Akash D.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Starting file   ## 
         ###############################################################
 """

import requests
import json
import pathlib
import datetime
import click
from ci_commands import encrypt
from buildpan import setting, yaml_reader, create_file
from buildpan.installer import installer
from pyfiglet import Figlet


info = setting.info

# getting env variable
init_log = info["INSERT_INIT_LOG_URL"]
fetch_details = info["FETCH_DETAILS_URL"]
        
@click.command()
def init():
    '''
    For initiating the webhook operation 

    Please store config.yaml in the directory 
    Please create the clone of the repository  
    \f
    
   
    '''
    path=pathlib.Path().resolve()
    print("Your current directory  is : ", path)
    try:

        yaml_reader.yaml_reader(path)
        
        pipeline_id = yaml_reader.yaml_reader.pipeline_id
        print(1, pipeline_id)
        response = requests.get(fetch_details + "?" + 'pipeline_id=' + pipeline_id)
        data = response.text
        print(2, data)
        data = json.loads(data)

        enc_key = b'CgOc_6PmZq8fYXriMbXF0Yk27VT2RVyeiiobUd3DzR4='
            
        # Serializing json 
        json_object = json.dumps(data, indent = 5)
    
        # Writing to sample.json
        with open(pipeline_id+'.json',"w") as outfile:
            outfile.write(json_object)
        
        #Reading from json file
        with open(pipeline_id+'.json') as file:
            info = json.load(file)
            branchName = info["branchName"]
            token = info["githubtoken"]
            repo_name = info["name"]
            project_id = info["projectId"]
            provider = info["provider"]
        
        # encrypting a json file
        enc = encrypt.Encryptor()
        enc.encrypt_file(enc_key, pipeline_id+'.json')
        print(3)
        requests.post(init_log + "?" +'pipeline_id='+pipeline_id+'&msg=init operation Success!')
        print(4)
        installer(pipeline_id)
        print(5)
        # create file
        create_file.create_file(project_id, repo_name, path, pipeline_id, branchName)
        print(6)
        print("\n Init operation done.")
        
    except Exception as e:
        print("config file not found or not in proper format.")
        print("Message : " + str(e))
        print("Initialization failed")
        try:
            pass
            requests.post(init_log + "?" +'pipeline_id='+pipeline_id+'&msg=init operation Failed!')
        except:
            pass


init() 