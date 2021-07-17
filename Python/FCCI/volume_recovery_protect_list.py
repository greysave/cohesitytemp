#Storage Volume Recovery and Protection from CSV

from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.environment_get_protection_jobs_enum import EnvironmentGetProtectionJobsEnum as envjob
from cohesity_management_sdk.models.environment_list_protection_sources_enum import EnvironmentListProtectionSourcesEnum as envsrc
from cohesity_management_sdk.models.environment_list_application_servers_enum import EnvironmentListApplicationServersEnum as envapp
from cohesity_management_sdk.models.environment_list_protected_objects_enum import EnvironmentListProtectedObjectsEnum as envobj
from cohesity_management_sdk.models.protection_job_request_body import ProtectionJobRequestBody as body
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
        # self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ") 
        # self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):
        #Autneticate to the cluster method
        return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)


class ProtectedObjects(object):
    def get_protection_jobs(self, cohesity_client, job_list):
        pass
        self.job_list = job_list
        jobs = []
        self.protection_jobs = cohesity_client.protection_jobs
        self.jobs_list = self.protection_jobs.get_protection_jobs()
        for job in self.jobs_list:
            jobs.append(job.name)
        
#CSV Import Class
class CsvImport(object):
    def __init__(self):
        pass
    
    def open_csv(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.file_path = filedialog.askopenfilename()
        return self.file_path   
               
    def verify_csv(self, csv_file):
        self.csv_file = csv_file
        if (magic.from_file(self.csv_file, mime=True).__contains__("text/plain") or magic.from_file(self.csv_file, mime=True).__contains__("text/csv")
            or magic.from_file(self.csv_file).__contains__("ASCII text, with very long lines"))  and self.csv_file.__contains__(".csv".lower()):
            return True
        else:
            return False
            
    def csv_import(self, csv_file):
        #import csv of protection job names and return as alist
        file = pd.read_csv(self.csv_file)
        return(file.Hostname + '-' + file.Name)
        
        
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
    csv_verified_file = list(csv.csv_import(csv_file))
    
    
    
        
    
   
    

#Initate Main Function
if __name__ == '__main__':
    main()
  