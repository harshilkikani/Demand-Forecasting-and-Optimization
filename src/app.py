"""Lightweight FastAPI orchestration layer.

Endpoints:
 - POST /run/bronze -> runs bronze ingestion
 - POST /run/silver -> runs silver transform
 - POST /run/train -> trains model (requires features path)
 - POST /run/optimize -> runs optimization (requires forecast and price arrays)
 - GET /health -> simple health check
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

from .bronze_ingest import ingest_bronze
from .silver_transform import transform_bronze
from .features import build_features
from .train_model import train
from .optimize import run_optimization
from .mlflow_helper import configure_mlflow_local


app = FastAPI(title="Forecast-Opt Pipeline API")


class OptimizeRequest(BaseModel):
    forecast: List[float]
    price: List[float]


@app.get('/health')
def health():
    return {"status": "ok"}


@app.post('/run/bronze')
def run_bronze():
    path = ingest_bronze()
    return {"bronze_path": path}


@app.post('/run/silver')
def run_silver(bronze_path: str):
    out = transform_bronze(bronze_path)
    return {"silver_path": out}


@app.post('/run/features')
def run_features(silver_path: str):
    out = build_features(silver_path)
    return {"features_path": out}


@app.post('/run/train')
def run_train(features_path: str):
    configure_mlflow_local()
    try:
        res = train(features_path)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/run/optimize')
def run_opt(req: OptimizeRequest):
    if len(req.forecast) != len(req.price):
        raise HTTPException(status_code=400, detail='forecast and price length mismatch')
    out = run_optimization(req.forecast, req.price)
    return out


if __name__ == '__main__':
    import uvicorn
    configure_mlflow_local()
    uvicorn.run(app, host='0.0.0.0', port=8000)
