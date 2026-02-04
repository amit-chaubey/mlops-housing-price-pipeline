# Helm

Charts and instructions for deploying the ML housing stack and the observability stack (Prometheus + Grafana).

- **mlflow-housing/** — ML model + UI (custom chart)
- **monitoring/** — Placeholder; use `kube-prometheus-stack` below for Prometheus + Grafana

---

## Installing Helm

Install Helm v3 on Linux or macOS:

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

See [Official Helm install instructions](https://helm.sh/docs/intro/install/) for other options.

Verify:

```bash
helm --help
helm version
```

---

## Deploy Prometheus + Grafana with Helm

Use the [kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack) chart (Prometheus + Grafana + common exporters).

Add the Helm repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Install the stack (Grafana NodePort **30200**, Prometheus NodePort **30300**):

```bash
helm upgrade --install prom \
  -n monitoring \
  --create-namespace \
  prometheus-community/kube-prometheus-stack \
  --set grafana.service.type=NodePort \
  --set grafana.service.nodePort=30200 \
  --set prometheus.service.type=NodePort \
  --set prometheus.service.nodePort=30300
```

Validate:

```bash
helm list -A
kubectl get all -n monitoring
```

- **Grafana**: `http://<node-ip>:30200` (default login `admin` / `prom-operator`)
- **Prometheus**: `http://<node-ip>:30300`
