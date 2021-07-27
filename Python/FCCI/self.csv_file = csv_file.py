 self.csv_file = csv_file
        names = []
        self.jobs_list = []
        for i, j in self.csv_file.iterrows():
            names.append(j.Name)
        self.protection_jobs = cohesity_client.protection_jobs
        self.job_test = self.protection_jobs.get_protection_jobs()
        #for name in names:
        self.jobs_list.append(self.protection_jobs.get_protection_jobs(names = names))
        print(self.jobs_list)
            
        for job in self.jobs_list:
            #Add new column to CSV with jobID
            self.csv_file["JobID"] = job.id
            print(job.id)
            return csv_file