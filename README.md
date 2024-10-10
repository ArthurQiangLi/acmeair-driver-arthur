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



## Error info
```
[Planning] Total utility 0.80 is sufficient. No action required.
Traceback (most recent call last):
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connection.py", line 196, in _new_conn
    sock = connection.create_connection(
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\util\connection.py", line 60, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\socket.py", line 955, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno 11001] getaddrinfo failed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connectionpool.py", line 789, in urlopen
    response = self._make_request(
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connectionpool.py", line 490, in _make_request
    raise new_e
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connectionpool.py", line 466, in _make_request
    self._validate_conn(conn)
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connectionpool.py", line 1095, in _validate_conn
    conn.connect()
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connection.py", line 615, in connect
    self.sock = sock = self._new_conn()
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connection.py", line 203, in _new_conn
    raise NameResolutionError(self.host, self, e) from e
urllib3.exceptions.NameResolutionError: <urllib3.connection.HTTPSConnection object at 0x000001FBB5FA3CD0>: Failed to resolve 'c104-e.ca-tor.containers.cloud.ibm.com' ([Errno 11001] getaddrinfo failed)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\requests\adapters.py", line 667, in send
    resp = conn.urlopen(
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\connectionpool.py", line 843, in urlopen
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\urllib3\util\retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='c104-e.ca-tor.containers.cloud.ibm.com', port=30227): Max retries exceeded with url: /apis/apps/v1/namespaces/group-7/deployments/acmeair-mainservice/scale (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000001FBB5FA3CD0>: Failed to resolve 'c104-e.ca-tor.containers.cloud.ibm.com' ([Errno 11001] getaddrinfo failed)"))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\iamle\Documents\local_acmeair_g7\acmeair-driver-arthur\acmeair-driver-arthur\monitor_script_ver4_arthur", line 336, in <module>
    executing(current_pods)
  File "c:\Users\iamle\Documents\local_acmeair_g7\acmeair-driver-arthur\acmeair-driver-arthur\monitor_script_ver4_arthur", line 268, in executing
    get_response = requests.get(scale_url, headers=headers, verify=False)
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\requests\api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\requests\api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
  File "C:\Users\iamle\AppData\Local\Programs\Python\Python310\lib\site-packages\requests\adapters.py", line 700, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='c104-e.ca-tor.containers.cloud.ibm.com', port=30227): Max retries exceeded with url: /apis/apps/v1/namespaces/group-7/deployments/acmeair-mainservice/scale (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000001FBB5FA3CD0>: Failed to resolve 'c104-e.ca-tor.containers.cloud.ibm.com' ([Errno 11001] getaddrinfo failed)"))
```