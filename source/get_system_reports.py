import numpy as np
import client as c
import json
import requests
import datetime
import os
import sys
from createslots import create_dynamic_slots, create_partionable_slots
from calculate_queue_resources import calculate_queues_total, get_job_info
from generate_slot_report import generate_cg_report
from calculate_total_memory_resources import calculate_total_cpus_memory_disk
auth_token = os.environ['USER_TOKEN']
condor_machine_url = os.environ['CONDOR_MACHINE_URL']
condor_job_url = os.environ['CONDOR_JOB_URL']


def get_system_report():
    """
    System Metrics is composed primarily of a Condor Scraper that scraps machine information and job information from
    the Condor REST API.
    This function merges the machine metrics dictionary with the job metrics dictionary by queue name.
    Once all the information is consolidated new keys, such as utilization and the final 'type' key needed for Logstash
    is added and the logs sent to Logstash.
    """
    machine_metrics = get_report_machines()
    job_metrics = get_report_jobs()
    # Job metrics coming from Condor should never be equal to 1 or 0
    if len(job_metrics) <= 1:
        print(job_metrics)
        sys.exit("Error: queue information invalid to capture job metrics! Please check the formatting of the 'requirements' key for Condor jobs and make sure the parsing in 'get_jobs_info' is valid. ")
    # Loop through queues
    queues = ['njs', 'bigmem', 'bigmemlong', 'concierge', 'kb_upload']
    # The queue info array dict is here for debugging
    queue_info_array = []
    for queue in queues:
        # If job information is available for a queue it means a job(s) is running or idle in that queue
        if queue in job_metrics.keys():
            # Update machine metrics dictionary at queue with the job information fount
            machine_metrics[queue].update(job_metrics[queue])
        queue_info_temp = machine_metrics['queue_info']
        queue_dict = machine_metrics[queue]
        queue_dict.update(queue_info_temp[queue])
        queue_dict["queue"] = queue
        queue_dict["timestamp"] = machine_metrics['timestamp']
        queue_dict["environment"] = machine_metrics['environment']
        queue_dict["reserved"]['hosts'] = machine_metrics[queue]['claimed']
        queue_dict["available"]['hosts'] = machine_metrics[queue]['unclaimed']
        queue_dict['utilization_hosts'] = np.float64(queue_dict['reserved']['hosts'])/queue_dict['available']['hosts']
        queue_dict['utilization_cpus'] = np.float64(queue_dict['reserved']['cpus'])/queue_dict['available']['cpus']
        queue_dict['utilization_disk'] = np.float64(queue_dict['reserved']['disk_gb'])/queue_dict['available']['disk_gb']
        queue_dict['utilization_memory'] = np.float64(queue_dict['reserved']['memory_gb'])/queue_dict['available']['memory_gb']
        queue_dict["type"] = "schedulermetrics2"
        # the output of queue_info_array will be the same as the output sent to logstash
        queue_info_array.append(queue_dict)
        c.to_logstashJson(json.dumps(queue_dict))
        del machine_metrics['queue_info'][queue]
        del machine_metrics[queue]
        
    print("Total Machine Information")
    del machine_metrics['queue_info']
    print("Total claimed hosts", machine_metrics['claimed'])
    print("Total available hosts", machine_metrics['unclaimed'])
    print("Total hosts", machine_metrics['total_hosts'])
    print("Total resources", machine_metrics['total_resources'])
    print("{} queue records have been added to Logstash".format(len(queue_info_array)))

    
def get_report_machines():
    """
    The dictionary returned by get_report_machines should be static and constant.
    Each queue should always have basic memory/cpu/disk stats.
    """
    now = datetime.datetime.now().isoformat()
    # Get machines
    response = requests.get(condor_machine_url, headers={'Authorization': auth_token})
    json_data = json.loads(response.text)
    print("Repsonse status code is", response.status_code)

    # Account for slots on machines
    unclaimed = json_data.get('Unclaimed')
    claimed = json_data.get('Claimed')

    partionable_slots = create_partionable_slots(claimed=claimed, unclaimed=unclaimed)
    print("Partionable slots found:", len(partionable_slots))

    dynamic_slots = create_dynamic_slots(claimed=claimed)
    print("Dynamic Slots:", len(dynamic_slots))

    print("Creating actual memory/cpu/disk usages, rather than reserved")
    for slot in partionable_slots:
        partionable_slots[slot].calculate_actual_usage(input_dynamic_slots=dynamic_slots)

    host_report = generate_cg_report(partionable_slots)
    # The initialization of machine dictionary and resources
    total_hosts = len(partionable_slots)
    total_resources = calculate_total_cpus_memory_disk(partionable_slots)
    queue_dict = {}
    queue_info = calculate_queues_total(partionable_slots, queue_dict)
    memory_metrics_dict = {'timestamp': now,
                           'environment': condor_machine_url,
                           'total_hosts': total_hosts,
                           'total_resources': total_resources,
                           'queue_info': queue_info}
    memory_metrics_dict.update(host_report)
    
    return memory_metrics_dict

def get_report_jobs():
    """Gets all jobs running or idle in Condor and then separates by queue/kb_clientgroup."""
    # Get running (2) and idle (1) jobs from Condor
    running_jobs_constraint = "constraint=jobstatus==2"
    queued_jobs_constraint = "constraint=jobstatus==1"
    response_running = requests.get(condor_job_url + running_jobs_constraint,
                                    headers={'Authorization': auth_token})
    response_queued = requests.get(condor_job_url + queued_jobs_constraint,
                                   headers={'Authorization': auth_token})
    json_data_running = json.loads(response_running.text)
    json_data_queued = json.loads(response_queued.text)
    total_jobs = json_data_running + json_data_queued
    # Allocate total jobs to the get_job_info function for heavy data lifting
    job_info_by_queue = get_job_info(total_jobs)
    job_info_by_queue['total_queued'] = len(json_data_queued)
    job_info_by_queue['total_running'] = len(json_data_running)

    return job_info_by_queue
