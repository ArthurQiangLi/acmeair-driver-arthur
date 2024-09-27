#!/bin/bash

# Set group number
GROUP=7
if [ "$GROUP" -eq 0 ]; then
    echo "Error: please update your group number!"
    exit 1
fi

# Get the Acme Air host
HOST=$(oc get route acmeair-main-route -n group-${GROUP} --template='{{ .spec.host }}')
PORT=80

# Accept workload level as an argument
WORKLOAD=${1:-medium}

# Set parameters based on workload level
case "$WORKLOAD" in
    low)
        THREAD=10
        USER=500
        DURATION=60
        RAMP=10
        DELAY=10
        ;;
    medium)
        THREAD=20
        USER=1000
        DURATION=60
        RAMP=10
        DELAY=10
        ;;
    high)
        THREAD=50
        USER=2000
        DURATION=60
        RAMP=10
        DELAY=10
        ;;
    *)
        echo "Error: Invalid workload level. Please choose from: low, medium, high."
        exit 1
        ;;
esac

echo "Workload Level: $WORKLOAD"
echo "HOST=${HOST}"
echo "PORT=${PORT}"
echo "THREAD=${THREAD}"
echo "USER=${USER}"
echo "DURATION=${DURATION}"
echo "RAMP=${RAMP}"
echo "DELAY=${DELAY}"

# Check if host is reachable
# if ! curl --output /dev/null --silent --head --fail "http://${HOST}"; then
#     echo "Error: Cannot reach host ${HOST}"
#     exit 1
# fi

# Load initial data for the services
curl http://${HOST}/booking/loader/load || { echo "Error loading booking data"; exit 1; }
curl http://${HOST}/flight/loader/load || { echo "Error loading flight data"; exit 1; }
curl http://${HOST}/customer/loader/load?numCustomers=10001 || { echo "Error loading customer data"; exit 1; }

# Run JMeter with the specified parameters
jmeter -n -t acmeair-jmeter/scripts/AcmeAir-microservices-mpJwt.jmx \
 -DusePureIDs=true \
 -JHOST=${HOST} \
 -JPORT=${PORT} \
 -JTHREAD=${THREAD} \
 -JUSER=${USER} \
 -JDURATION=${DURATION} \
 -JRAMP=${RAMP} \
 -JDELAY=${DELAY} > jmeter_output.log 2>&1

echo 
echo "#### JMeter test completed. Check jmeter_output.log for details."
