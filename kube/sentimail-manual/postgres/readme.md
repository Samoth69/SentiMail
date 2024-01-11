# postgres

```powershell
kubectl create secret generic postgres-secret --from-file .\postgres\user-password --from-file .\postgres\admin-password

helm install sentimail-postgres oci://registry-1.docker.io/bitnamicharts/postgresql -f values.yml
```