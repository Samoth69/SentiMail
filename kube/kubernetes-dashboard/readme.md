# kubernetes-dashboard

## install

```bash
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
# Deploy a Helm Release named "kubernetes-dashboard" using the kubernetes-dashboard chart
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
# on ajoute l'admin-user si c'est pas déjà fait
kubectl -n kubernetes-dashboard apply -f dashboard.yml
```

## usage

```bash
# token pour s'authentifier
kubectl -n kubernetes-dashboard create token admin-user
# récupérer le nom du pod de la dashboard
kubectl -n kubernetes-dashboard get pods
# ouverture du flux entre votre pc et le kubernetes-dashboard
kubectl -n kubernetes-dashboard port-forward NOM_POD_KUBE_DASHBOARD 8443:8443
```

Ouvrez l'adresse https://127.0.0.1:8443  
Il est normal d'avoir une erreur SSL pour certificat auto signé.

## liens utiles

- values helm https://github.com/kubernetes/dashboard/blob/master/charts/helm-chart/kubernetes-dashboard/values.yaml
