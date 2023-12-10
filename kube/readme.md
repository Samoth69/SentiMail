# cluster kube

## dashboard traefik

```bash
kubectl -n kube-system get pods
kubectl -n kube-system port-forward [nom pod traefik] 9000:9000
```

aller ici: http://127.0.0.1:9000/dashboard/

## ce qui à été fait

### réseau

- crowdsec sur opnsense
- pare-feu cloudflare avec WAF basic + filtrage ip française

### Kube

- selinux actif sur le node kube (merci k3s)

## todo

- traefik
  - désactiver les indexations des robots
    - https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=fr
  - protection DDOS ?
- kube
  - storage class
  - helm
