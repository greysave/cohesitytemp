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
        pass

    def user_auth(self, cluster_ip = getpass._raw_input("Please enter the cluster VIP"), username = getpass._raw_input("Please Enter the username:"), password = getpass.getgetpass.getpass(prompt='Please enter the user password: ', stream=None), domain = getpass._raw_input("Please Enter the user domain:")):
        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.domain = domain
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

#Generate a token to log into the cohesity client


def main():
    access = CohesityUserAuthentication.user_auth()





