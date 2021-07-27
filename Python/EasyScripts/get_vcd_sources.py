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
  
class ProtectionObject(object):
    def list_vm_protection_source(self, cohesity_client, vm_env):
        sources = []
        self.protection_sources = cohesity_client.protection_sources
        self.source_list = self.protection_sources.list_protection_sources(environments = vm_env)
        return self.source_list
        # for source in self.source_list:
        #     sources.append(source)
        #     print(dir(source))
        # return sources

    def get_protection_object(self):
        pass
    
def main():
    #Set environment Variables
    vm_env_src = [envsrc.K_VMWARE]
    env_enum = [env.K_VMWARE]
    #Authentication Instansiation
    cohesity_client = CohesityUserAuthentication()
    try:
        cohesity_client = cohesity_client.user_auth()
    except:
        pass

    #Get all protection jobs
    protect_source = {}
    protect_object = ProtectionObject()
    vm_list_source = protect_object.list_vm_protection_source(cohesity_client, vm_env_src)
    for source in vm_list_source:
        protect_source[source.protection_source.name] = source.protection_source.id
        #print(z)
    #print(dir(protect_source))
    # for item in protect_source.items():
    #     print(item)
    #     if "vcloud" in item:
    #         print(protect_source[item])
    for k, v in protect_source.items():
        if "vcloud" in k:
            print(protect_source[k])
     

if __name__ == '__main__':
    main()
