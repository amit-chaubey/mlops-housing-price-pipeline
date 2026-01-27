# 🏠 Housing Price Prediction - MLOps Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

![UV](https://img.shields.io/badge/UV-FFD43B?style=for-the-badge&logo=python&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

---

## 📋 Overview

An end-to-end MLOps pipeline for housing price prediction, featuring comprehensive data processing, experiment tracking, and model deployment capabilities.

## 🔄 Current Status

**Phase 1: Data Engineering & Exploration** ✅

We are currently focused on data-related operations:
- **Data Preprocessing**: Cleaning, validation, and transformation of raw housing data
- **Exploratory Data Analysis**: Statistical analysis and visualization of dataset characteristics
- **MLflow Integration**: All data processing steps are tracked and logged in MLflow for full experiment traceability

**Phase 2: Model Training** 🚧 (Coming Soon)

Model training and evaluation will be implemented next, with full MLflow experiment tracking.

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.9+ |
| **Package Management** | UV, pip |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Visualization** | Matplotlib, Seaborn |
| **Experiment Tracking** | MLflow |
| **Notebooks** | Jupyter |
| **API Framework** | FastAPI |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes |

## 📁 Project Structure

```
├── data/              # Raw and processed datasets
├── notebooks/         # Jupyter notebooks for analysis
├── src/               # Source code modules
│   ├── data/         # Data processing scripts
│   ├── features/     # Feature engineering
├── deployment/        # Docker & Kubernetes configs
└── models/            # Trained model artifacts
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run data processing
python src/data/run_processing.py

# Start MLflow UI
mlflow ui
```

## 📊 MLflow Tracking

All experiments, data processing steps, and model artifacts are tracked in MLflow, providing:
- Complete experiment lineage
- Reproducible data transformations
- Model versioning and comparison
- Performance metrics visualization

---

<div align="center">

**Built with ❤️ for MLOps Excellence**

</div>
