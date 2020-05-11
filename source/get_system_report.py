from get_report_machines import get_report_machines
from get_report_jobs import get_report_jobs
import client as c

def get_system_report():
    machine_metrics = get_report_machines()
    job_metrics = get_report_jobs()
    machine_metrics.update(job_metrics)
    machine_metrics["type"] = "schedulermetrics"
    c.to_logstashJson(machine_metrics)
    print("{} system metrics added to Logstash.".format(len(machine_metrics)))
