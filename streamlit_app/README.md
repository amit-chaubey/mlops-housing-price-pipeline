## Streamlit UI (`streamlit_app`)

This folder contains the **Streamlit frontend** for the House Price Prediction project. The app:

- Serves the UI on port **8501**
- Calls the FastAPI inference API endpoint via `POST /predict`
- Uses `API_URL` to locate the API service

## Quickstart (Docker Compose — recommended)

From the repository root, start both the API and the UI:

```bash
docker compose up --build
```

Then open the UI at `http://localhost:8501`.

In Compose, the Streamlit container is configured with:

- `API_URL=http://fastapi:8000`

So it can reach the FastAPI service by its Compose service name (`fastapi`) over the internal Docker network.

## Build & run the Streamlit image (Docker only)

If you want to build/run the Streamlit container independently:

### Build

Run this from the **repository root** (build context must be `streamlit_app/`):

```bash
docker build -t streamlit-ml:dev -f streamlit_app/Dockerfile streamlit_app
```

### Run

If your FastAPI API is running on your host at port 8000:

```bash
docker run --rm -p 8501:8501 \
  -e API_URL="http://host.docker.internal:8000" \
  streamlit-ml:dev
```

Then open `http://localhost:8501`.

## Run locally (no Docker)

```bash
cd streamlit_app
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
API_URL="http://localhost:8000" streamlit run app.py
```

## Configuration

- **`API_URL`**: base URL for the FastAPI service (the app calls `"$API_URL/predict"`).
  - Compose default: `http://fastapi:8000`
  - Local default (recommended): `http://localhost:8000`
  - App fallback (if unset): `http://model:8000` (see `app.py`)
- **`APP_VERSION`**: optional version string displayed by the UI (default: `1.0.0`)

## Container build notes (what the Dockerfile does)

The `streamlit_app/Dockerfile`:

- **Base image**: `python:3.9-slim`
- **Copies** the Streamlit app source into `/app`
- **Installs** dependencies using `pip install -r requirements.txt`
- **Exposes** port `8501`
- **Starts** Streamlit with `streamlit run app.py --server.address=0.0.0.0`

## Production considerations

For production deployments, treat Streamlit as a web app behind a gateway:

- Put it behind a **reverse proxy / ingress** (TLS termination, auth, rate limiting).
- Configure **resource limits** (CPU/memory) and **replicas** at the orchestrator level.
- Ensure `API_URL` points to a stable internal API address (service DNS), not localhost.
- Avoid committing secrets; pass configuration via environment variables or secret stores.