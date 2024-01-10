# crowdsec

```bash
helm install crowdsec crowdsec/crowdsec -f crowdsec-values.yaml -n crowdsec --create-namespace
helm install -n kube-system traefik-bouncer crowdsec/crowdsec-traefik-bouncer -f crowdsec-traefik-bouncer-values.yaml
```