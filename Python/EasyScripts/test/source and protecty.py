#Cohesity Test Easy Script
from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.environment_get_protection_jobs_enum import EnvironmentGetProtectionJobsEnum as envjob
from cohesity_management_sdk.models.environment_list_protection_sources_enum import EnvironmentListProtectionSourcesEnum as envsrc
from cohesity_management_sdk.models.environment_list_application_servers_enum import EnvironmentListApplicationServersEnum as envapp
from cohesity_management_sdk.models.environment_list_protected_objects_enum import EnvironmentListProtectedObjectsEnum as envobj
from cohesity_management_sdk.models.protection_job_request_body import ProtectionJobRequestBody as body
from cohesity_management_sdk.models.environment_enum import EnvironmentEnum as env
import datetime
#import os
import getpass
#import sys

class CohesityException(Exception):
    pass

class AuthenticationException(CohesityException):
    pass
class ProtectionSourceList(object):
    pass

class CohesityUserAuthentication(object):
    
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ") 
        self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):     
      return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

class CreateVMProtectionJob(object):
    def __init__(self, body):
        pass
    def check_protection_job_exists(self):
        pass
    def check_protection_source_exists(self):
        pass
    def get_vm_list(self, cohesity_client):
        vms = []
        self.protection_sources = cohesity_client.protection_sources
        self.vm_list = self.protection_sources.list_virtual_machines(protected=False)
        for item in self.vm_list:
            vms.append(item)
        return vms
    def protect_vms(self, cohesity_client, body):
        protect_vms = cohesity_client.protection_jobs()
        
        
    
def main():
    #Authenticate to the Cluster
    cohesity_client = CohesityUserAuthentication()
    cohesity_client = cohesity_client.user_auth()
    
    #Get a list of VMs on the Cluster
    vm_list = CreateVMProtectionJob()
    for item in vm_list.get_vm_list(cohesity_client):
        if item.name == "LINUX_Client" or "WIN_Client" or "GATEWAY":
            body.name == item.name
    body.policy_id = policy_id

        

  

if __name__ == '__main__':
    main()




