import requests
import json
import os
from job_info import get_job_info
auth_token = os.environ['USER_TOKEN']
condor_job_url = os.environ['CONDOR_JOB_URL']

def get_report_jobs():
    # Get jobs
    running_jobs_constraint = "constraint=jobstatus==2"
    queued_jobs_constraint = "constraint=jobstatus==1"
    response_running = requests.get(condor_job_url + running_jobs_constraint,
                                    headers={'Authorization': auth_token})
    response_queued = requests.get(condor_job_url + queued_jobs_constraint,
                                   headers={'Authorization': auth_token})
    json_data_running = json.loads(response_running.text)
    json_data_queued = json.loads(response_queued.text)
    total_jobs = json_data_running + json_data_queued
    job_info_by_queue = get_job_info(total_jobs)
    job_info_by_queue['total_queued'] = len(json_data_queued)
    job_info_by_queue['total_running'] = len(json_data_running)

    return job_info_by_queue
