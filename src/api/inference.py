import joblib
import pandas as pd
from datetime import datetime
from pathlib import Path
from schemas import HousePredictionRequest, PredictionResponse

# Load model and preprocessor
MODEL_PATH = Path("models/trained/house_price_model.pkl")
PREPROCESSOR_PATH = Path("models/trained/preprocessor.pkl")

_model = None
_preprocessor = None
_load_error: str | None = None


def _try_load_artifacts() -> None:
    """
    Best-effort load of model artifacts.

    We deliberately do not crash the service at import time:
    - CI/PR builds can build the image without trained artifacts.
    - Local dev can start the API and mount artifacts later via Docker volumes.
    """
    global _model, _preprocessor, _load_error
    if _model is not None and _preprocessor is not None:
        return

    try:
        _model = joblib.load(MODEL_PATH)
        _preprocessor = joblib.load(PREPROCESSOR_PATH)
        _load_error = None
    except Exception as e:
        _model = None
        _preprocessor = None
        _load_error = str(e)


def is_model_loaded() -> bool:
    """Return True if both model + preprocessor are loaded in memory."""
    _try_load_artifacts()
    return _model is not None and _preprocessor is not None


def _require_model_loaded():
    """Return loaded artifacts or raise a helpful error."""
    _try_load_artifacts()
    if _model is None or _preprocessor is None:
        raise RuntimeError(
            "Model artifacts are not available. "
            f"Expected files: {MODEL_PATH} and {PREPROCESSOR_PATH}. "
            f"Load error: {_load_error}"
        )
    return _model, _preprocessor

def predict_price(request: HousePredictionRequest) -> PredictionResponse:
    """
    Predict house price based on input features.
    """
    model, preprocessor = _require_model_loaded()

    # Prepare input data
    input_data = pd.DataFrame([request.dict()])
    input_data['house_age'] = datetime.now().year - input_data['year_built']
    input_data['bed_bath_ratio'] = input_data['bedrooms'] / input_data['bathrooms']
    input_data['price_per_sqft'] = 0  # Dummy value for compatibility

    # Preprocess input data
    processed_features = preprocessor.transform(input_data)

    # Make prediction
    predicted_price = model.predict(processed_features)[0]

    # Convert numpy.float32 to Python float and round to 2 decimal places
    predicted_price = round(float(predicted_price), 2)

    # Confidence interval (10% range)
    confidence_interval = [predicted_price * 0.9, predicted_price * 1.1]

    # Convert confidence interval values to Python float and round to 2 decimal places
    confidence_interval = [round(float(value), 2) for value in confidence_interval]

    return PredictionResponse(
        predicted_price=predicted_price,
        confidence_interval=confidence_interval,
        features_importance={},
        prediction_time=datetime.now().isoformat()
    )

def batch_predict(requests: list[HousePredictionRequest]) -> list[float]:
    """
    Perform batch predictions.
    """
    model, preprocessor = _require_model_loaded()

    input_data = pd.DataFrame([req.dict() for req in requests])
    input_data['house_age'] = datetime.now().year - input_data['year_built']
    input_data['bed_bath_ratio'] = input_data['bedrooms'] / input_data['bathrooms']
    input_data['price_per_sqft'] = 0  # Dummy value for compatibility

    # Preprocess input data
    processed_features = preprocessor.transform(input_data)

    # Make predictions
    predictions = model.predict(processed_features)
    return predictions.tolist()