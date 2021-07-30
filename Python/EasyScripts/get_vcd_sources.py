from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.environment_get_protection_jobs_enum import EnvironmentGetProtectionJobsEnum as envjob
from cohesity_management_sdk.models.environment_list_protection_sources_enum import EnvironmentListProtectionSourcesEnum as envsrc
from cohesity_management_sdk.models.environment_list_application_servers_enum import EnvironmentListApplicationServersEnum as envapp
from cohesity_management_sdk.models.environment_list_protected_objects_enum import EnvironmentListProtectedObjectsEnum as envobj
from cohesity_management_sdk.models.protection_job_request_body import ProtectionJobRequestBody as body
from cohesity_management_sdk.models.environment_enum import EnvironmentEnum as env
from cohesity_management_sdk.models.environment_list_protection_sources_registration_info_enum import EnvironmentListProtectionSourcesRegistrationInfoEnum as envreg
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
    def list_vm_protection_source(self, cohesity_client, vm_env, tenant_list):
        sources =[]
        self.protection_sources = cohesity_client.protection_sources
        #Add default org
        self.source_list = self.protection_sources.list_protection_sources(environments = vm_env)
        #Add tenants
        if len(tenant_list) > 0:
            for tenants in tenant_list:
                self.source_list.extend(self.protection_sources.list_protection_sources(environments = vm_env, tenant_ids = tenants))
        
        return self.source_list
        

    def get_source_id(self, source_list):
        protect_source = {}
        return_list = []
        
        for source in source_list:
            protect_source[source.protection_source.name] = source.protection_source.id
            
        for k, v in protect_source.items():
            if "vcloud" in k:
                #print(protect_source[k])
                return_list.append(protect_source[k])
        return return_list
    
    def get_protection_object(self):
        pass

class TenantObject(object):
    def get_tenant_ids(self, cohesity_client):
        self.tenant_list = []
        self.tenant = cohesity_client.tenant
        self.tenants = self.tenant.get_tenants()
        for tenant in self.tenants:
            self.tenant_list.append(tenant.tenant_id)
        return self.tenant_list
    

    
def main():
    #Set environment Variables
    vm_env_src = [envsrc.K_VMWARE]
    env_enum = [env.K_VMWARE]
    #Authentication Instansiation
    cohesity_client = CohesityUserAuthentication()
    try:
        cc = cohesity_client.user_auth()
    except:
        pass

    #Get all protection jobs
    
    protect_object = ProtectionObject()
    tenant_object =TenantObject()
    tenant_list = tenant_object.get_tenant_ids(cc)
    vm_list_source = protect_object.list_vm_protection_source(cc, vm_env_src, tenant_list)
    
    

    #Get source ID
    source_id = protect_object.get_source_id(vm_list_source)
    
    # for source in vm_list_source:
    #     print(dir(source.protection_sources))

    for source in source_id:
        # result = cc.protection_sources.get_protection_sources_objects(object_ids = source.protection_source.id)
        result = cc.protection_sources.get_protection_sources_objects()
        for  item in result:
    # #print(item.name)
    #     for sources in source_id:
    #         # print(sources)
            if  item.parent_id == source and item.name.__contains__("CAT"):
                print(item.name)

     
    #print(tenant_list)

if __name__ == '__main__':
    main()
