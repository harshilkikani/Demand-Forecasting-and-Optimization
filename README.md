# Spain Energy Forecasting & Optimization Pipeline  

## 📌 Overview  
This project demonstrates an **end-to-end data pipeline** for forecasting and optimization using **PySpark, Delta Lake, Databricks, FastAPI, and Jenkins**. It was built to showcase real-world data engineering + machine learning workflows, including:  

- **Medallion architecture (Bronze → Silver → Gold)** with Delta Lake  
- **Time series forecasting** with rolling averages and ensemble methods (SARIMAX/XGBoost)  
- **Prescriptive optimization** using Google OR-Tools  
- **API layer** with FastAPI + Pydantic for request/response validation  
- **CI/CD automation** via Jenkins for testing and deployment  

The use case is based on **renewable energy demand forecasting in Spain**, leveraging public datasets with hourly consumption, pricing, and weather features.  

---

## ⚡ Tech Stack  
- **Databricks** — distributed compute, Delta Lake, MLflow tracking  
- **PySpark** — scalable ETL, feature engineering, forecasting workflows  
- **Delta Lake** — ACID-compliant storage for Medallion architecture  
- **XGBoost / SARIMAX** — forecasting models  
- **OR-Tools** — optimization for energy allocation planning  
- **FastAPI + Pydantic** — REST API layer for serving forecasts and optimization plans  
- **Jenkins** — CI/CD pipeline (lint, test, deploy)  

---

## 🏗 Project Architecture  
        +------------------+
        |   Bronze Layer   |   (raw ingestion: energy, weather CSVs)
        +------------------+
                 |
                 v
        +------------------+
        |   Silver Layer   |   (cleaning, joins, timestamps)
        +------------------+
                 |
                 v
        +------------------+
        |    Gold Layer    |   (features, rolling means, calendar vars)
        +------------------+
                 |
      -----------------------
      |          |           |
      v          v           v
 Forecasting   Optimization   API

---

## 🚀 Getting Started  

### 1. Clone the repo & install dependencies  
```bash
git clone https://github.com/<your-username>/spain-energy.git
cd spain-energy
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

### 2. Download the Spain energy + weather datasets from Kaggle and place them in data/:
energy_dataset.csv
weather_features.csv

### 3. Run pipeline locally

python jobs/01_bronze_ingest.py
python jobs/02_silver_join.py
python jobs/03_gold_features.py
python jobs/04_forecast.py
python jobs/05_optimize.py

### 4. Launch API service
uvicorn api.main:app --reload --port 8000

Endpoints:
- POST /runs/full → run full pipeline
- GET /plans → fetch optimization plan

### 5. Run tests
pytest -q
