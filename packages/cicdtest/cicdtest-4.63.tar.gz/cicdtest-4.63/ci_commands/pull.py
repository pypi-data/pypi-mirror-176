"""
    Title: pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description:
        ###############################################################
        ## Check for pull operation on a repository   ## 
         ###############################################################
 """

import json
from buildpan.previous_commit import prev_commit
import requests
from buildpan import setting, workflow, repo_pull, find_path
import click


info = setting.info


# getting env variable
push_commit = info["PUSH_COMMIT_URL"]
update_status = info["UPDATE_STATUS_URL"]

@click.command()
def pull():
    '''
    For initiating the pull operation

    \f
    '''

    try:
        find_path.find_path()
        file_path = find_path.find_path.file_path

        #reading data from centralized file
        with open(file_path + "/info.txt") as file:
            info = file.readlines()
            for data in info:
                d = eval(data)
                pipeline_id = d["pipeline_id"]
                pipeline_id = "pipeline_id="+pipeline_id
                
                # using pooling for pull operation
                response = requests.get(push_commit, pipeline_id)
                
                data=response.text
                data = json.loads(data)

                path = d["path"]
                project_id = d["project_id"]
                repo_name = d["repo_name"]
                branch_name = d["branch_name"]
                build_id = data["buildId"]
                commit_id = data["hash"]

                # doing pull operation
                repo_pull.repo_pull(path, branch_name, build_id, commit_id)
                        
                # if pull success calling deployment        
                response = workflow.workflows(path, build_id)
                
                # if deployment fails go to previous commit
                if response == False:
                    prev_commit(path, build_id)
                    requests.post(update_status + "?" +'build_id='+build_id + "&status=4")
                else:
                    requests.post(update_status + "?" +'build_id='+build_id + "&status=1")
    
    except Exception as e:
        print("Exception = ", e)



