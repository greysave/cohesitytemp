#Cohesity Test Easy Script
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


class ProtectionJobsList(object):
    
    def get_protection_jobs(self, cohesity_client):
        """
        Method to display the list of Active
        :param cohesity_client(object): Cohesity client object.
        :return:
        """
        jobs = []
        self.protection_jobs = cohesity_client.protection_jobs
        self.jobs_list = self.protection_jobs.get_protection_jobs()
        for job in self.jobs_list:
            # jobs.append('{0:<10}\t\t{1:>8}'.format(
            # self.epoch_to_date(job.creation_time_usecs), job))
            jobs.append(job)
        return jobs 
    @staticmethod
    def epoch_to_date(epoch):
        """
        Method to convert epoch time in usec to date format
        :param epoch(int): Epoch time of the job run.
        :return: date(str): Date format of the job runj.
        """
        date = datetime.datetime.fromtimestamp(epoch/10**6).\
            strftime('%m-%d-%Y %H:%M:%S')
        return date

class EnvProtectionJobList(ProtectionJobsList):
       
    def get_env_protection_job(self, cohesity_client, environments):
        """
        Method to display a list of VM Protection Jobs
        Inherited from display_protection_jobs)
        :param environment(string)
        """
        self.environments = environments
        jobs = []
        self.protection_jobs = cohesity_client.protection_jobs
        self.jobs_list = self.protection_jobs.get_protection_jobs(environments = self.environments)
        for job in self.jobs_list:
            jobs.append('{0:<10}\t\t{1:>8}'.format(
                self.epoch_to_date(job.creation_time_usecs), job.name))
        return jobs

class ProtectionSourceObj(object):

    def list_protection_obj(self, cohesity_client):
        sources = []
        self.protection_sources = cohesity_client.protection_sources
        self.source_list = self.protection_sources.get_protection_sources_objects()
        for source in self.source_list:
            sources.append(source.name)
        return sources

class ProtectionSourceList(object):
    def list_protection_source(self, cohesity_client):
        sources = []
        self.protection_sources = cohesity_client.protection_sources
        self.source_list = self.protection_sources.list_protection_sources()
        for source in self.source_list:
            sources.append(source.name)

class EnvProtectionSourceList(ProtectionSourceList):
    def list_env_protection_source(self, cohesity_client, environments):
        sources = []
        self.protection_sources = cohesity_client.protection_sources
        self.source_list = self.protection_sources.list_protection_sources(environments = self.environments)
        for source in self.source_list:
            sources.append(source.name)
        return sources

 
# class EnvProtectionSourceAppList(ProtectionSourceList):
#     def list_app_protection_source(self, cohesity_client, environments):
#         sources = []
#         self.protection_sources = cohesity_client.protection_sources
#         self.source_list = self.protection_sources.list_protectection_objects(environments = self.environments)
#         for source in self.source_list:
#             sources.append(source.name)
#         return sources

class ProtectionJobCreate(object):
    def create_protection_job(self, name, policy_id, view_box_id):
        pass


#Generate a token to log into the cohesity client

def main():
    env_source = [envsrc.K_VMWARE]
    env_enum = [env.K_VMWARE]
    #Authentication Instansiation
    
    cohesity_client = CohesityUserAuthentication()
    try:
        cohesity_client = cohesity_client.user_auth()
    except:
        pass
    #Getting Cluster Info

    #environments = [EnvironmentGetProtectionJobsEnum.K_VMWARE]
    #result = ProtectionJobsList
    #result.display_protection_jobs(cohesity_client)
    
    """ 
    cohesity_controller = cohesity_client.cluster
    result = cohesity_controller.get_basic_cluster_info()
    result_dict = result.__dict__
    print(result_dict['domains'])
    """
    #Get all protection jobs
    print(" \n \n All Jobs")
    protect_object = ProtectionJobsList()
    for item in protect_object.get_protection_jobs(cohesity_client):
        print(item)
    
    protection_job_body =  body
    print(type(protection_job_body))
    protect_object_2 = cohesity_client.protection_jobs.get_protection_jobs()
    
    for item in protect_object_2:
        if item.environment == "kVMware" :
            protection_job_body.name = '{protection_job} Protection Job'.format(protection_job = item.name)
            print(protection_job_body.name)
        else:
            print("This is not VMWare")

    #Loop through the protection source and query for the name and environment
    protect_source_2 = cohesity_client.protection_sources.list_protection_sources()
    #print(dir(protect_source_2))
    for item in protect_source_2:
        print(dir(item))
        if item.protection_source.environment == env_enum[0]:
            print("{name} is of the {envio} type.".format(name = item.protection_source.name, envio = item.protection_source.environment))
        #print(dir(item.unprotected_sources_summary))
        
    
          
        
       
        # if item.environment == env_enum[0]:
        #     print(item.name)
            


    
        
    
    # print(' \n \n VM Jobs')
    # vm_env = [envjob.K_VMWARE]
    # vm_object = EnvProtectionJobList()
    # for item in vm_object.get_env_protection_job(cohesity_client, vm_env):
    #     print(item)

    # print(" \n \n Protection Sources")
    # protect_soucre = ProtectionSourceObj()
    # for item in protect_soucre.list_protection_obj(cohesity_client):
    #     print(item)
    

    print(" \n \n Protection Environment Sources",)
    #print(dir(list_env_protection_source))
    print(dir(envsrc))
    #vm_envi = [envapp.K_VMWARE]
    #vm_source = EnvProtectionSourceList()
    # print(vm_env)
    # print(type(vm_env))
    # print(dir(vm_env))
    # env_source = [envsrc.K_VMWARE]
    env_protect_source = EnvProtectionSourceList()
    
        
    #print(dir(envsrc))
    #environments = [EnvironmentGetProtectionJobsEnum.K_VMWARE]
    #$test_env = K_VMWARE
    #result = cohesity_client.protection_sources.list_protection_sources(environments = env_source)
    # for item in result:
    #     print(item)

    # for item in env_protect_source.list_env_protection_source(cohesity_client, environments=env_source):
    #     print(item)
    # print(dir())

    # result = cohesity_client.protection_sources.list_protected_objects(environment= env_source)

    # print(result)


    #print(type(cohesity_client))

if __name__ == '__main__':
    main()




