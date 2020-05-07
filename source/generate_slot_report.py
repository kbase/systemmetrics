from collections import defaultdict, Counter


def generate_cg_report(partionable_slots):
    print("Creating all machines report")
    report = defaultdict(list)
    cg_count = Counter()
    for slot in partionable_slots:
        machine = partionable_slots[slot]
        cg_count[machine.clientgroup] += 1
        if(machine.claimed):
            report['claimed'].append(machine)
            report[machine.clientgroup+"_claimed"].append(machine)
        else:
            report['unclaimed'].append(machine)
            report[machine.clientgroup+"_unclaimed"].append(machine)
    print("Total claimed", len(report['claimed']))
    for c in report['claimed']:
        print(c.machine_name,)
    print("Total unclaimed", len((report['unclaimed'])))
    print("Creating available clientgroup machines report")
    print(cg_count)
    del(report['claimed'])
    del(report['unclaimed'])
    for key in report.keys():
        print(key, len(report[key]))
