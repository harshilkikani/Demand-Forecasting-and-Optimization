"""Bronze ingestion step.

Reads CSVs from the repository `data/` folder and writes a Bronze table in
Delta (if available) or Parquet. This script is intentionally simple so it
can run locally (no Databricks required) and demonstrates the medallion
architecture's first layer.

Usage:
	python -m src.bronze_ingest
	or import ingest_bronze from this module and call it programmatically.
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, col


def get_spark(app_name: str = "bronze_ingest") -> SparkSession:
	return SparkSession.builder.appName(app_name).getOrCreate()


def ingest_bronze(root_dir: str = None) -> str:
	"""Ingest raw CSVs into a bronze Delta/parquet dataset.

	Args:
		root_dir: repository root. Defaults to script parent (project root).

	Returns:
		path to the written bronze dataset.
	"""
	if root_dir is None:
		root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

	data_dir = os.path.join(root_dir, "data")
	bronze_dir = os.path.join(root_dir, "data", "bronze", "energy_dataset")
	os.makedirs(bronze_dir, exist_ok=True)

	spark = get_spark()

	energy_path = os.path.join(data_dir, "energy_data.csv")
	weather_path = os.path.join(data_dir, "weather_data.csv")

	energy = spark.read.csv(energy_path, header=True, inferSchema=True)
	weather = spark.read.csv(weather_path, header=True, inferSchema=True)

	# Basic normalization: ensure timestamp column exists and is proper type
	if "timestamp" in energy.columns:
		energy = energy.withColumn("timestamp", to_timestamp(col("timestamp")))

	# Join energy + weather as a simple enrichment example (left join)
	if "location" in energy.columns and "location" in weather.columns:
		df = energy.join(weather, on=["timestamp", "location"], how="left")
	else:
		# If join keys not present, just union columns where possible
		df = energy

	# Try to write as Delta if delta-spark is available, otherwise parquet
	try:
		df.write.format("delta").mode("overwrite").save(bronze_dir)
		out = bronze_dir
	except Exception:
		parquet_path = os.path.join(bronze_dir, "data.parquet")
		df.write.mode("overwrite").parquet(parquet_path)
		out = parquet_path

	# show a quick preview
	df.limit(5).show()
	spark.stop()
	return out


if __name__ == "__main__":
	print("Running bronze ingestion...")
	path = ingest_bronze()
	print(f"Wrote bronze dataset to: {path}")