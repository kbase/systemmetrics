# KBase System Metrics

This repository contains code for gathering and uploading KBase system metrics from Condor API such as memory, disk and cpu usage, as well as job and queue information.

## Getting Started
Before being able to run this docker container a ".env" file needs to be made. 
It should be called .env and should contain the following:

* USER_TOKEN=<TOKEN>
* SERVICE_WIZARD_URL=<URL>
* ELASTICSEARCH_HOST=<URL>
* CONDOR_JOB_URL=<URL>
* CONDOR_MACHINE_URL=<URL>

Please ask a fellow developer for the correct url paths and alter your .env 
file accordingly. 

The script in hooks/build is used to build a docker image named "kbase/systemmetrics" 
from the current contents of the repo. You can simply run it by:
```sh
$ IMAGE_NAME=kbase/systemmetrics hooks/build
```

Once it's built, one can run the source directory by the following command:
```sh
$ docker-compose run --rm SystemMetrics
```

Or one can run the error log cron job by:
```sh
$ docker-compose run --rm SystemMetrics ../bin/cron_shell.sh
```

## Testing
To test the output of the main script (get_system_report) without uploading logs to
logstash, one should comment out the following export statement:
```sh
c.to_logstashJson(machine_metrics)
```
and one should return "machine_metrics"


# Guide to understanding job states

### Execution Engine Job states are available in the EE2 Repo 
* https://github.com/kbase/execution_engine2/blob/develop/lib/execution_engine2/db/models/models.py

Currently they are
* created 
* estimating
* queued 
* running
* finished # Successful run legacy code
* completed # Successful run in ee2
* error  # Failed run # Something went wrong and job failed # Possible Reasons are (ErrorCodes)
* terminated = # Canceled by user # Canceled by user, admin, or script # Possible Reasons are (TerminatedCodes)
    
### HTCondor JobStatus
* See https://htcondor.readthedocs.io/en/latest/classad-attributes/job-classad-attributes.html

Integer which indicates the current status of the job.
Value 	Idle
1 	Idle
2 	Running
3 	Removing
4 	Completed
5 	Held
6 	Transferring Output
7 	Suspended

These are not a one to one mapping, and each tell you different information. 
If a job is IDLE, it can still run in condor
If a job is RUNNING, it is currently running in condor
If a job is HELD, it will probably never run again, depending on the HOLD REASON (See HTCondor Manual)
If the hold reason is `16 	Input files are being spooled` then the job is about to enter the idle state, otherwise, it will never run again.

  
