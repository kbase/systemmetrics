from math import floor
from statistics import mean


def average_times(queue_dict):
    for queue in queue_dict.keys():
        queue_time_array = queue_dict[queue]["queue_info"]["average_q_time_hr"]
        run_time_array = queue_dict[queue]["run_info"]["average_run_time_hr"]
        if len(queue_time_array) == 1 and len(run_time_array) == 1:
            queue_time_ave = queue_time_array[0]
            run_time_ave = run_time_array[0]
        else:
            queue_time_ave = mean(queue_time_array)
            run_time_ave = mean(run_time_array)

        if queue == "kb_upload":
            del queue_dict[queue]["queue_info"]["average_q_time_hr"]
            del queue_dict[queue]["run_info"]["average_run_time_hr"]
            average_qtime_sec = floor(queue_time_ave)
            average_runtime_sec = floor(run_time_ave)
            queue_dict[queue]["queue_info"]["average_q_time_sec"] = average_qtime_sec
            queue_dict[queue]["run_info"]["average_run_time_sec"] = average_runtime_sec

        else:
            average_qtime_hours = floor(queue_time_ave / 3600)
            average_runtime_hours = floor(run_time_ave / 3600)
            queue_dict[queue]["queue_info"]["average_q_time_hr"] = average_qtime_hours
            queue_dict[queue]["run_info"]["average_run_time_hr"] = average_runtime_hours

    return queue_dict
