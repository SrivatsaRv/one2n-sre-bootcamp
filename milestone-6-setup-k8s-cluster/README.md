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


### Handy Commands - to handle minikube context-switches
```
$ minikube status -p app-cluster      
$ kubectl config use-context app-cluster

if you don't do this , minikube will assume minikube cluster context
```