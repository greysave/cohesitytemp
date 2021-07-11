#Cohesity Test Easy Script
from cohesity_management_sdk.cohesity_client import CohesityClient
import datetime
#import os
import getpass
#import sys

class CohesityException(Exception):
    pass

class AuthenticationException(CohesityException):
    pass
class CohesityUserAuthentication(object):
    

    def __init__(self):
        """
        
        """
        self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ") 
        self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):     
      return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

class ProtectionJobsList(object):
    
    def display_protection_jobs(self, cohesity_client):
        """
        Method to display the list of Active
        :param cohesity_client(object): Cohesity client object.
        :return:
        """
        self.protection_jobs = cohesity_client.protection_jobs
        self.jobs_list = self.protection_jobs.get_protection_jobs()
        for job in self.jobs_list:
            print ('{0:<10}\t\t{1:>8}'.format(
                self.epoch_to_date(job.creation_time_usecs), job.name))
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

class EnvironmentProtectionJobList(ProtectionJobsList):
       
    def display_vm_protection_job(self, environment):
        """
        Method to display a list of VM Protection Jobs
        Inherited from display_protection_jobs)
        :param environment(string)
        """
        super().display_protection_jobs(environment)
#Generate a token to log into the cohesity client

def main():
    #Authentication Instansiation
    cohesity_client = CohesityUserAuthentication()
    cohesity_client = cohesity_client.user_auth()
    #Getting Cluster Info
    """ 
    cohesity_controller = cohesity_client.cluster
    result = cohesity_controller.get_basic_cluster_info()
    result_dict = result.__dict__
    print(result_dict['domains'])
    """
    #Get all protection jobs
    """   
    protect_object = ProtectionJobsList()
    protect_object.display_protection_jobs(cohesity_client)
    """
    #environments = [EnvironmentGetProtectionJobsEnum.K_VMWARE]
    #result = protection_jobs_controller.get_protection_jobs(None, None, None, environments)

    

if __name__ == '__main__':
    main()




