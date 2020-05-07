import json
import requests
import datetime
import os
from createslots import create_dynamic_slots
from createslots import create_partionable_slots
from generate_slot_report import generate_cg_report
from calculate_total_memory_resources import calculate_total_cpus_memory_disk
from calculate_total_memory_queue import calculate_queues_total


def get_report_machines():
    now = datetime.datetime.now().isoformat()
    # Get machines
    url = "https://appdev.kbase.us/services/condor-rest-api/v1/grouped_status/state?query=startd"
    response = requests.get(url, headers={'Authorization': os.environ['KB_AUTH_TOKEN']})
    json_data = json.loads(response.text)
    print("Repsonse status code is", response.status_code)

    # Account for slots on machines
    unclaimed = json_data.get('Unclaimed')
    claimed = json_data.get('Claimed')

    partionable_slots = create_partionable_slots(claimed=claimed, unclaimed=unclaimed)
    print("Partionable slots found:", len(partionable_slots))

    dynamic_slots = create_dynamic_slots(claimed=claimed)
    print("Dynamic Slots:", len(dynamic_slots))

    # queue = create_queue(njs)
    # print("Number of jobs in NSJ: {}".format(len(dynamic_slots)))

    print("Creating actual memory/cpu/disk usages, rather than reserved")
    for slot in partionable_slots:
        partionable_slots[slot].calculate_actual_usage(input_dynamic_slots=dynamic_slots)

    generate_cg_report(partionable_slots)

    total_hosts = len(partionable_slots)
    total_resources = calculate_total_cpus_memory_disk(partionable_slots)
    queue_info = {}
    queue_info = calculate_queues_total(partionable_slots, queue_info)
    memory_metrics_dict = {'timestamp': now,
                           'environment': url,
                           'total_hosts': total_hosts,
                           'total_resources': total_resources,
                           'queue_info': queue_info}

    return memory_metrics_dict

        
