

class DynamicSlot():
    def __init__(self, classad):
        self.parent_slot = classad['machine']
        self.totalmemory = classad['totalmemory']
        if 'residentsetsize' not in classad:
            print("Couldn't find memory for", classad['machine'])
        self.memory_usage_peak = classad.get('residentsetsize', 0)
        self.disk_usage_peak = classad['diskusage']
        self.average_cpu_usage = classad['cpususage']
        self.classad = classad
