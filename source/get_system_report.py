from get_report_machines import get_report_machines
from get_report_jobs import get_report_jobs
import client as c

def get_system_report():
    machine_metrics = get_report_machines()
    job_metrics = get_report_jobs()
    queues = ['njs', 'bigmem', 'bigmemlong', 'concierge', 'kb_upload']
    queue_dictionary = {}
    queue_info_array = []
    for queue in queues:
        if queue in job_metrics.keys():
            machine_metrics[queue].update(job_metrics[queue])
        queue_info = machine_metrics['queue_info']
        queue_dict = machine_metrics[queue]
        queue_dict.update(queue_info[queue])
        queue_dict["queue"] = queue
        queue_dict["timestamp"] = machine_metrics['timestamp']
        queue_dict["environment"] = machine_metrics['environment']
        queue_dict["reserved"]['hosts'] = machine_metrics[queue]['claimed']
        queue_dict["available"]['hosts'] = machine_metrics[queue]['unclaimed']
        if queue_dict['available']['hosts'] != 0:
            queue_dict['utilization'] = queue_dict['reserved']['hosts']/queue_dict['available']['hosts']
        queue_dict["type"] = "schedulermetrics2"
        queue_info_array.append(queue_dict)
        c.to_logstashJson(queue_dict)
        del machine_metrics['queue_info'][queue]
        del machine_metrics[queue]
        
    print("Total Machine Information")
    del machine_metrics['queue_info']
    print("Total claimed hosts", machine_metrics['claimed'])
    print("Total available hosts", machine_metrics['unclaimed'])
    print("Total hosts", machine_metrics['total_hosts'])
    print("Total resources", machine_metrics['total_resources'])
    print("{} queue records have been added to Logstash".format(len(queue_info_array)))
