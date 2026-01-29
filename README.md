## Housing Price Prediction — End-to-end MLOps Project

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Frames-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Arrays-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Boosting-337ab7?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI%20Server-2f2f2f?style=for-the-badge&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Multi--Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)

</div>

An end-to-end project for **housing price prediction** covering:

- Data exploration and feature engineering (notebooks + repeatable scripts)
- Model training with experiment tracking via MLflow
- Model serving via FastAPI (Uvicorn) and a Streamlit UI client
- Containerization with Docker and orchestration-ready deployment scaffolding

**Owner / Maintainer**: Amit Choubey (Hector Labs)

---

## Architecture (high level)

```
Raw CSV -> Cleaned CSV -> Featured CSV + Preprocessor -> Trained Model
   |           |                 |                      |
 data/raw   data/processed   models/trained         FastAPI (/predict)
                                                        |
                                                     Streamlit UI
```

---

## Repository layout (what to look at)

```
configs/
  model_config.yaml              # Training configuration (model name, params, target)
data/
  raw/                           # Raw dataset(s) you can replace/modify
  processed/                     # Cleaned + featured datasets produced by pipeline
deployment/
  kubernetes/                    # Kubernetes scaffolding (bird’s-eye guidance below)
  mlflow/                        # Optional MLflow tracking server (docker-compose)
models/
  trained/                       # Inference artifacts used by the API
notebooks/
  01_data_preprocessing.ipynb
  02_data_exploration.ipynb
  02_feature_engineering.ipynb
  03_experimentation.ipynb
src/
  data/run_processing.py         # Script: raw -> cleaned
  features/engineer.py           # Script: cleaned -> featured + preprocessor.pkl
  models/train_model.py          # Script: train + log to MLflow + save model pkl
  api/                           # FastAPI app (inference)
streamlit_app/
  app.py                         # Streamlit UI
  Dockerfile                     # UI container build
docker-compose.yaml              # Run FastAPI + Streamlit together
Dockerfile                       # Build FastAPI inference image (repo root)
```

---

## Local setup (clone → venv → install)

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Recommended execution sequence (data → model → serving)

This repo supports both a **notebook-first** workflow for understanding and a **script-first** workflow for repeatability.

### 1) Inspect / update the raw data

- Put your raw CSV in `data/raw/` (default file expected by the script: `data/raw/house_data.csv`)
- Review existing processed data examples in `data/processed/`

### 2) Data preprocessing (raw → cleaned)

**Notebook (explainable):**

- Run `notebooks/01_data_preprocessing.ipynb`

**Script (repeatable):**

```bash
python src/data/run_processing.py
```

This produces:

- `data/processed/cleaned_house_data.csv`

### 3) Data exploration (EDA)

- Run `notebooks/02_data_exploration.ipynb` (reads `data/processed/cleaned_house_data.csv`)

### 4) Feature engineering (cleaned → featured + preprocessor)

You have two options:

- `notebooks/02_feature_engineering.ipynb` (primarily for analysis; exports `data/processed/data_scientists_features.csv`)
- `src/features/engineer.py` (production-oriented; exports `data/processed/featured_house_data.csv` + `models/trained/preprocessor.pkl`)

Recommended (repeatable) path:

```bash
python src/features/engineer.py \
  --input data/processed/cleaned_house_data.csv \
  --output data/processed/featured_house_data.csv \
  --preprocessor models/trained/preprocessor.pkl
```

Validate:

```bash
ls models/trained/
```

### 5) Experimentation (model selection / config)

- Run `notebooks/03_experimentation.ipynb` to explore models and tune approaches.
- Ensure `configs/model_config.yaml` reflects the final training configuration you want.

### 6) Train the final model (featured → model artifact)

You can track experiments locally (default MLflow file store) **or** run an MLflow tracking server.

#### Option A: run MLflow tracking server (recommended)

Start MLflow via the included compose file:

```bash
docker compose -f deployment/mlflow/docker-compose.yaml up
```

This exposes MLflow at `http://localhost:5555`.

Train and log to MLflow:

```bash
python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --models-dir models \
  --mlflow-tracking-uri http://localhost:5555
```

#### Option B: track locally (no server)

```bash
python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --models-dir models
```

Validate artifacts:

```bash
ls models/trained/
```

Expected:

- `models/trained/preprocessor.pkl`
- `models/trained/house_price_model.pkl`

---

## Serve the model (FastAPI) + UI (Streamlit)

### Option A: Docker Compose (recommended)

From repo root:

```bash
docker compose up --build
```

Validate:

- FastAPI docs: `http://localhost:8000/docs`
- Streamlit UI: `http://localhost:8501`

`docker-compose.yaml` also sets:

- `API_URL=http://fastapi:8000` (Streamlit -> FastAPI inside the Compose network)

### Option B: run containers directly (pull & run)

This repo’s `docker-compose.yaml` references these image tags:

- FastAPI image: `akatyayana/fastapi-ml:dev`
- Streamlit image: `akatyayana/streamlit-ml:dev`

Pull (if published in your registry):

```bash
docker pull akatyayana/fastapi-ml:dev
docker pull akatyayana/streamlit-ml:dev
```

Registry lookup shortcuts:

- FastAPI image search: `https://hub.docker.com/search?q=akatyayana%2Ffastapi-ml`
- Streamlit image search: `https://hub.docker.com/search?q=akatyayana%2Fstreamlit-ml`

Run FastAPI (requires the `.pkl` artifacts to be inside the image or mounted):

```bash
docker run --rm -p 8000:8000 akatyayana/fastapi-ml:dev
```

Run Streamlit pointing to the API on your host:

```bash
docker run --rm -p 8501:8501 \
  -e API_URL="http://host.docker.internal:8000" \
  akatyayana/streamlit-ml:dev
```

---

## Build, tag, and push images (for your registry)

### FastAPI image (repo root `Dockerfile`)

Build:

```bash
docker build -t akatyayana/fastapi-ml:dev -f Dockerfile .
```

Push:

```bash
docker push akatyayana/fastapi-ml:dev
```

### Streamlit image (`streamlit_app/Dockerfile`)

Build (from repo root; build context is `streamlit_app/`):

```bash
docker build -t akatyayana/streamlit-ml:dev -f streamlit_app/Dockerfile streamlit_app
```

Push:

```bash
docker push akatyayana/streamlit-ml:dev
```

---

## Troubleshooting (common, practical)

### Ports already in use

If you see “bind: address already in use”, either stop the conflicting process/container or change host-side ports in `docker-compose.yaml`.

### Inspect containers

```bash
docker compose ps
docker compose logs -f fastapi
docker compose logs -f streamlit
```

### Shell into a container (debug dependency/runtime issues)

```bash
docker compose exec fastapi sh
docker compose exec streamlit sh
```

From inside the container you can:

- Inspect installed packages: `pip list`
- Reinstall dependencies: `pip install -r requirements.txt`

Best practice is to **fix dependency issues in the repo requirements files** and rebuild:

```bash
docker compose build --no-cache
docker compose up --build
```

---

## Kubernetes (bird’s-eye view)

The `deployment/kubernetes/` folder is intended for container orchestration. Typical production deployment patterns include:

- **Deployment** for FastAPI (stateless inference pods)
- **Service** (ClusterIP) to expose FastAPI internally
- **Ingress** (or an API Gateway) to expose FastAPI externally behind a **load balancer**
- **HPA (Horizontal Pod Autoscaler)** to scale pods based on CPU/latency signals

Local experimentation: **minikube**  
Managed production: **AWS EKS** (or equivalent), with an ingress controller + managed load balancer.

---

## Ownership

Copyright © Amit Choubey (Hector Labs). All rights reserved.
