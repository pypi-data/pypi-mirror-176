"""
    Title: workflow
    Author: Abizer
    Modified By: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description:
        ###############################################################
        ##      Calls deployer for workflow process                  ## 
        ###############################################################
 """

from buildpan import yaml_reader, deployer
from buildpan import setting
import datetime, requests

info = setting.info


insert_log = info["INSERT_PULL_LOG_URL"]

def workflows(path, build_id):
    
    try:
        yaml_reader.yaml_reader(path)
        workflow = yaml_reader.yaml_reader.workflow
        jobs = yaml_reader.yaml_reader.jobs

        success = False
        
        for job in workflow:
            if job == "scripts":
                success = deployer.script_runer(jobs[job], path)
            
            elif job == "deploy":
                if jobs[job]['appName'].lower() == 'Meanstack'.lower():
                    success = deployer.mean_stack(path, build_id)
                else:
                    success = False
                    print(f"{jobs[job]['appName']} is not Supported")
                    break
            else:
                success = False
        return success
    
    except Exception as e:
        requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment failed!')
