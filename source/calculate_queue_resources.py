import time
from math import floor
from statistics import mean


def average_times(queue_dict):
    for queue in queue_dict.keys():
        queue_time_array = queue_dict[queue]["average_q_time_hr"]
        run_time_array = queue_dict[queue]["average_run_time_hr"]
        if len(queue_time_array) == 1 and len(run_time_array) == 1:
            queue_time_ave = queue_time_array[0]
            run_time_ave = run_time_array[0]
        else:
            queue_time_ave = mean(queue_time_array)
            run_time_ave = mean(run_time_array)

        if queue == "kb_upload":
            del queue_dict[queue]["average_q_time_hr"]
            del queue_dict[queue]["average_run_time_hr"]
            average_qtime_sec = floor(queue_time_ave)
            average_runtime_sec = floor(run_time_ave)
            queue_dict[queue]["average_q_time_sec"] = average_qtime_sec
            queue_dict[queue]["average_run_time_sec"] = average_runtime_sec

        else:
            average_qtime_hours = floor(queue_time_ave / 3600)
            average_runtime_hours = floor(run_time_ave / 3600)
            queue_dict[queue]["average_q_time_hr"] = average_qtime_hours
            queue_dict[queue]["average_run_time_hr"] = average_runtime_hours

    return queue_dict

def get_job_info(jobs):
    
    queue_dict = {}
    queue_times = []
    run_times = []
    for job in jobs:
        job = job['classad']
        queue_requirement = job["requirements"]
        if "concierge" in queue_requirement:
            queue = queue_requirement.split(",")[0].split("(")[-1].strip('""')
        else:
            queue = queue_requirement.split("CLIENTGROUP")[1].split("&&")[0].strip("[' ==)/").strip('"')
        job_type = job["jobstatus"]
        if queue not in queue_dict.keys():
            if job_type == 2 or job_type == 1:
                queue_dict[queue] = {'total_in_queue': 0, "average_q_time_hr": [],
                                     'total_running': 0, "average_run_time_hr": []}
            else:
                continue

        if job_type == 2:
            # Get needed values
            q_date = job['qdate']
            start_date = job["jobstartdate"]
            run_array = queue_dict[queue]["average_run_time_hr"]
            queue_array = queue_dict[queue]["average_q_time_hr"]
            # Get times
            epoch_time_now = int(time.time())
            run_time = epoch_time_now - start_date
            queue_time = start_date - q_date
            queue_array.append(queue_time)
            run_array.append(run_time)
            queue_dict[queue]['total_running'] += 1
        elif job_type == 1:
            q_date = job['qdate']
            queue_array = queue_dict[queue]["average_q_time_hr"]
            epoch_time_now = int(time.time())
            queue_time = epoch_time_now - q_date
            queue_array.append(queue_time)
            queue_dict[queue]['total_in_queue'] += 1
   
    formatted_dict = average_times(queue_dict)
                
    return formatted_dict


def calculate_queues(partionable_slots, queue_info):

    data_storage_types = ['cpus', 'memory_mb', 'disk_kb',
                          'disk_kb_reserved', 'memory_mb_reserved', 'cpus_reserved',
                          'cpu_actual', 'memory_actual', 'disk_actual']

    for slot in partionable_slots:
        machine = partionable_slots[slot]
        queue = machine.clientgroup
        if queue in queue_info.keys():
            queue_memory = queue_info[queue]
            # Available
            queue_memory['cpus'] += machine.totalslotcpus
            queue_memory['memory_mb'] += machine.totalmemory
            queue_memory['disk_kb'] += machine.totaldisk
            # Reserved (Are these the right attributes?)
            queue_memory['cpus_reserved'] += machine.childcpus_reserved
            queue_memory['memory_mb_reserved'] += machine.childmemory_reserved
            queue_memory['disk_kb_reserved'] += machine.childdisk_reserved
            # Actual Usage
            queue_memory['cpu_actual'] += machine.cpu_actual
            queue_memory['memory_actual'] += machine.memory_actual
            queue_memory['disk_actual'] += machine.disk_actual
            queue_info[machine.clientgroup] = queue_memory
        else:
            # Initalize dictionary objects
            queue_memory = dict.fromkeys(data_storage_types, 0)
            # Available
            queue_memory['cpus'] = machine.totalslotcpus
            queue_memory['memory_mb'] = machine.totalmemory
            queue_memory['disk_kb'] = machine.totaldisk
            # Reserved
            queue_memory['cpus_reserved'] = machine.childcpus_reserved
            queue_memory['memory_mb_reserved'] = machine.childmemory_reserved
            queue_memory['disk_kb_reserved'] = machine.childdisk_reserved
            # Actual Usage
            queue_memory['cpu_actual'] = machine.cpu_actual
            queue_memory['memory_actual'] = machine.memory_actual
            queue_memory['disk_actual'] = machine.disk_actual
            queue_info[machine.clientgroup] = queue_memory
    return queue_info

def calculate_queues_total(partionable_slots, queue_dict):
    queue_info = calculate_queues(partionable_slots, queue_dict)
    for queue, memory_dict in queue_info.items():
        # Available Usage
        disk_gb_available = floor(memory_dict['disk_kb'] / 1024 / 1024)
        memory_gb_available = floor(memory_dict['memory_mb'] / 1024)

        # TODO FIX THIS Not sure actual units, or ??
        disk_gb_reserved = floor(memory_dict['disk_kb_reserved'] / 1024 / 1024)
        memory_gb_reserved = floor(memory_dict['memory_mb_reserved'] / 1024)

        # TODO FIX THIS Actual Usage
        disk_gb_actual = floor(memory_dict['disk_actual'] / 1024 / 1024)
        memory_gb_actual = floor(memory_dict['memory_actual'] / 1024)

        local_dict = queue_info[queue]
        available = {'disk_gb': disk_gb_available, 'memory_gb': memory_gb_available, 'cpus': local_dict['cpus']}
        reserved = {'disk_gb': disk_gb_reserved, 'memory_gb': memory_gb_reserved, 'cpus': local_dict['cpus_reserved']}
        actual = {'disk_gb': disk_gb_actual, 'memory_gb': memory_gb_actual}
        queue_info[queue] = {}
        queue_info[queue]['available'] = available
        queue_info[queue]['reserved'] = reserved
        queue_info[queue]['actual'] = actual
    return queue_info
