FROM python:3.9-slim

# Streamlit UI image (built from `streamlit_app/` context).
# This container serves the interactive frontend and calls the FastAPI service.
# It expects `app.py` and `requirements.txt` to be present in this directory.
WORKDIR /app

# Copy the Streamlit app source + its local dependency manifest into the image.
# (This Dockerfile is built with `streamlit_app/` as the build context in Compose.)
COPY . .

# Install Streamlit app dependencies.
# Note: keeping this as-is preserves the current build behavior and dependency resolution.
RUN pip install -r requirements.txt

# Document the port Streamlit listens on.
EXPOSE 8501

# Run Streamlit, binding to all interfaces so Docker can expose the port.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0" ] 
