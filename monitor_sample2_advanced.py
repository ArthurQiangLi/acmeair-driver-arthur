#!/usr/bin/env python
#
# This script shows the basics of getting data out of Sysdig Monitor by creating a
# very simple request that has no filter and no segmentation.
#
# The request queries for the average CPU across all of the instrumented hosts for
# the last 10 minutes, with 1 minute data granularity
#

import sys, json
from sdcclient import SdMonitorClient
from sdcclient import IbmAuthHelper

# config values based on instructions from: https://cloud.ibm.com/apidocs/monitor#authentication-when-using-python 
GUID = '3fed93bc-00f4-4651-8ce2-e73ba4b9a918'
APIKEY = 'mMdgK_7zUpsjHuRmBuQaut8GqecNMqw76XpWMRoQDSxK'
URL = 'https://ca-tor.monitoring.cloud.ibm.com'

ibm_headers = IbmAuthHelper.get_headers(URL, APIKEY, GUID)
sdclient = SdMonitorClient(sdc_url=URL, custom_headers=ibm_headers)

#
# List of metrics to export. Imagine a SQL data table, with key columns and value columns
# You just need to specify the ID for keys, and ID with aggregation for values.
#
metrics = [
    # The first metric we request is the container name. This is a segmentation
    # metric, and you can tell by the fact that we don't specify any aggregation
    # criteria. This entry tells Sysdig Monitor that we want to see the CPU
    # utilization for each container separately.
    {"id": "container.name"},
    # The second metric we request is the CPU. We aggregate it as an average.
    {"id": "cpu.used.percent",
     "aggregations": {
         "time": "avg",
         "group": "avg"
     }
     }
]

#
# Data filter or None if you want to see "everything"
#
filter = None

#
# Time window:
#   - for "from A to B": start is equal to A, end is equal to B (expressed in seconds)
#   - for "last X seconds": start is equal to -X, end is equal to 0
#
start = -600
end = 0

#
# Sampling time:
#   - for time series: sampling is equal to the "width" of each data point (expressed in seconds)
#   - for aggregated data (similar to bar charts, pie charts, tables, etc.): sampling is equal to 0
#
sampling = 60

paging = {"from": 0, "to": 4}



#
# Load data / fire the query
# ok, res = sdclient.get_data(metrics, start, end, sampling, filter=filter)


#
# Fire the query.
#
ok, res = sdclient.get_data(metrics=metrics,  # List of metrics to query
                            start_ts=-600,  # Start of query span is 600 seconds ago
                            end_ts=0,  # End the query span now
                            sampling_s=60,  # 1 data point per minute
                            filter=filter,  # The filter specifying the target host
                            paging=paging,  # Paging to limit to just the 5 most busy
                            datasource_type='container')  # The source for our metrics is the container

#
# Show the result!
#
print((json.dumps(res, sort_keys=True, indent=4)))
if not ok:
    sys.exit(1)


# End of file