## Trained model artifacts

This folder is the **runtime location** for trained artifacts used by the FastAPI inference service:

- `models/trained/house_price_model.pkl`
- `models/trained/preprocessor.pkl`

### Why this file exists

Git does not track empty directories, and `.gitignore` intentionally ignores `*.pkl`.
We keep this `README.md` so the `models/trained/` directory exists in the repository,
which prevents Docker builds from failing on `COPY models/trained/...`.

### How artifacts get here

- **Locally**: after training, place the generated `*.pkl` files in this directory.
- **CI (recommended)**: the `MLOps CI` workflow downloads trained artifacts into this directory
  before building/publishing Docker images (manual `workflow_dispatch` run).

