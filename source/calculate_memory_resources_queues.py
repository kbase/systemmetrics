

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
