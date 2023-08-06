"""
    Title: stop
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 22-09-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Remove a particular repo details from centralized file    ## 
        ###############################################################
"""

import click
from click.decorators import command
import os, pathlib
from buildpan import yaml_reader, find_path

@click.command()
def stop():
    '''
    For deleting a particular repository information
    \f
    
   
    '''
    try:
        path=pathlib.Path().resolve()
        
        yaml_reader.yaml_reader(path)    
        pipeline_id = yaml_reader.yaml_reader.pipeline_id


        find_path.find_path()
        file_path = find_path.find_path.file_path
    

        with open(file_path + "/info.txt", "r") as input:
            with open(file_path + "/sample.txt", "w") as output:
                for line in input:
                    data = eval(line)

                    # if substring contain in a line then don't write it
                    if pipeline_id not in data["pipeline_id"]:
                        output.write(str(data) + "\n")

        #replace file with original name
        os.replace(file_path +'/sample.txt', file_path +'/info.txt')
        print("Repository Deleted!")
    except:
        print("This repository is not configured.")