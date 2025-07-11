from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors

spark = SparkSession.builder.appName("Success Metric Optimization").getOrCreate()
input_path = "hdfs://localhost:9000/steam_data/feature_engineered_steam.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)
features = ["positive_ratings", "average_playtime", "owners_numeric"]
target = "success_metric"
df = df.dropna(subset=features + [target])
assembler = VectorAssembler(inputCols=features, outputCol="features")
df = assembler.transform(df).select(col("features"), col(target).alias("label"))
lr = LinearRegression(featuresCol="features", labelCol="label")
lr_model = lr.fit(df) 
coefficients = lr_model.coefficients.toArray()
normalized_weights = coefficients / coefficients.sum() 
print("Optimized Success Metric Weights:")
for i, feature in enumerate(features):
    print(f"{feature}: {normalized_weights[i]:.4f}")
spark.stop()