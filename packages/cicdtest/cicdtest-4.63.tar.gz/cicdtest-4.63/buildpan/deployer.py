"""
    Title: deployer
    Module Name: deployer
    Author: Abizer
    Modified By: Abizer, Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description: Return Type is Bolean Is success then "True" otherwise "False"
        ###############################################################
        ##                 Deployer for all Stack                    ## 
        ###############################################################
 """

import subprocess 
import datetime, requests
import json
import os
from buildpan import setting

info = setting.info


insert_log = info["INSERT_PULL_LOG_URL"]

def mean_stack(cwd, build_id):
    '''
    Deploy MeanStack project
    '''
    try:

        success = False
        curtime = datetime.datetime.now()
        message = ""
        
        # Reding entrypoint 
        file_path = os.path.join(cwd,"package.json")
        package_file = open(file_path)
        project_detail = json.loads(package_file.read())
        package_file.close()

        # installing all the dependency if packge.json found otherwise genrate error
        result_install = subprocess.run(['npm', 'install'] , stdout= subprocess.PIPE, stderr = subprocess.STDOUT, cwd=cwd)
        if result_install.returncode:
            requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment failed!')
            return success 
        else:
            # if pm2 is not installed installing otherwise update 
            result_install_pm2 = subprocess.run(['npm','install', 'pm2', '-g'], stdout= subprocess.PIPE, stderr = subprocess.PIPE)
            if result_install_pm2.returncode:
                requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment failed!')
                return success
            else:
                try:
                    app_name = project_detail["main"]
                except Exception as e:
                    popen_arg = ["ls", "app.js"]
                    file_found = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,cwd=cwd)
                    if file_found.returncode:
                        popen_arg = ["ls", "index.js"]    
                        file_found = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,cwd=cwd)
                        if file_found.returncode:
                            requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment failed!')
                            return success
                        else:
                            app_name = "index.js"
                    else:
                        app_name = "app.js"


                # check service status if off start that otherwise reload it 
                service_status = subprocess.run(['pm2', 'status'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                if service_status.stdout.decode().find("online") == -1:
                    popen_arg = ['pm2', 'start', project_detail["main"]]
                    result_start = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = cwd)
                    process_fails = result_start.returncode
                    message = result_start.stdout.decode()
                else:
                    popen_arg = ['pm2', 'reload', project_detail["main"]]
                    result_relod = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = cwd)
                    process_fails = result_relod.returncode
                    message = result_relod.stdout.decode()

            if process_fails:
                requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment failed!')
                return success
            else: 
                success = True
                requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment success!')
                return success
    except Exception as e:
        requests.post(insert_log + "?" +'build_id='+build_id+'&msg=deployment failed!')
        return False

def script_runer(scripts, path):
    '''
    Script runner is called when Script under jobs is called in workflow and have some script 
    that to be executed 
    
    '''
    
    success = False
    for script in scripts:
        script_list = list(script.split(" "))
        result = subprocess.run(script_list,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd = path)
        print(result.stdout.decode())
        if result.returncode:
            return success
        
    success = True
    return success
    
            



