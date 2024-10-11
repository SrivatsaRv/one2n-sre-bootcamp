# Milestone-6: Setup a Kubernetes Cluster 
We need to spin up a three-node Kubernetes cluster using Minikube on your local. Going forward we will treat this Kubernetes cluster as our production cluster.

### Out of these three nodes
- Node A will be used by our application.
- Node B will be used for running dependent services.
- Node C will be used for running our observability stack.


## Prerequisites
Before getting started, ensure you have the following prerequisites:

- Minikube
- Kubectl 
- Docker Desktop


## How to Run ?

**Step-1**: Setup a 4 node minikube cluster (1 master + 3 worker)
```
$minikube start --nodes 4 -p prod-cluster
```

**Step-2**: Setup the labels on nodes with kubectl
```
$kubectl label nodes prod-cluster-m02 type=application
$kubectl label nodes prod-cluster-m03 type=dependency-app
$kubectl label nodes prod-cluster-m04 type=monitoring-stack


$kubectl get nodes -L type
NAME               STATUS   ROLES           AGE   VERSION   TYPE
prod-cluster       Ready    control-plane   23h   v1.31.0   
prod-cluster-m02   Ready    <none>          23h   v1.31.0   flask-app
prod-cluster-m03   Ready    <none>          23h   v1.31.0   dependency-app
prod-cluster-m04   Ready    <none>          23h   v1.31.0   monitoring-stack

```


**Step-3**: Use Vagrant to Bring Up the Setup in 1 Click
```
$vagrant up

#Expected Output 

   default: 66b98279bfb9 Pull complete
    default: nginx Pulled
    default: Container mysql_container  Running
    default: Container flask_api2  Running
    default: Container flask_api1  Running
    default: Container nginx_container  Creating
    default: Container nginx_container  Created
    default: Container nginx_container  Starting
    default: Container nginx_container  Started
    default: API Services, NGINX, and MySQL deployed successfully.

NOTE - You will be prompoted for VM Download  by UTM - Click ALLOW -> Wait for It -> Mount your Milestone-5 Path (from your cloned dir setup) -> Click yes on CLI
- this is a MacOS specific constraint being addressed. 

```


**Step-4**: Services will be up on your ifconfig-a (newly created bridged network IP) 
```
bridge100: flags=8a63<UP,BROADCAST,SMART,RUNNING,ALLMULTI,SIMPLEX,MULTICAST> mtu 1500
        options=3<RXCSUM,TXCSUM>
        ether 52:a6:d8:7d:b1:64
        inet 192.168.64.1 netmask 0xffffff00 broadcast 192.168.64.255     --------------------------->>> THIS IS THE UP YOU NEED TO HIT YOUR BROWSER WITH + POSTMAN
        inet6 fe80::50a6:d8ff:fe7d:b164%bridge100 prefixlen 64 scopeid 0x14 


### Expectations
The following expectations should be met to complete this milestone.
- Three node Kubernetes cluster using Minikube should be spun up - ✅
- Appropriate node labels should be added to these three nodes - ✅
