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
```

## Step 1: Create the Namespaces , Labels and 
```
$kubectl apply -f namespaces.yml 
$kubectl apply -f apply-taints.yml  (note - going forward this only applies labels, not taints - affinity now )


VERIFY SETUP - 
$kubectl get nodes -L type   

NAME               STATUS   ROLES           AGE    VERSION   TYPE
helm-cluster       Ready    control-plane   2d7h   v1.31.0   
helm-cluster-m02   Ready    <none>          2d7h   v1.31.0   application
helm-cluster-m03   Ready    <none>          2d7h   v1.31.0   database
helm-cluster-m04   Ready    <none>          2d7h   v1.31.0   dependent-services

```

## Step 2: Install Vault with Helm Chart and Custom Values File 
```
ADD TO REPO
$helm repo add hashicorp https://helm.releases.hashicorp.com
$helm repo update

INSTALL
$helm install vault hashicorp/vault --namespace vault --values helm-vault-raft-values.yml

VERIFY (Ensure no errors)
$kubectl get pods -n vault
$kubectl logs vault-0 -n vault
```

## Step 3: Configure Vault - Unlock and Add your Keys into It (Namespace = Vault)
```
SETUP PORT FORWARD - 
$kubectl -n vault port-forward service/vault 8200:8200 &


INITIALIZE VAULT WITH REQUIRED KEYS 
$kubectl -n vault exec vault-0 -- vault operator init -format=json -key-shares=1 -key-threshold=1 > vault-keys.json

CONTENTS - 
{
  "keys": [
    "<your-key-wil-be-generated-here>"
  ],
  "keys_base64": [
    "<your-key-wil-be-generated-here-in-base-64-encoding>"
  ],
  "root_token": "hvs.<token-id>"
}

UNSEAL VAULT
$vault operator unseal <your-key-wil-be-generated-here-in-base-64-encoding>

LOGIN TO VAULT 
$vault login vault login hvs.<token-id>

ENABLE KV SECRET STORE - 
$kubectl exec -it vault-0 -n vault -- vault secrets enable -version=1 -path=secret kv

ADD YOUR SECRETS
vault kv put secret/mysql-root-password password="<password>"
vault kv put secret/mysql-database name="<db-name>"
vault kv put secret/mysql-url url="mysql://root:newpassword@mysql-service:3306/student_db"
vault kv put secret/dockerhub-token token="<docker-login-token>"
vault kv put secret/dockerhub-username username="<docker-username>"
vault kv put secret/keychain-password password="<for-mac-users-only-this-is-your-laptop-admin-password>"
```

### Step 5: Add Secrets for Vault Token
```
$kubectl create secret generic vault-token \
  --from-literal=token=hvs.QI9NXMV0k90DVxnkJiPqM8uA \
  -n student-api

$kubectl get secrets -n student-api                  
NAME          TYPE     DATA   AGE
vault-token   Opaque   1      21s. -> CREATED

```

### Step 5: Install External-Secrets Operator using Helm-Charts (Namespace = ExternalSecrets)
```
$helm repo add external-secrets https://charts.external-secrets.io
$helm install external-secrets external-secrets/external-secrets -n external-secrets

VERIFY
$kubectl get all -n external-secrets
$helm list -n external-secrets
$kubectl logs deployment.apps/external-secrets -n external-secrets
$kubectl logs deployment.apps/external-secrets-cert-controller -n external-secrets
$kubectl get validatingwebhookconfiguration
$kubectl logs deployment.apps/external-secrets-webhook -n external-secrets
$kubectl get secrets -n external-secrets        

GOOD TO PROCEED
```


### Step 6: Bring up the Application - (Namespace = Student-API)
```
$helm install api ./api-charts --namespace student-api

VALIDATE
$kubectl get secretstore -n student-api
#validate the vault-token.
$kubectl get secret vault-token -n student-api 
$kubectl describe secretstore vault-secret-store -n student-api
8.3 create the Externalsecrerts template & values file
```

### Step 7: Port Forwarding Services that are Required 
```
Flask Application  
$kubectl port-forward service/api-service-new 5000:5000 -n student-api  &

Vault Service 
$kubectl port-forward svc/vault-ui 8200:8200 -n vault &
```

### Step 8: Validate with your Browser + Postman Collection
```
present in the root directory
```

### Step 9: Delete Everything  - Tear Down
```
minikube delete --profile helm-cluster
``