# github scale set

- c'est ce qui va tourner nos jobs github

```bash
kubectl create namespace arc-runners
kubectl create secret generic github-pat-classic --namespace=arc-runners --from-literal=github_token='YOUR-PAT'
helm install arc-runner-set --namespace arc-runners --values values.yaml oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
```