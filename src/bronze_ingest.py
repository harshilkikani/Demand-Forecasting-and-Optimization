from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

energy_data = spark.read.csv('energy_data.csv', header = True)

weather_data = spark.read.csv('weather_data.csv', header = True)