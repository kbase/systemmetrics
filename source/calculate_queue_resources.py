import time
from math import floor
from statistics import mean


def average_times(queue_dict):
    """average_times is a helper function for get_job_info that takes an array of run times and queue times for each job run in a queue
    and calculates the mean of the array. The function appends the mean as a value into the queue info dictionary in both it's original unit - seconds - and in hours. Returns the queue dictionaries with the appended mean"""
    for queue in queue_dict.keys():
        # Collect run_time and q_time arrays
        queue_time_array = queue_dict[queue]["average_q_time_hr"]
        run_time_array = queue_dict[queue]["average_run_time_hr"]
        # If only one element is present in the array just take that element
        if len(queue_time_array) == 1 and len(run_time_array) == 1:
            queue_time_ave = queue_time_array[0]
            run_time_ave = run_time_array[0]
        # Else find the mean
        else:
            queue_time_ave = mean(queue_time_array)
            run_time_ave = mean(run_time_array)
        # Convert mean to hours from seconds
        average_qtime_hours = floor(queue_time_ave // 3600)
        average_runtime_hours = floor(run_time_ave // 3600)
        # Add run time and q time values in seconds and hours to dictionary
        queue_dict[queue]["average_q_time_sec"] = floor(queue_time_ave)
        queue_dict[queue]["average_run_time_sec"] = floor(run_time_ave)
        queue_dict[queue]["average_run_time_hr"] = average_runtime_hours
        queue_dict[queue]["average_q_time_hr"] = average_qtime_hours

    return queue_dict


def get_job_info(jobs):
    """get_jobs_info function is the main function to format the job portion of each queue dictionary for system metrics. It iterates through jobs in condor collects all the job information under the 'classad' key and checks which queue its looking at. For each queue it makes a queue_info dictionary that consists of the average run time and average q-time for jobs in the q (calculated by the helper function above) and counts how many jobs running jobs or queued jobs are currently in the queue. Returns a ultimate queue dictionary containing each queue seen as a queue to its sub job info dictionary."""
    queue_dict = {}
    # Interate through jobs
    for job in jobs:
        # All job info for KBase jobs in Condor is under 'classad'
        job = job['classad']
        # What kb_clientgroup or queue do we have?/Grab queue and the status of the job
        queue = job["kb_clientgroup"]
        job_type = job["jobstatus"]
        # If queue type (kb_uploads, bigmem, etc.) has not been seen yet and the job status is either running (2) or idle/queued (1) make a queue dictionary
        if queue not in queue_dict.keys():
            if job_type == 2 or job_type == 1:
                queue_dict[queue] = {'total_in_queue': 0, "average_q_time_hr": [],
                                     'total_running': 0, "average_run_time_hr": [],
                                     "average_run_time_sec": None, "average_q_time_sec": None}
            else:
                continue
        # A job type of running means the job contains information about the current run time and the q time in seconds
        if job_type == 2:
            # Get needed values
            q_date = job['qdate']
            start_date = job["jobstartdate"]
            run_array = queue_dict[queue]["average_run_time_hr"]
            queue_array = queue_dict[queue]["average_q_time_hr"]
            # Get times
            epoch_time_now = int(time.time())
            # Current run time for a job is when the job started subtracted the current time on the system when checked
            run_time = epoch_time_now - start_date
            # Q time is when the job started minus when the job was first queued
            queue_time = start_date - q_date
            queue_array.append(queue_time)
            run_array.append(run_time)
            queue_dict[queue]['total_running'] += 1
        # A job of type 'idle' means the job has not started running yet
        elif job_type == 1:
            q_date = job['qdate']
            queue_array = queue_dict[queue]["average_q_time_hr"]
            epoch_time_now = int(time.time())
            # Thus, the current amount of time this job has spent in the queue is the the current time minus the time it was queued
            queue_time = epoch_time_now - q_date
            queue_array.append(queue_time)
            queue_dict[queue]['total_in_queue'] += 1
    # Send final queue dict to helper function to calculate the run time and q_time means
    formatted_dict = average_times(queue_dict)

    return formatted_dict


def calculate_queues(partionable_slots, queue_info):
    """Calculate_queues is similar to get_job_info but in terms of memory/cpu/disk usage per queue not job stats. Only slots that are partionable can run jobs and thus have a kb_clientgroup/queue. This function iterates through partitionable slots and for each clientgroup/queue it sees it collection info on it's system usage."""

    data_storage_types = ['cpus', 'memory_mb', 'disk_kb',
                          'disk_kb_reserved', 'memory_mb_reserved', 'cpus_reserved',
                          'cpu_actual', 'memory_actual', 'disk_actual']

    for slot in partionable_slots:
        machine = partionable_slots[slot]
        queue = machine.clientgroup
        # If queue has already been seen, simply the sum the system usage info for this slot.
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
            # If queue hasn't been seen create a dictionary with all the data storage types
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
    """Calculate_queues_total primarily relies on a helper function 'calculate queues' to calculate the total usage (disk/cpu/memory) per queue. Once the total system usage has been calculated it converts the units from Kb to Gb"""
    queue_info = calculate_queues(partionable_slots, queue_dict)
    for queue, memory_dict in queue_info.items():
        # Available Usage
        disk_gb_available = floor(memory_dict['disk_kb'] / 1024 / 1024)
        memory_gb_available = floor(memory_dict['memory_mb'] / 1024)

        # Reserved Usage
        disk_gb_reserved = floor(memory_dict['disk_kb_reserved'] / 1024 / 1024)
        memory_gb_reserved = floor(memory_dict['memory_mb_reserved'] / 1024)

        # Actual Usage
        disk_gb_actual = floor(memory_dict['disk_actual'] / 1024 / 1024)
        memory_gb_actual = floor(memory_dict['memory_actual'] / 1024)

        local_dict_temp = queue_info[queue]
        # Only cpu availble and reserved are accurately reporting as of March 2020
        available = {'disk_gb': disk_gb_available, 'memory_gb': memory_gb_available, 'cpus': local_dict_temp['cpus']}
        reserved = {'disk_gb': disk_gb_reserved, 'memory_gb': memory_gb_reserved, 'cpus': local_dict_temp['cpus_reserved']}
        actual = {'disk_gb': disk_gb_actual, 'memory_gb': memory_gb_actual}
        # Now that the system usage has been calculated for this queue re-initiate the dictionary with the sub dictionaries and return
        queue_info[queue] = {}
        queue_info[queue]['available'] = available
        queue_info[queue]['reserved'] = reserved
        queue_info[queue]['actual'] = actual
    return queue_info
