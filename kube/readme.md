# cluster kube

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
