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