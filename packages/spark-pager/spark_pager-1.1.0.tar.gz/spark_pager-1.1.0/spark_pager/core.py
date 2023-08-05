""" coding .:: utf-8 """
import threading
import json
import requests
from .mailer import send_mail

class Pager():
    """
    Description:
    """
    def __init__(self, spark_context, username, password, host='smtp.gmail.com', port=587):
        self.spark_context = spark_context
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.event = True
        self.tr = threading.Thread(target=self.get_spark_jobs, name="Spark_Jobs")
            

    def parse_spark_job(self, res, completed_jobs):
        """
        Description :
        """
        current_job = json.dumps(res)
        
        if current_job in completed_jobs:
            pass
        else:
            send_mail(self.username, self.password, self.host, self.port, res)
             
                
    def get_spark_jobs(self):
        """
        Description:
        
        """
        spark_ui = self.spark_context.uiWebUrl
        app_id = self.spark_context.applicationId
        url = f'{spark_ui}/api/v1/applications/{app_id}/jobs'
        
        completed_jobs = set()
        while self.event:
            spark_jobs = self.spark_context.statusTracker().getJobIdsForGroup() ###-> [2,1,0]
            if spark_jobs:
                req = requests.get(url) \
                              .json()[0]
                
                res = {'jobId': req['jobId'], 
                       'jobName': req['name'], 
                       'status': req['status'],
                       'numTasks': req['numTasks'],
                       'numActiveTasks': req['numActiveTasks'],
                       'numCompletedTasks': req['numCompletedTasks']}
                
                self.parse_spark_job(res, completed_jobs)
                completed_jobs.add(json.dumps(res))
                

    
    def listener(self):
        """
        Description:
        
        """
        self.tr.start()
        
        
    def stop(self):
        """
        Description:
        """
        self.event = False

        