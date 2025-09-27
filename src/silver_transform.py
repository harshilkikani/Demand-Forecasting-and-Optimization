"""Silver transform: cleans bronze data and prepares a time-series table."""
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg


def get_spark(app_name: str = "silver_transform") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()


def transform_bronze(bronze_path: str, out_dir: str = None) -> str:
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(bronze_path), "..", "silver")
    os.makedirs(out_dir, exist_ok=True)

    spark = get_spark()
    try:
        df = spark.read.format("delta").load(bronze_path)
    except Exception:
        df = spark.read.parquet(bronze_path)

    # basic cleaning: drop nulls and aggregate hourly if needed
    cleaned = df.dropna()

    # if there are numeric features, compute hourly averages as example
    numeric_cols = [c for c, t in cleaned.dtypes if t in ("int", "double", "float")]
    if numeric_cols:
        agg = cleaned.groupBy("timestamp").agg(*[avg(c).alias(c) for c in numeric_cols])
    else:
        agg = cleaned

    out_path = os.path.join(out_dir, "energy_silver.parquet")
    agg.write.mode("overwrite").parquet(out_path)
    spark.stop()
    return out_path


if __name__ == "__main__":
    print("Transforming bronze to silver (local run)")