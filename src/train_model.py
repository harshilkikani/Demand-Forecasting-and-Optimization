"""Train an XGBoost model and log to MLflow.

This is a simple, local trainer that reads feature parquet, converts to pandas,
trains an XGBoost regressor to predict a target column named `load` (energy
consumption), and logs parameters/metrics to MLflow. The code is intentionally
compact for demonstration and testing.
"""
import os
import mlflow
import xgboost as xgb
import pandas as pd


def train(features_path: str, target: str = "load", run_name: str = "xgb_run") -> dict:
    df = pd.read_parquet(features_path)
    if target not in df.columns:
        raise ValueError(f"target column '{target}' not found in features")

    X = df.drop(columns=[target])
    y = df[target]

    params = {"objective": "reg:squarederror", "n_estimators": 50, "max_depth": 3}

    mlflow.set_experiment("energy_forecast")
    with mlflow.start_run(run_name=run_name) as run:
        model = xgb.XGBRegressor(**params)
        model.fit(X, y)

        preds = model.predict(X)
        rmse = ((preds - y) ** 2).mean() ** 0.5

        mlflow.log_params(params)
        mlflow.log_metric("rmse", float(rmse))
        mlflow.sklearn.log_model(model, "model")

        return {"run_id": run.info.run_id, "rmse": float(rmse)}


if __name__ == "__main__":
    print("This script trains a trivial XGBoost model. Call train(features_path)")