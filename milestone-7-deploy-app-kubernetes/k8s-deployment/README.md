# Kubernetes Deployment Instructions

## Prerequisites
Ensure you have the following:
- A running Kubernetes cluster **Minikube** 
- `kubectl` configured to interact with your cluster
- The necessary Docker images are available for pulling (Dockerhub token generated and handy)

---
## Step 0: Setup the Minikube Cluster with 3 Nodes
```
$minikube start --nodes 4 -p prod-cluster
$cat ~/.kube/config 
$minikube status -p prod-cluster
$kubectl config use-context prod-cluster


GET NODES and LIST THEM
$kubectl get nodes
NAME               STATUS   ROLES           AGE     VERSION
prod-cluster       Ready    control-plane   3m29s   v1.31.0
prod-cluster-m02   Ready    <none>          3m17s   v1.31.0
prod-cluster-m03   Ready    <none>          3m9s    v1.31.0
prod-cluster-m04   Ready    <none>          3m      v1.31.0



$kubectl get nodes -L type
NAME               STATUS   ROLES           AGE    VERSION   TYPE
prod-cluster       Ready    control-plane   106m   v1.31.0   
prod-cluster-m02   Ready    <none>          106m   v1.31.0   application
prod-cluster-m03   Ready    <none>          106m   v1.31.0   database
prod-cluster-m04   Ready    <none>          106m   v1.31.0   dependent-services

```

## Step 1: Create the Namespace and Apply the Taints on Nodes
```
$kubectl apply -f namespaces.yml 
$kubectl apply -f apply-taints.yml 
$kubectl get nodes -L type        
```


## Step 2: Bring up Hashicorp Vault in Vault Namespaces
```
$kubectl apply -f vault/vault.yml

You should see a 
- vault pod
- vault service
- vault deployment
- vault replciaset

Check ifv vault came up successfully: 
$kubectl logs vault-5cff967498-jn2mp -n vault
```

## Step 3: Initialize -> Unseal Vault -> Enable KV Secrets Engine -> Add Secrets to Vault
```
$kubectl exec -it vault-5cff967498-jn2mp -n vault -- /bin/sh
$vault operator init

NOTE - You will now get 5 tokens + 1 root login token - it takes 3/5 tokens to unseal vault.

$vault operator unseal <token-1/5>
$vault operator unseal <token-2/5>
$vault operator unseal <token-3/5>

NOTE - At this point vault is UNSEALED

$vault status 
Sealed                  false   ----> IT IS NOW UNSEALED  


LOGIN TO VAULT and ENABLE KV SECRET STORE
> kubectl exec -it vault-<pod-id> -n vault -- vault login hvs.<root-token>
> vault secrets enable -version=1 -path=secret kv

ADD SECRETS 
> vault kv put secret/mysql-root-password password="<add-yours>"
> vault kv put secret/mysql-database name="<add-yours>"
> vault kv put secret/mysql-url url=""<add-yours>""
> vault kv put secret/dockerhub-token token=""<add-yours>""
> vault kv put secret/dockerhub-username username=""<add-yours>""

Verify - > vault kv list secret/


YOU ARE READY WITH VAULT - Setup Vault UI with Port Forward

$kubectl port-forward svc/vault 8200:8200 -n vault &

Access the Vault UI from - 
http://localhost:8200/ui/vault  (use login root token for password)
```

## Step 4: Bring up External Secrets Operator - to Sync with Vault
```
You will store your existing root token as a Kubernetes Secret for ESO to use.

GENERATE THE KUBERNETES SECRET IN STUDENT NAMESPACE (vault-token) 

$kubectl create secret generic vault-token \
  --from-literal=token=hvs.<vault-root-login-token-string>\
  -n student-api

```

## Step 5: Install External Secrets Operator Using Helm 
```
$helm install external-secrets external-secrets/external-secrets -n external-secrets

Verify this setup comes up successfully, in the external-secrets namesapce

$kubectl get all -n external-secrets

Check the logs - 
$helm list -n external-secrets
$kubectl logs deployment.apps/external-secrets -n external-secrets
$kubectl logs deployment.apps/external-secrets-cert-controller -n external-secrets
$kubectl get validatingwebhookconfiguration
$kubectl logs deployment.apps/external-secrets-webhook -n external-secrets
$kubectl get secrets -n student-api      


GOOD TO PROCEED - APPLY THE MANIFESTS (APP AND DATABASE)
```

## Step 6: Apply (vault-secret-store.yml) - Connects the ESO and Vault 
```
$kubectl apply -f external-secrets/vault-secret-store.yml
>secretstore.external-secrets.io/vault-backend created

CHECK LOGS 
$kubectl get secretstore vault-backend -n student-api

$kubectl get secrets -n student-api
$kubectl describe secretstore vault-backend -n student-api
$kubectl describe secretstore vault-backend

Look for - 
Events:
  Type    Reason  Age                    From          Message
  ----    ------  ----                   ----          -------
  Normal  Valid   3m54s (x3 over 8m54s)  secret-store  store validated - GOOD SIGN , PROCEED TO APP
```

## Step 7: Apply (external-secrets.yml) - Makes the Secrets from Secret Store Available to Namespaces
```
$kubectl apply -f external-secrets/external-secrets.yml -n student-api
> externalsecret.external-secrets.io/db-credentials created

CHECK LOGS 
$kubectl get externalsecrets -n student-api
$kubectl describe externalsecret db-credentials -n student-api
$kubectl get secrets -n student-api

Look For 
Events:
  Type    Reason   Age   From              Message
  ----    ------   ----  ----              -------
  Normal  Created  44s   external-secrets  Created Secret
```

## Step 8: Apply Database Manifest and Bring up Database
```
$kubectl apply -f db/db.yml
namespace/student-api unchanged
configmap/mysql-initdb-config created
persistentvolumeclaim/mysql-pvc created
deployment.apps/mysql-deployment created


CHECK LOGS 
$kubectl get pods -n student-api
$kubectl get pvc -n student-api
$kubectl logs mysql-698d8c9c8-h795x -n student-api 

Look for 
> 2024-10-17T01:56:33.603777Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.40'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```

## Step 9: Apply Application Manifest and Bring up Flask Application with Init Container Packaged
```
$kubectl apply -f app/app.yml
deployment.apps/flask-app unchanged / created
service/flask-app-service unchanged / created 

CHECK LOGS
$kubectl get pods -n student-api 
$kubectl logs flask-app-6465d4c6d6-4k75p -n student-api -c db-upgrade
$kubectl logs flask-app-6465d4c6d6-4k75p -n student-api 



CHECK PRIMARY CONTAINER LOGS - FLASK APP  and INIT CONTAINER LOGS 

$kubectl logs flask-app-cd5457cc8-cjjhw -n student-api -c db-upgrade
Starting DB Migration
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 5ee30765baf2, Auto-generated migration
DB Migration completed


Defaulted container "flask-app" out of: flask-app, db-upgrade (init)
 * Serving Flask app 'app.py'
 * Debug mode: off
```


## Port Forward your Application 
```
$kubectl port-forward svc/flask-app-service 5000:5000 -n student-api
Forwarding from 127.0.0.1:5000 -> 5000
Forwarding from [::1]:5000 -> 5000
```

### View it on `http://127.0.0.1:5000/api/v1/healthcheck`


### NOTE - 
- Small corrections if found , will be applied.