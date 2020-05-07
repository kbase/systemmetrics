from calculate_memory_resources_queues import calculate_queues


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
