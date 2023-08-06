"""
    Title: repo_pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description:
        ###############################################################
        ## Perform a pull operation on a repository   ## 
         ###############################################################
 """

import datetime
import requests
from buildpan import setting
import subprocess


info = setting.info


insert_log = info["INSERT_PULL_LOG_URL"]


def repo_pull(path, branch_name, build_id, commit_id):

    try:

        subprocess.call(["git", "pull", "origin", branch_name, commit_id], cwd=path)

        requests.post(insert_log + "?" +'build_id='+build_id+'&msg=pull operation success!')

    except Exception as e:         
        requests.post(insert_log + "?" +'build_id='+build_id+'&msg=pull operation Failed!')
