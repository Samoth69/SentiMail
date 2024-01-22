```bash
helm upgrade --install -n sentimail-dev sentimail-rabbitmq oci://registry-1.docker.io/bitnamicharts/rabbitmq -f dev-values.yml
helm upgrade --install -n sentimail-prod sentimail-rabbitmq oci://registry-1.docker.io/bitnamicharts/rabbitmq -f prod-values.yml
```