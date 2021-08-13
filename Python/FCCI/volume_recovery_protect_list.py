#Storage Volume Recovery and Protection from CSV

from tkinter.constants import TRUE
from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.environment_get_protection_jobs_enum import EnvironmentGetProtectionJobsEnum as envjob
from cohesity_management_sdk.models.environment_list_protection_sources_enum import EnvironmentListProtectionSourcesEnum as envsrc
from cohesity_management_sdk.models.environment_list_application_servers_enum import EnvironmentListApplicationServersEnum as envapp
from cohesity_management_sdk.models.environment_list_protected_objects_enum import EnvironmentListProtectedObjectsEnum as envobj
from cohesity_management_sdk.models.protocol_access_enum import ProtocolAccessEnum
from cohesity_management_sdk.models.recover_task_request import RecoverTaskRequest
from cohesity_management_sdk.models.restore_object_details import RestoreObjectDetails
from cohesity_management_sdk.models.update_view_param import UpdateViewParam
from cohesity_management_sdk.models.protection_job_request_body import ProtectionJobRequestBody
from cohesity_management_sdk.models.environment_enum import EnvironmentEnum as env
from cohesity_management_sdk.models.run_protection_job_param import RunProtectionJobParam
from cohesity_management_sdk.models.access_token_credential import AccessTokenCredential
import datetime
import os
import getpass
import csv
import tkinter as tk
from tkinter import filedialog
import magic
import pandas as pd
import requests
import json

#User Authentication Token/Controller Object
class CohesityUserAuthentication(object):
    #User Authentication Intialization
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_fqdn = getpass._raw_input("Please enter the cluster FQDN or VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ") 
        self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")


    def user_auth(self):
        #Autneticate to the cluster method
        return CohesityClient(self.cluster_fqdn, self.username, self.password, self.domain)
    
    def get_cluster_fqdn(self):
        return self.cluster_fqdn
    
    def get_bearer_token(self, cohesity_cient):
        access_token = cohesity_cient.access_tokens
        body = AccessTokenCredential()
        body.username = self.username
        body.password = self.password
        body.domain = self.domain
        bearer_token = access_token.create_generate_access_token(body)
        return bearer_token

class StorageDomainObject(object):
    def __init__(self):
        self.storage_domain = getpass._raw_input("Please enter the Storage Domain to use:  ")
        
    def get_storage_domain_id(self, cohesity_client):
        view_box =  cohesity_client.view_boxes.get_view_boxes(names=self.storage_domain)
        return view_box[0].id
class PolicyObject(object):
    def __init__(self):
        self.policy_name = getpass._raw_input("Please enter the Protection Policy to use:  ")
        
    def get_policy_id(self, cohesity_client):
        policy =  cohesity_client.protection_policies.get_protection_policies(names=self.policy_name)
        return policy[0].id
    
class ViewObject(object):
    def get_view_id(self, cohesity_client, csv_file):
        view_id = []
        names = []
        self.view_list = []
        self.csv_file = csv_file
        
        
        for i, j in self.csv_file.iterrows():
             names.append(j.Name)
        
             
        self.views = cohesity_client.views
        
        for name in names:
            self.view_list.append(self.views.get_view_by_name(name = name))
        
        for view in self.view_list:
            view_id.append(view.view_id)
        
        self.csv_file["ViewID"] = view_id
        return self.csv_file
class ProtectedObjects(object):       
    def get_protection_jobs(self, cohesity_client, csv_file):
        job_id = []
        names = []
        self.jobs_list = []
        self.csv_file = csv_file
        
        for i, j in self.csv_file.iterrows():
            names.append(j.Name)
        
        self.protection_jobs = cohesity_client.protection_jobs
        
        for name in names:
            verified_job = self.protection_jobs.get_protection_jobs(names = name)
            for item in verified_job:
                if item.is_deleted == False or item.is_deleted == None:
                    self.jobs_list.append(item)
        
        for job in self.jobs_list:
            job_id.append(job.id)
        self.csv_file["JobID"] = job_id
        
        return(self.csv_file)
       
    
    def recover_nas_list(self, cohesity_client, csv_file):
        self.csv_file = csv_file
              
        for i, j in csv_file.iterrows():
            #Create Recovery Task
            body = RecoverTaskRequest()
            body.mtype = 'kMountFileVolume'
            body.view_name = j.Name
            body.objects = []
            body.objects.append(RestoreObjectDetails())
            body.name = "Recover-{name}".format(name = j.Name)
            body.objects[0].job_id = j.JobID
            body.restore_view_parameters = UpdateViewParam()
            body.restore_view_parameters.protocol_access = ProtocolAccessEnum.KSMBONLY
            body.restore_view_parameters.enable_smb_view_discovery = TRUE
            cohesity_client.restore_tasks.create_recover_task(body=body)
            print("The generic nas {Hostname}\\{Name} has been recovered".format(Hostname = j.Hostname, Name = j.Name))
            
    def create_view_protection_job(self, cohesity_url, csv_file, cohesity_client, bearer_token, policy_id, storage_domain_id):
        #Get time
        time = cohesity_client.cluster.get_cluster()
        #Get current cluster time
        epoch = time.current_time_msecs
        #Convert cluster time to 24 hour format
        date = datetime.datetime.fromtimestamp(epoch/10**3)
        #Set the zimezone difference this must be changed prior to running.  Need to create a class and object to handle this.
        new_date = date + datetime.timedelta(hours = -3)
        #get cluster timezone
        timezone = cohesity_client.cluster.get_cluster().timezone
        #REST API Headers and auth
        headers = {"Authorization": "Bearer %s" % bearer_token.access_token}
        #REST API Url
        url = 'https://{cohesity_url}/v2/data-protect/protection-groups'.format(cohesity_url=cohesity_url)
        protect_name = []
        protect_view_id = []
        #Rest API payload thorugh loop
        for i, j in csv_file.iterrows():
            payload = {"name": j.Name,"policyId": policy_id,"priority": "kMedium","storageDomainId": storage_domain_id,"startTime": {"hour": new_date.hour,"minute": new_date.minute,"timeZone": timezone}, "environment": "kView", "viewParams": {"objects": [{"id": j.ViewID, "name": j.Name}],"replicationParams": {"viewNameConfigList": [{"sourceViewId": j.ViewID,"useSameViewName": True}]},"indexingPolicy": {"enableIndexing": True,"includePaths": ["/"]}}}
            
            req = requests.post(url=url, data=json.dumps(payload), headers=headers, verify=False)
            print("The View {name} has been protected".format(name=j.Name))
                           
        
#CSV Import Class
class CsvImport(object):
    #CSV Object
    def __init__(self):
        pass
    
    def open_csv(self):
        #Use Native OS FileExplorer to open csv
        self.root = tk.Tk()
        self.root.withdraw()
        self.file_path = filedialog.askopenfilename()
        return self.file_path   
               
    def verify_csv(self, csv_file):
        #Verify that the file is the correct format
        self.csv_file = csv_file
        if (magic.from_file(self.csv_file, mime=True).__contains__("text/plain") or magic.from_file(self.csv_file, mime=True).__contains__("text/csv")
            or magic.from_file(self.csv_file).__contains__("ASCII text, with very long lines"))  and self.csv_file.__contains__(".csv".lower()):
            return True
        else:
            return False
            
    def csv_import(self, csv_file):
        #import csv of protection job names and return as alist
        file = pd.read_csv(self.csv_file)
        return(file)
        
        
    def __repr__(self):
        #print("Please select a file")
        pass

def main():
     #Create authenticated controller token
    cohesity_client = CohesityUserAuthentication()
    cohesity_url = cohesity_client.get_cluster_fqdn()
    cc = cohesity_client.user_auth()
    
    #Create Bearer Token
    bearer_token = cohesity_client.get_bearer_token(cc)
    
    #Obtain Policy ID
    policy_object = PolicyObject()
    policy_id = policy_object.get_policy_id(cc)
   
   #Obtain Storage Domain ID
    storage_domain_object = StorageDomainObject()
    storage_domain_id = storage_domain_object.get_storage_domain_id(cc)
   
    #Open CSV File
    csv = CsvImport()
    csv_file = csv.open_csv()
    
    #Verify CSV File
    csv_verify = csv.verify_csv(csv_file)
    if csv.verify_csv(csv_file) == True:
       print("File Verified")
    else:
       print("File Failed Verifiecation please select a different file")
    
    #import CSV File
    csv_verified_file = csv.csv_import(csv_file)
    
    #Get Protection Object
    protected_object = ProtectedObjects()
    
    #Get Protection Jobs
    protection_jobs = protected_object.get_protection_jobs(cc, csv_verified_file)
    
    #Recover Protecion Job to a View
    recovery_job = protected_object.recover_nas_list(cc, protection_jobs)
    
    #Get View IDs
    view_object = ViewObject()
    view_id = view_object.get_view_id(cc, csv_verified_file)
    view_protection_job = protected_object.create_view_protection_job(cohesity_url, view_id, cc, bearer_token, policy_id, storage_domain_id)
    
    
    
#Initate Main Function
if __name__ == '__main__':
    main()
  