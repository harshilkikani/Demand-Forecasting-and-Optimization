import os
from src.bronze_ingest import ingest_bronze
from src.silver_transform import transform_bronze
from src.features import build_features
from src.optimize import run_optimization


def test_bronze_and_silver(tmp_path):
    # run bronze using project root
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bronze = ingest_bronze(root)
    assert bronze is not None

    silver = transform_bronze(bronze)
    assert silver is not None


def test_features_and_optimize():
    # create tiny forecast and price
    forecast = [100.0, 120.0, 80.0]
    price = [10.0, 5.0, 12.0]
    out = run_optimization(forecast, price)
    assert 'schedule' in out and 'objective' in out
