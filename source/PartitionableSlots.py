import math


class PartitionableSlot():
    def __init__(self, classad):
        self.machine_name = classad['machine']
        self.clientgroup = classad['clientgroup']
        self.totalslotcpus = classad['totalslotcpus']
        self.totaldisk = classad['totaldisk']
        self.detectedcpus = classad['detectedcpus']
        self.cpubusytime = classad['cpubusytime']
        self.totalmemory = classad['totalmemory']
        self.childmemory_reserved = sum(classad.get('childmemory'))  # TODO SUM
        self.childcpus_reserved = sum(classad.get('childcpus'))
        self.childdisk_reserved = sum(classad.get('childdisk'))
        self.cpu_used = math.ceil(self.childcpus_reserved / self.totalslotcpus) * 100
        self.memory_used = math.ceil(self.childmemory_reserved / self.totalmemory) * 100
        self.disk_used = math.ceil(self.childdisk_reserved / self.totaldisk) * 100
        self.claimed = False
        self.cpu_actual = 0
        self.memory_actual = 0
        self.disk_actual = 0

    def claim(self):
        self.claimed = True

    def calculate_actual_usage(self, input_dynamic_slots):
        memory_usage_peak = 0
        disk_usage_peak = 0
        average_cpu_usage = 0

        for slot in input_dynamic_slots:
            if input_dynamic_slots[slot].parent_slot == self.machine_name:
                memory_usage_peak += input_dynamic_slots[slot].memory_usage_peak
                disk_usage_peak += input_dynamic_slots[slot].disk_usage_peak
                average_cpu_usage += input_dynamic_slots[slot].average_cpu_usage
        self.cpu_actual = average_cpu_usage
        self.memory_actual = memory_usage_peak
        self.disk_actual = disk_usage_peak

    def __repr__(self):
        return str(vars(self))
    
