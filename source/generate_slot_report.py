from collections import Counter


def generate_cg_report(partionable_slots):
    print("Creating all machines report")

    report = {'claimed': 0, 'unclaimed': 0}
    cg_count = Counter()

    for slot in partionable_slots:
        machine = partionable_slots[slot]
        queue = machine.clientgroup
        cg_count[machine.clientgroup] += 1
        if queue not in report.keys():
            report[queue] = {'claimed': 0, 'unclaimed': 0}
        if(machine.claimed):
            report['claimed'] += 1
            report[queue]["claimed"] += 1
        else:
            report['unclaimed'] += 1
            report[queue]["unclaimed"] += 1

    return(report)
