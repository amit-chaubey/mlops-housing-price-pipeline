## FastAPI inference service (`src/api`)

This folder contains the **House Price Prediction API** implemented with FastAPI. It exposes:

- `GET /health`: health check
- `POST /predict`: single prediction (returns a structured response)
- `POST /batch-predict`: batch prediction (returns a list of predicted prices)

The service loads a trained model and preprocessor at import time from:

- `models/trained/house_price_model.pkl`
- `models/trained/preprocessor.pkl`

If either file is missing (or incompatible), the API will fail to start with a clear error.

## API contract

### Request schema (`HousePredictionRequest`)

`POST /predict` and `POST /batch-predict` accept the same input fields:

- `sqft` (float, `> 0`): square footage
- `bedrooms` (int, `>= 1`): number of bedrooms
- `bathrooms` (float, `> 0`): number of bathrooms
- `location` (str): e.g. `urban`, `suburban`, `rural`
- `year_built` (int, `1800..2023`): year built (validated)
- `condition` (str): e.g. `Good`, `Excellent`, `Fair`

### Responses

- `POST /predict` returns:
  - `predicted_price` (float)
  - `confidence_interval` (list[float]) — currently a \(\pm 10\%\) range
  - `features_importance` (dict) — currently empty
  - `prediction_time` (ISO timestamp)
- `POST /batch-predict` returns: `list[float]` (predicted prices)

## Run locally (development)

The imports in `main.py` are written to run from **within** `src/api`. Use a virtual environment and start Uvicorn from that directory.

```bash
cd src/api
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- Interactive docs: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Health: `http://localhost:8000/health`

## Run with Docker (recommended for parity)

This repo builds the API container from the **root** `Dockerfile` (base image `python:3.11-slim`) and starts Uvicorn with:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

From the repository root:

```bash
docker compose up --build
```

This will start:

- FastAPI on `http://localhost:8000`
- Streamlit on `http://localhost:8501` (configured to call the API via `http://fastapi:8000` inside Compose)

## Example requests

### Health check

```bash
curl -s http://localhost:8000/health
```

### Single prediction

```bash
curl -s -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1800,
    "bedrooms": 3,
    "bathrooms": 2,
    "location": "suburban",
    "year_built": 2005,
    "condition": "Good"
  }'
```

### Batch prediction

```bash
curl -s -X POST "http://localhost:8000/batch-predict" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "sqft": 1800,
      "bedrooms": 3,
      "bathrooms": 2,
      "location": "suburban",
      "year_built": 2005,
      "condition": "Good"
    },
    {
      "sqft": 950,
      "bedrooms": 2,
      "bathrooms": 1,
      "location": "urban",
      "year_built": 1995,
      "condition": "Fair"
    }
  ]'
```

## Notes / gotchas

- **Model artifacts are required**: ensure `models/trained/house_price_model.pkl` and `models/trained/preprocessor.pkl` exist in the runtime filesystem.
- **CORS is wide open**: the API enables CORS for all origins/methods/headers (useful for demos; tighten for production).
- **`year_built` validation**: requests with `year_built > 2023` will be rejected by schema validation (this is enforced in `schemas.py`).

