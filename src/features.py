"""Feature engineering: reads silver data and produces training features."""
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, dayofweek


def get_spark(app_name: str = "features") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()


def build_features(silver_path: str, out_path: str = None) -> str:
    if out_path is None:
        out_path = os.path.join(os.path.dirname(silver_path), "features.parquet")

    spark = get_spark()
    df = spark.read.parquet(silver_path)

    # example features: hour of day, day of week
    if "timestamp" in df.columns:
        df_feat = df.withColumn("hour", hour("timestamp")).withColumn("dow", dayofweek("timestamp"))
    else:
        df_feat = df

    df_feat.write.mode("overwrite").parquet(out_path)
    spark.stop()
    return out_path


if __name__ == "__main__":
    print("Building features...")