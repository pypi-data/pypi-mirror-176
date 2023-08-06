"""
    Title: previous_commit
    Author: Kushagra A.
    Language: Python
    Date Created: 14-09-2021
    Date Modified: 14-09-2021
    Description:
        ###############################################################
        ## Get previous commit of a repository   ## 
         ###############################################################
 """

import subprocess
from buildpan import setting
import requests

info = setting.info

# getting env variable
insert_log = info["INSERT_PULL_LOG_URL"]


def prev_commit(path, build_id):
    try:

        # restoring to previous commit
        result = subprocess.run(["git", "rev-parse", "@~"], cwd=path, shell=True,stdout=subprocess.PIPE)
        val = str(result.stdout).index("'")
        index1=str(result.stdout).index("'",val+1)
        hash = str(result.stdout)[val+1:index1-2]
        result1 = subprocess.run(["git", "checkout", hash], stdout= subprocess.PIPE, stderr = subprocess.STDOUT, cwd=path)

        requests.post(insert_log + "?" +'build_id='+build_id+'&msg=previous commit operation success!')     
    except Exception as e:
        requests.post(insert_log + "?" +'build_id='+build_id+'&msg=previous commit operation Failed!') 
