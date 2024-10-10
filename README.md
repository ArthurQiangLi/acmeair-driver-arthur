# runJMeter2.sh usage (2024/09/26):

```
./runJmeter2.sh low
```

It will return :
```
Workload Level: high
HOST=acmeair7.mycluster-ca-tor-2-bx2-4x-04e8c71ff333c8969bc4cbc5a77a70f6-0000.ca-tor.containers.appdomain.cloud
PORT=80
THREAD=50
USER=2000
DURATION=60
RAMP=20
DELAY=5
DELAY=5
Cleared bookings in 0.008 secondsLoaded flights for 5 days in 16.745 secondsLoaded 10001 customers in 0.386 seconds./runJmeter2.sh: line 76: 1: command not found
JMeter test completed. Check jmeter_output.log for details.
```


# login info
API Key              mMdgK_7zUpsjHuRmBuQaut8GqecNMqw76XpWMRoQDSxK

# Log in with this token
```
API Key              mMdgK_7zUpsjHuRmBuQaut8GqecNMqw76XpWMRoQDSxK

# Log in with this token
```
oc login --token=sha256~kqKXQZ2nUKsxn9kt_s1qtfCUmKdnQ_Z_0MWrvkInZnI --server=https://c104-e.ca-tor.containers.cloud.ibm.com:30227
oc login --token=sha256~9PGcSrOCGeJq_24iHf7OVFam_cAK6A8bNXgBv7bYts8 --server=https://c104-e.ca-tor.containers.cloud.ibm.com:30227


```

# Assignment2
## Get API Version Compatibility
```
curl -k -v \
-X GET \
-H "Authorization: Bearer sha256~gsDM7K2dv17_jLvCSM9UMAZ9G4eccInr4OJR53gQZrY" \
-H "Accept: application/json" \
https://c104-e.ca-tor.containers.cloud.ibm.com:30227/apis

```

## Get deployment info
```
curl -k -v \
-X GET \
-H "Authorization: Bearer sha256~gsDM7K2dv17_jLvCSM9UMAZ9G4eccInr4OJR53gQZrY" \
-H "Accept: application/json" \
https://c104-e.ca-tor.containers.cloud.ibm.com:30227/apis/apps/v1/namespaces/group-7/deployments/acmeair-mainservice/scale

```
If this works, it confirms that the `acmeair-mainservice` is a Kubernetes Deployment rather than an OpenShift DeploymentConfig.

## Set scale number
```
curl -k -v \
-X PUT \
-H "Authorization: Bearer sha256~gsDM7K2dv17_jLvCSM9UMAZ9G4eccInr4OJR53gQZrY" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-d '{
      "apiVersion": "autoscaling/v1",
      "kind": "Scale",
      "metadata": {
        "name": "acmeair-mainservice",
        "namespace": "group-7"
      },
      "spec": {
        "replicas": 3
      }
    }' \
https://c104-e.ca-tor.containers.cloud.ibm.com:30227/apis/apps/v1/namespaces/group-7/deployments/acmeair-mainservice/scale

```

returns:
```
{
  "kind": "Scale",
  "kind": "Scale",
  "apiVersion": "autoscaling/v1",
  "apiVersion": "autoscaling/v1",
  "metadata": {
    "name": "acmeair-mainservice",
    "namespace": "group-7",
    "uid": "92d126bc-5b2c-400a-ae1b-7fd07a537eef",
    "resourceVersion": "38830649",
    "creationTimestamp": "2024-10-09T22:57:18Z"
  },
  "spec": {
    "replicas": 3
  },
  "status": {
    "replicas": 2,
    "selector": "name=acmeair-main-deployment"
  }
}* Connection #0 to host c104-e.ca-tor.containers.cloud.ibm.com left intact
```
