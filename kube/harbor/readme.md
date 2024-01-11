# Harbor

Permet de stocker les images docker custom

```bash
# creation namespace
kubectl create namespace harbor
# config spécifique traefik
kubectl -n harbor apply -f .\ingressRoute.yaml
# on démarre l'appli
helm -n harbor install my-harbor harbor/harbor --values ./values.yaml
```
