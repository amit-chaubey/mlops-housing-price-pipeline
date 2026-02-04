#!/usr/bin/env bash
# Install Prometheus + Grafana via kube-prometheus-stack (Grafana 30200, Prometheus 30300).
set -e
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prom \
  -n monitoring \
  --create-namespace \
  prometheus-community/kube-prometheus-stack \
  --set grafana.service.type=NodePort \
  --set grafana.service.nodePort=30200 \
  --set prometheus.service.type=NodePort \
  --set prometheus.service.nodePort=30300
echo "Done. Check: helm list -A && kubectl get all -n monitoring"
echo "Grafana: http://<node-ip>:30200  |  Prometheus: http://<node-ip>:30300"
