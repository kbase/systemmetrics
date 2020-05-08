#!/bin/bash

python DynamicSlots.py

python PartitionableSlots.py

python job_info.py

python average_times_queues.py

python createslots.py

python generate_slot_report.py

python calculate_memory_resources_queues.py

python calculate_total_memory_resources.py

python calculate_total_memory_queue.py

python get_report_machines.py

python get_report_jobs.py

python get_system_metrics.py

python upload_system_metrics.py $*
