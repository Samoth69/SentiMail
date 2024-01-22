```bash
kubectl apply -f ingress.yml
kubectl apply -n sentimail-dev dev-secret.yml
kubectl apply -n sentimail-prod prod-secret.yml
helm install -n sentimail-dev sentimail-minio oci://registry-1.docker.io/bitnamicharts/minio -f dev-values.yml
helm install -n sentimail-prod sentimail-minio oci://registry-1.docker.io/bitnamicharts/minio -f prod-values.yml
```