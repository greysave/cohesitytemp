#Storage Volume Recovery and Protection from CSV

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
import datetime
import os
import getpass
import csv
import tkinter as tk
from tkinter import filedialog
import magic
import pandas as pd

#User Authentication Token/Controller Object
class CohesityUserAuthentication(object):
    #User Authentication Intialization
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ") 
        self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):
        #Autneticate to the cluster method
        return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

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
class ProtectedObjects(object):       
    def get_protection_jobs(self, cohesity_client, csv_file):
        job_id = []
        self.csv_file = csv_file
        names = []
        self.jobs_list = []
        for i, j in self.csv_file.iterrows():
            names.append(j.Name)
        self.protection_jobs = cohesity_client.protection_jobs
        
        for name in names:
            self.jobs_list.extend(self.protection_jobs.get_protection_jobs(names = name))
        
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
            body.restore_view_parameters.enable_smb_view_discovery = True
            cohesity_client.restore_tasks.create_recover_task(body=body)
            print("The generic nas {Hostname}\\{Name} has been recovered".format(Hostname = j.Hostname, Name = j.Name))
            
    def create_view_protection_job(self, csv_file, cohesity_client, policy_id, storage_domain_id):
        body = ProtectionJobRequestBody()
        body.environment = env.KVIEW
        body.view_box_id = storage_domain_id
        body.policy_id = policy_id
        body.timezone = cohesity_client.cluster.get_cluster().timezone
        for i, j in csv_file.iterrows():
            body.name = j.Name
            body.view_name = j.Name
            cohesity_client.protection_jobs.create_protection_job(body=body)
            print("The Cohesity View protection job {Name} has been created".format(Name = j.Name))
        
        
        
                    
        
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
    cohesity_client = cohesity_client.user_auth()
    policy_object = PolicyObject()
    policy_id = policy_object.get_policy_id(cohesity_client)
    storage_domain_object = StorageDomainObject()
    storage_domain_id = storage_domain_object.get_storage_domain_id(cohesity_client)
    print(policy_id)
    print(storage_domain_id)
    
    #Open and verify CSV File
    #Open CSV File
    csv = CsvImport()
    csv_file = csv.open_csv()
    #Verify CSV File
    csv_verify = csv.verify_csv(csv_file)
    if csv.verify_csv(csv_file) == True:
        print("File Verified")
    else:
        print("File Failed Verifiecation please select a different file")
    #Verify CSV File
    csv_verified_file = csv.csv_import(csv_file)
    protected_object = ProtectedObjects()
    protection_jobs = protected_object.get_protection_jobs(cohesity_client, csv_verified_file)
    recovery_job = protected_object.recover_nas_list(cohesity_client, protection_jobs)
    view_protection_job = protected_object.create_view_protection_job(csv_verified_file, cohesity_client, policy_id, storage_domain_id)
    
    
    
#Initate Main Function
if __name__ == '__main__':
    main()
  