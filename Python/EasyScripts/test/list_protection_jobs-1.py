# Copyright 2019 Cohesity Inc.
#
# Python example to get a list Protection jobs.
#
# Usage: python list_protection_jobs.py

import datetime
import os

from cohesity_app_sdk.app_client import AppClient
from cohesity_management_sdk.cohesity_client import CohesityClient


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
        
    


def get_mgmt_token():
    """
    To get the management access token from App Server to authenticate
    :return: mgmt_auth_token
    """
    # Get the Environment variables from App Container.
    app_auth_token = os.getenv('APP_AUTHENTICATION_TOKEN')
    app_endpoint_ip = os.getenv('APPS_API_ENDPOINT_IP')
    app_endpoint_port = os.getenv('APPS_API_ENDPOINT_PORT')

    # Initialize the client.
    app_cli = AppClient(app_auth_token, app_endpoint_ip, app_endpoint_port)
    app_cli.config.disable_logging()

    settings = app_cli.settings
    print(settings.get_app_settings())

    # Get the management access token.
    token = app_cli.token_management
    mgmt_auth_token = token.create_management_access_token()
    return mgmt_auth_token


def main():

    # Login to the cluster
    host_ip = os.getenv('10.26.0.159')
    mgmt_auth_token = get_mgmt_token()
    cohesity_client = CohesityClient(cluster_vip=host_ip, auth_token=mgmt_auth_token)

    # Getting and listing protection jobs
    protect_object = ProtectionJobsList()
    protect_object.display_protection_jobs(cohesity_client)

if __name__ == '__main__':
    main()
