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


class ProtectedObjects(object):
    def get_protection_jobs(self, cohesity_client, csv_file):
        self.csv_file = csv_file
        names = []
        for i, j in self.csv_file.iterrows():
            names.append(j.Name)
        self.protection_jobs = cohesity_client.protection_jobs
        self.jobs_list = self.protection_jobs.get_protection_jobs(names = "gregtest")
        for job in self.jobs_list:
            #Add new column to CSV with jobID
            csv_file["JobID"] = job.id
            return csv_file
            
       
            #return jobs
    
    def test(self, cohesity_client, file):
        pass
    def recover_nas_list(self, cohesity_client, csv_file):
        self.csv_file = csv_file
        #self.job_name = list(self.csv_file.Hostname + "-" + self.csv_file.Name)
        #
        testlist = []
       
        self.protection_jobs = cohesity_client.protection_jobs
        for i, j in csv_file.iterrows():
            #Create Recovery Task
            body = RecoverTaskRequest()
            body.mtype = 'kMountFileVolume'
            body.objects = []
            body.objects.append(RestoreObjectDetails())
            body.name = "Recover-{name}".format(name = j.Name)
            body.objects[0].job_id = j.JobID
            #Update View Parameters
            body.restore_view_parameters = UpdateViewParam()
            body.restore_view_parameters.protocol_access = ProtocolAccessEnum.KSMBONLY
            body.restore_view_parameters.enable_smb_view_discovery = True
            
            cohesity_client.restore_tasks.create_recover_task(body=body)
            
        #     for item in self.job_name:
        #         body.name = self.name
        #         body.objects.job_name = self.job_name
        #         #testlist.append(body.name, body.job_name)
        #         return item
                
            # body.objects.append(RestoreObjectDetails())
            # body.objects.job_name = self.job_name
        #return job_name
            #return body.job_name
            
            
        
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
#Volume Recovery Class
class VolumeRecovery(object):
    pass
#Protection Job Class
class CreateProtectionJob(object):
    pass

def main():
     #Create authenticated controller token
    cohesity_client = CohesityUserAuthentication()
    cohesity_client = cohesity_client.user_auth()
    
    #Open and verify CSV File
    csv = CsvImport()
    csv_file = csv.open_csv()
    csv_verify = csv.verify_csv(csv_file)
    #print(dir(pd))
    if csv.verify_csv(csv_file) == True:
        print("File Verified")
    else:
        print("File Failed Verifiecation please select a different file")
    csv_verified_file = csv.csv_import(csv_file)
    #print(csv_verified_file)
    #csv_protection_job_name = list(csv_verified_file.Hostname + "-" + csv_verified_file.Name)
   # print(csv_protection_job_name)
    # obj_restore = ProtectedObjects.recover_nas_list(cohesity_client, csv_file)
    # print(obj_restore)
    protected_object = ProtectedObjects()
    protection_jobs = protected_object.get_protection_jobs(cohesity_client, csv_verified_file)
    #print(protection_jobs)
    recvery_job = protected_object.recover_nas_list(cohesity_client, protection_jobs)
    
    
    
#Initate Main Function
if __name__ == '__main__':
    main()
  