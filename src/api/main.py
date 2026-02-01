from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from inference import predict_price, batch_predict, is_model_loaded
from schemas import HousePredictionRequest, PredictionResponse

# Initialize FastAPI app with metadata
app = FastAPI(
    title="House Price Prediction API",
    description=(
        "An API for predicting house prices based on various features. "
        "Maintained by Amit Choubey at Hector Labs."
    ),
    version="1.0.0",
    contact={
        "name": "Amit Choubey",
        "url": "https://hectorlabs.co.uk",
        "email": "amit@hectorlabs.co.uk",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy", "model_loaded": is_model_loaded()}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: HousePredictionRequest):
    try:
        return predict_price(request)
    except RuntimeError as e:
        # Common in CI/PR builds where model artifacts are not present.
        raise HTTPException(status_code=503, detail=str(e))

# Batch prediction endpoint
@app.post("/batch-predict", response_model=list)
async def batch_predict_endpoint(requests: list[HousePredictionRequest]):
    try:
        return batch_predict(requests)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))