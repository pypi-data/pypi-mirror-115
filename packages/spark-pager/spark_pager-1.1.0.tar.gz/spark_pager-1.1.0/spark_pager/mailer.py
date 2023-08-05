""" html_text.py formats the mail which will be sent to the end-user """
from .html_text import html
from mailthon import postman, email
from datetime import datetime


def send_mail(username, password, host, port, spark_job):
    today = datetime.today()
    date_format = '%I:%M %p &emsp; &ensp; %m/%d/%y'
    start_time = str(today.strftime(date_format))

    job_id = str(spark_job['jobId'])
    descr  = str(spark_job['jobName'])
    status = str(spark_job['status'])
    num_task = str(spark_job['numTasks'])
    num_active_tasks = str(spark_job['numActiveTasks'])
    num_comp_tasks = str(spark_job['numCompletedTasks'])
    
    msg = html.replace('!!!START_TIME!!!', start_time) \
              .replace('!!!STATUS!!!', status) \
              .replace('!!!JOB_ID!!!', job_id) \
              .replace('!!!DESCR!!!', descr) \
              .replace('!!!NUM_TASKS!!!', num_task) \
              .replace('!!!NUM_ACTIVETASKS!!!', num_active_tasks) \
              .replace('!!!NUM_COMPLETEDTASKS!!!', num_comp_tasks)
    
    p = postman(host=host, port=port, auth=(username, password))
    r = p.send(email(
        content=msg,
        subject="265, `You got Mail`",
        sender="Spark-Pager <spark@pager.com>",
        receivers=[username],
    ))
    assert r.ok
    