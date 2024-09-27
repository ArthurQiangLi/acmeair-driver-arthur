#!/usr/bin/env python3
#
# Self-Configuring Monitoring Script for Acme Air using Sysdig Monitor
#
# This script continuously monitors the Acme Air application by fetching
# Average Response Time, Maximum Response Time, and Container CPU Utilization
# from Sysdig Monitor. It then analyzes these metrics based on defined
# utility functions and logs the results to a JSON file.

import sys
import json
import time
import datetime
import logging
from sdcclient import SdMonitorClient
from sdcclient import IbmAuthHelper

# ----------------------------
# Configuration Parameters
# ----------------------------

# Sysdig Monitor Configuration
GUID = '3fed93bc-00f4-4651-8ce2-e73ba4b9a918'  # Replace with your GUID
APIKEY = 'mMdgK_7zUpsjHuRmBuQaut8GqecNMqw76XpWMRoQDSxK'  # Replace with your API key
URL = 'https://ca-tor.monitoring.cloud.ibm.com'  # Replace with your Sysdig Monitor URL

# Monitoring Parameters
METRICS = [
    {"id": "application.response.time.average"},  # Replace with actual metric ID
    {"id": "application.response.time.max"},      # Replace with actual metric ID
    {"id": "container.cpu.usage.percent"}         # Replace with actual metric ID
]

START_OFFSET_SECONDS = -600  # Last 10 minutes
END_OFFSET_SECONDS = 0        # Up to now
SAMPLING_INTERVAL_SECONDS = 60  # 1-minute intervals
PAGING = {"from": 0, "to": 100}  # Adjust based on expected number of containers

# Logging Configuration
LOG_FILE = 'monitoring_log.json'
LOG_INTERVAL_SECONDS = 60  # Monitoring loop interval

# Utility Function Weights
WEIGHTS = {
    "average_response_time": 0.4,
    "max_response_time": 0.4,
    "cpu_utilization": 0.2
}

# Quality Requirements Thresholds
THRESHOLDS = {
    "average_response_time": {
        "excellent": 150,
        "acceptable": 300
    },
    "max_response_time": {
        "excellent": 300,
        "acceptable": 600
    },
    "cpu_utilization": {
        "low": 60,
        "high": 80
    }
}



# ----------------------------
# Utility Functions
# ----------------------------

def calculate_utility(value, thresholds, is_cpu=False):
    """
    Calculate the utility score based on the value and defined thresholds.

    Args:
        value (float): The metric value.
        thresholds (dict): Thresholds for utility calculation.
        is_cpu (bool): Flag indicating if the metric is CPU utilization.

    Returns:
        float: Utility score (0, 0.5, or 1).
    """
    if not is_cpu:
        if value <= thresholds["excellent"]:
            return 1.0
        elif thresholds["excellent"] < value <= thresholds["acceptable"]:
            return 0.5
        else:
            return 0.0
    else:
        if value < thresholds["low"]:
            return 1.0
        elif thresholds["low"] <= value <= thresholds["high"]:
            return 0.5
        else:
            return 0.0

def current_timestamp():
    """
    Get the current timestamp in ISO format.

    Returns:
        str: Current timestamp.
    """
    return datetime.datetime.utcnow().isoformat() + 'Z'

# ----------------------------
# Main Monitoring Class
# ----------------------------

class SelfConfiguringMonitor:
    def __init__(self, guid, apikey, url, metrics, log_file):
        self.guid = guid
        self.apikey = apikey
        self.url = url
        self.metrics = metrics
        self.log_file = log_file

        # Initialize Sysdig Monitor Client
        self.ibm_headers = IbmAuthHelper.get_headers(self.url, self.apikey, self.guid)
        self.sdclient = SdMonitorClient(sdc_url=self.url, custom_headers=self.ibm_headers)

        # Setup Logging
        logging.basicConfig(filename=self.log_file,
                            level=logging.INFO,
                            format='%(message)s')

    def fetch_metrics(self):
        """
        Fetch the defined metrics from Sysdig Monitor.

        Returns:
            list: List of metric data.
        """
        try:
            ok, res = self.sdclient.get_data(
                metrics=self.metrics,
                start_ts=START_OFFSET_SECONDS,
                end_ts=END_OFFSET_SECONDS,
                sampling_s=SAMPLING_INTERVAL_SECONDS,
                filter=None,
                paging=PAGING,
                datasource_type='container'  # Adjust if necessary
            )
            if not ok:
                logging.error(f"{current_timestamp()} - Error fetching data: {res}")
                return []
            return res
        except Exception as e:
            logging.error(f"{current_timestamp()} - Exception during data fetch: {str(e)}")
            return []

    def analyze_metrics(self, data):
        """
        Analyze the fetched metrics and calculate utility scores.

        Args:
            data (list): List of metric data.

        Returns:
            dict: Analysis results including utility scores.
        """
        analysis_results = []
        for entry in data:
            # Initialize variables
            avg_response_time = None
            max_response_time = None
            cpu_utilization = None

            # Extract metric values
            for metric in entry.get('metrics', []):
                metric_id = metric.get('id')
                value = metric.get('value', 0)

                if metric_id == "application.response.time.average":
                    avg_response_time = value
                elif metric_id == "application.response.time.max":
                    max_response_time = value
                elif metric_id == "container.cpu.usage.percent":
                    cpu_utilization = value

            # Proceed only if all metrics are available
            if avg_response_time is not None and max_response_time is not None and cpu_utilization is not None:
                # Calculate individual utilities
                u_avg_response = calculate_utility(avg_response_time, THRESHOLDS["average_response_time"])
                u_max_response = calculate_utility(max_response_time, THRESHOLDS["max_response_time"])
                u_cpu = calculate_utility(cpu_utilization, THRESHOLDS["cpu_utilization"], is_cpu=True)

                # Calculate total utility
                total_utility = (
                    WEIGHTS["average_response_time"] * u_avg_response +
                    WEIGHTS["max_response_time"] * u_max_response +
                    WEIGHTS["cpu_utilization"] * u_cpu
                )

                # Determine overall status
                if total_utility == 1.0:
                    status = "Optimal"
                elif 0.5 <= total_utility < 1.0:
                    status = "Acceptable"
                else:
                    status = "Critical"

                # Compile analysis result
                result = {
                    "timestamp": current_timestamp(),
                    "container": entry.get('container.name', 'unknown'),
                    "average_response_time_ms": avg_response_time,
                    "max_response_time_ms": max_response_time,
                    "cpu_utilization_percent": cpu_utilization,
                    "utility_scores": {
                        "average_response_time": u_avg_response,
                        "max_response_time": u_max_response,
                        "cpu_utilization": u_cpu
                    },
                    "total_utility": total_utility,
                    "status": status
                }

                analysis_results.append(result)

        return analysis_results

    def log_results(self, analysis_results):
        """
        Log the analysis results to a JSON file.

        Args:
            analysis_results (list): List of analysis result dictionaries.
        """
        for result in analysis_results:
            logging.info(json.dumps(result))

    def run(self):
        """
        Run the monitoring and analysis loop indefinitely.
        """
        while True:
            data = self.fetch_metrics()
            if data:
                analysis_results = self.analyze_metrics(data)
                if analysis_results:
                    self.log_results(analysis_results)
                    # Optional: Print to console for real-time monitoring
                    for res in analysis_results:
                        print(json.dumps(res, indent=4))
            else:
                print(f"{current_timestamp()} - No data fetched.")

            # Sleep until the next interval
            time.sleep(LOG_INTERVAL_SECONDS)

# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    monitor = SelfConfiguringMonitor(
        guid=GUID,
        apikey=APIKEY,
        url=URL,
        metrics=METRICS,
        log_file=LOG_FILE
    )
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"{current_timestamp()} - Unexpected error: {str(e)}")
        sys.exit(1)

# End of file
