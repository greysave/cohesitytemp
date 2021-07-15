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
#CSV Import Class
class CsvImport(object):
    def __init__(self):
        self.root = tk.tk()
        self.root.withdraw()
        self.file_path = filedialog.askopenfilename()
    def csv_import(self, csv_org_file):
        with open(self.csv_file, "rt") as infile, open(self.csv_mod_file, "wt") as outfile:
            reader = csv.reader(infile)
            next(reader, None)
    def __repr__(self):
        print("Please select a file")
#Volume Recovery Class
class VolumeRecovery(object):
    pass
#Protection Job Class
class CreateProtectionJob(object):
    pass

def main():
    pass
    #Create authenticated controller token
    # cohesity_client = CohesityUserAuthentication()
    # cohesity_client = cohesity_client.user_auth()
    

#Initate Main Function
if __name__ == '__main__':
    main()
  