from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.environment_get_protection_jobs_enum import EnvironmentGetProtectionJobsEnum as envjob
from cohesity_management_sdk.models.environment_list_protection_sources_enum import EnvironmentListProtectionSourcesEnum as envsrc
from cohesity_management_sdk.models.environment_list_application_servers_enum import EnvironmentListApplicationServersEnum as envapp
from cohesity_management_sdk.models.environment_list_protected_objects_enum import EnvironmentListProtectedObjectsEnum as envobj
from cohesity_management_sdk.models.protection_job_request_body import ProtectionJobRequestBody as body
from cohesity_management_sdk.models.environment_enum import EnvironmentEnum as env
from cohesity_management_sdk.models.environment_list_protection_sources_registration_info_enum import EnvironmentListProtectionSourcesRegistrationInfoEnum as envreg
from cohesity_management_sdk.models.environment_list_protection_sources_root_nodes_enum import EnvironmentListProtectionSourcesRootNodesEnum as envnode
from cohesity_management_sdk.models.access_token_credential import AccessTokenCredential
import datetime
import os
import getpass
import json
import requests

class CohesityUserAuthentication(object):
    
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_fqdn = "localhost:52182"
        self.username = "gsavage@VCD"
        self.password = "Sa9e$2y!"
        self.domain = "local"
        # self.cluster_fqdn = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ") 
        # self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):     
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
  
class ProtectionObject(object):
    def list_vm_protection_source(self, cohesity_client, vm_env):
        self.protection_sources = cohesity_client.protection_sources
        self.source_list = self.protection_sources.list_protection_sources(environments = vm_env)
            
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

    def get_v_app_protection_source(self, cohesity_url, source_id, bearer_token):
            #REST API Headers and auth
            headers = {"Authorization": "Bearer %s" % bearer_token.access_token}
            #REST API Url
            #url = 'https://{cohesity_url}/irisservices/api/v1/public/protectionSources?IncludeSystemVApps=true&includeVMFolders=false&environments=kVMware&includeEntityPermissionInfo=false'.format(cohesity_url=cohesity_url)   
            url = 'https://{cohesity_url}/irisservices/api/v1/public/protectionSources?excludeTypes=kVCenter&excludeTypes=kFolder&excludeTypes=kDatacenter&excludeTypes=kHostSystem&excludeTypes=kResourcePool&excludeTypes=kVirtualMachine&excludeTypes=kStandaloneHost&excludeTypes=kVirtualApp'.format(cohesity_url=cohesity_url)
            sources = []
            #Rest API payload thorugh loop
            for source in source_id:
                payload = {"includeVMFolders": True, "includeSystemVApps": True, "id": source}                
                res = requests.get(url=url, headers=headers, data=json.dumps(payload), verify=False)
                return res.json()
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
    cohesity_url = cohesity_client.get_cluster_fqdn()
    

    protect_object = ProtectionObject()
    tenant_object =TenantObject()
    #tenant_list = tenant_object.get_tenant_ids(cc)
    vm_list_source = protect_object.list_vm_protection_source(cc, vm_env_src)
    objlst =[]
    for item in vm_list_source:
        # if item.protection_source.vmware_protection_source.name.__contains__(""):
        src_id = item.protection_source.vmware_protection_source.id
        print(dir(src_id))
        objlst.extend(cc.protection_sources.get_protection_sources_objects())
    print(objlst)
    for obj in objlst:
        print(obj.vmware_protection_source.mtype)
    bearer_token = cohesity_client.get_bearer_token(cc)


    org_name = "SEC"
    #Get source ID
    source_id = protect_object.get_source_id(vm_list_source)
    #print(source_id)
    vapp_list = protect_object.get_v_app_protection_source(cohesity_url, source_id, bearer_token)

    
    # print(dir(vapp_list))
    org_list = []
    for app in vapp_list:
        if 'nodes' in app:
            orgs = [o for o in app['nodes'] if o['protectionSource']['vmWareProtectionSource']['type'] == 'kOrganizaation']
        for org in orgs:
            org_temp = org['protectionSource']['name']
            print(org['protectionSource']['name'])
            org_list.append(org['protectionSource']['name'])
    vapp_temp = []
    for vdc in org_list:
        if 'nodes' in app:
            vdcs = [o for o in vdc['nodes'] if o['protectionSource']['vmWareProtectionSource']['type'] == 'kVDC']
        for vapp in vapp_temp:
            print(vapp['protectionSource']['name'])


    # for k, v in org.items():
    #      if "nodes" in k:
    #         for item in v:
    #             for k1, v1 in item.items():
    #                 if "protectionSource" in k1:
    #                     for k2, v2 in v1.items():
    #                         if k2.__contains__("vmWareProtectionSource"):
    #                             for k3, v3 in v2.items():
    #                                 if k3.__contains__("type") and v3 == "kOrganization":
    #                                     print(v3)
    #                                 if k3.__contains__("name") and v3 == org_name:
    #                                     print(v3)
    #                                 #     for k4, v4 in v3.items():
    #                                 #         print(k4, "->", v4)


    # vapp_template = vapp_list[0]
    # for k, v in org.items():
    #      if "nodes" in k:
    #         for item in v:
    #             for k1, v1 in item.items():
    #                 if "nodes" in k1:
    #                     # for item1 in v1.items():
    #                         # for k2, v2 in v1.items():
                            # print(k1, "")
                #     if "nodes" in k1:
                #             for item1 in v1:
                #                 print("The key is {key} and the value is {value}".format(key = k1,value = item1))
                            #print("The key is {key} and the value is {value}".format(key=k1,value=v1))                   
                   # print(k1["protectionSource"])

    org1 = vapp_list[0]

    # for k, v in org1.items():
    #     print("The key is {key} and the value is {value}".format(key=k,value=v))
    # for k, v in org1.items():
    #     print(k, '->', type(v))
    #     print(k['protectionSource'])

    #print(org)
    # print(type(vapp_list))
    # encode = json.dumps(vapp_list, indent=1)
    # if encode.
    # print(encode)
    # 
        #  for k, v in vapp.items():
        #      for item in v:
        #          if item.__contains__("nodes"):
        #              for k1,v1 in item.items():
        #                  print(k1)
        #                  if k1.__contains__('nodes') and type(k1) is list:
        #                      print(k1, '->', type(v1), v1)
        
    #print(type(vapp_list.json()))
    # for k, v in vapp_list.items():
    #     for k1 in v1 in v.items():
    #         print(k1)
    # for app in vapp_list:
    #     for k, v in app.items():
            
    #     #     #if (k["protectionSource"]["vmWareProtectionSource"]["type"]) == "kVirtualApp":
    #         for item in v:
    #             print(item['type'])
        # print(app['protectionSource'])
            
                # print(app["protectionSource"]["vmWareProtectionSource"]["name"])
                
    
    
    # for source in vm_list_source:
    #     print(dir(source.protection_sources))

    # for source in source_id:
    #     # result = cc.protection_sources.get_protection_sources_objects(object_ids = source.protection_source.id)
    #     result = cc.protection_sources.get_protection_sources_objects(object_ids=source)
    #     for  item in result:
    # # #print(item.name)
    # #     for sources in source_id:
    # #         # print(sources)
    #         #if  item.parent_id == source:# and "CAT" in result:
    #         #if item.name.__contains__("CAT"):
    #         print(item.vmware_protection_source.vcloud_director_info)

     
    #print(tenant_list)

if __name__ == '__main__':
    main()
