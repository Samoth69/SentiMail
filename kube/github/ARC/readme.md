# Github PAT

```bash
kubectl create namespace arc-systems
kubectl create secret generic github-pat-classic --namespace=arc-systems --from-literal=github_token='YOUR-PAT'
NAMESPACE="arc-systems"
helm install arc --namespace arc-systems --values values.yaml oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```