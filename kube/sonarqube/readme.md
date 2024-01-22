# Sonarqube

```bash
helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube
helm repo update
kubectl create namespace sonarqube
kubectl apply -f secret.yml
helm upgrade --install -n sonarqube sonarqube sonarqube/sonarqube -f values.yml
```