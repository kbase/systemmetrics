from get_system_reports import get_system_report
import time
import sys
import datetime
print("############################################")
print("System Metrics Upload (UTC): " + str(datetime.datetime.utcnow()))
start_time = time.time()

if len(sys.argv) == 1:
    get_system_report()
    print("Uploading system metrics to logstash stats took ",
          time.time() - start_time, " seconds to run")

else:
    print("Invalid number of arguments given")
