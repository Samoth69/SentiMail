# postgres

```bash
kubectl apply -f dev-secret.yml -f prod-secret.yml

helm upgrade --install -n sentimail-dev sentimail-postgres oci://registry-1.docker.io/bitnamicharts/postgresql -f dev-values.yml
helm upgrade --install -n sentimail-prod sentimail-postgres oci://registry-1.docker.io/bitnamicharts/postgresql -f prod-values.yml
```