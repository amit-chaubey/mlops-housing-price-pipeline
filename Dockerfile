FROM python:3.11-slim

# FastAPI inference image (repo root).
# This image packages:
# - Python dependencies from root `requirements.txt`
# - API source code from `src/api/`
# - Pre-trained model artifacts from `models/trained/*.pkl`
#
# Container runtime:
# - Starts Uvicorn serving `main:app` on port 8000
WORKDIR /app

# Install root requirements first.
# Copying `requirements.txt` before the source enables Docker layer caching:
# dependency installation is only re-run when requirements change.
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy API source.
# Note: This Dockerfile assumes `src/api/main.py` is copied into `/app/main.py`,
# so the Uvicorn target `main:app` resolves correctly from WORKDIR `/app`.
COPY src/api/ /app/

# Copy trained model artifacts into the container so inference can run offline.
# Note:
# - CI/PR builds might not have trained artifacts present (because `*.pkl` are gitignored).
# - Full "production-like" images should be built after training, when `models/trained/*.pkl`
#   exist in the build context (or mounted at runtime).
RUN mkdir -p models/trained
# Copy the directory (not a glob) so the build won't fail when no `.pkl` exist yet.
COPY models/trained/ models/trained/

# Document the port the container listens on (Uvicorn `--port 8000`).
EXPOSE 8000

# Start the FastAPI app with Uvicorn.
# `--host 0.0.0.0` binds to all interfaces so Docker can expose the port.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
