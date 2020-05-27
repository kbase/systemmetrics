import time
from average_times_queues import average_times


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
            q_date_iso = datetime.datetime.utcfromtimestamp(q_date).isoformat()
            queue_array = queue_dict[queue]["average_q_time_hr"]
            epoch_time_now = int(time.time())
            queue_time = epoch_time_now - q_date
            queue_array.append(queue_time)
            q_dates.append(q_date_iso)
            queue_dict[queue]['total_in_queue'] += 1
   
    formatted_dict = average_times(queue_dict)
                
    return formatted_dict
