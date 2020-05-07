from PartitionableSlots import PartitionableSlot
from DynamicSlots import DynamicSlot


def create_partionable_slots(claimed, unclaimed):
    ps = {}
    for item in unclaimed:
        classad = item['classad']
        slottype = classad['slottype']
        if slottype == 'Partitionable':
            machine_name = classad['machine']
            ps[machine_name] = PartitionableSlot(classad=classad)

    for item in claimed:
        classad = item['classad']
        slottype = classad['slottype']
        if slottype == 'Dynamic':
            machine_name = classad['machine']
            ps[machine_name].claim()
    return ps


def create_dynamic_slots(claimed):
    ds = {}
    for item in claimed:
        classad = item['classad']
        slottype = classad['slottype']
        if slottype == 'Dynamic':
            machine_name = classad['machine']
            ds[machine_name] = DynamicSlot(classad=classad)
    return ds
