from math import floor


def calculate_total_cpus_memory_disk(partionable_slots):
    """This function calculates the memory resources/allocated - available, reserved, actual - for a given machine.
       The memory resources are formatted to a dictionary that is returned."""

    # Initiate memory variables
    disk_kb = 0
    memory_mb = 0
    cpus = 0

    disk_kb_reserved = 0
    memory_mb_reserved = 0
    cpus_reserved = 0

    memory_actual = 0
    disk_actual = 0

    for slot in partionable_slots:
        p_slot = partionable_slots[slot]
        # Available
        cpus += p_slot.totalslotcpus
        memory_mb += p_slot.totalmemory
        disk_kb += p_slot.totaldisk
        # Reserved
        cpus_reserved += p_slot.childcpus_reserved
        memory_mb_reserved += p_slot.childmemory_reserved
        disk_kb_reserved += p_slot.childdisk_reserved
        # Actual Usage (actual usage cpu is off as of March 2020)
        # cpu_actual += p_slot.cpu_actual
        memory_actual += p_slot.memory_actual
        disk_actual += p_slot.disk_actual

    # Available Usage
    disk_gb_available = floor(disk_kb / 1024 / 1024)
    memory_gb_available = floor(memory_mb / 1024)

    # Reserved Usage
    disk_gb_reserved = floor(disk_kb_reserved / 1024 / 1024)
    memory_gb_reserved = floor(memory_mb_reserved / 1024)

    # TODO FIX THIS Actual Usage cpu?
    disk_gb_actual = floor(disk_actual / 1024 / 1024)
    memory_gb_actual = floor(memory_actual / 1024)

    # Format Usage Dictionaries
    available = {'disk_gb': disk_gb_available, 'memory_gb': memory_gb_available, 'cpus': cpus}
    reserved = {'disk_gb': disk_gb_reserved, 'memory_gb': memory_gb_reserved, 'cpus': cpus_reserved}
    actual = {'disk_gb': disk_gb_actual, 'memory_gb': memory_gb_actual}
    # Dictionary of memory resources
    resources = {'available': available,
                 'reserved': reserved,
                 'actual': actual}

    return resources
