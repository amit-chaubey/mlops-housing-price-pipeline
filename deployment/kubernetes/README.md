# Kubernetes deployment

- **base/** — shared manifests (model + UI deployments and services). Use as-is or via Kustomize.
- **overlays/dev** — dev overlay (e.g. `kubectl kustomize deployment/kubernetes/overlays/dev`).
- **overlays/prod** — prod overlay.

Existing manifests in this directory (root) are kept for backward compatibility.
