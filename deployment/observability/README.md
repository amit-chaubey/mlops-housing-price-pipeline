# Observability

Placeholder for Prometheus and Grafana. Use **kube-prometheus-stack** (Helm) for full cluster monitoring.

- **prometheus/** — scrape configs and custom rules (optional)
- **grafana/** — custom dashboards and datasources (optional)

---

## kube-prometheus-stack (Prometheus + Grafana)

**Prerequisites:** Kubernetes 1.19+, Helm 3+

### Install via OCI

```bash
helm install prom oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack \
  -n monitoring --create-namespace \
  --set grafana.service.type=NodePort \
  --set grafana.service.nodePort=30200 \
  --set prometheus.service.type=NodePort \
  --set prometheus.service.nodePort=30300
```

### Install via Helm repo (alternative)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prom prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  --set grafana.service.type=NodePort \
  --set grafana.service.nodePort=30200 \
  --set prometheus.service.type=NodePort \
  --set prometheus.service.nodePort=30300
```

### Show default values

```bash
helm show values oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack
```

### Uninstall and remove CRDs

```bash
helm uninstall prom -n monitoring
# Remove CRDs manually:
kubectl delete crd alertmanagerconfigs.monitoring.coreos.com \
  alertmanagers.monitoring.coreos.com podmonitors.monitoring.coreos.com \
  probes.monitoring.coreos.com prometheusagents.monitoring.coreos.com \
  prometheuses.monitoring.coreos.com prometheusrules.monitoring.coreos.com \
  scrapeconfigs.monitoring.coreos.com servicemonitors.monitoring.coreos.com \
  thanosrulers.monitoring.coreos.com
```

**Access:** Grafana `http://<node-ip>:30200` · Prometheus `http://<node-ip>:30300`

For full Helm instructions and script, see **deployment/helm/README.md** and **deployment/helm/install-prometheus-stack.sh**.
