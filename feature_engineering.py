from pyspark.sql import SparkSession
from pyspark.sql.functions import col, size, split, when, udf, explode
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.linalg import Vectors, VectorUDT

spark = SparkSession.builder.appName("Feature Engineering").getOrCreate()

input_path = "hdfs://localhost:9000/steam_data/cleaned_steam.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

unique_genres = (
    df.select(explode(split(col("genres"), ";")).alias("genre"))
    .distinct()
    .rdd.flatMap(lambda x: x)
    .collect()
)

for genre in unique_genres:
    df = df.withColumn(f'is_{genre.replace(" ", "_")}', when(col("genres").contains(genre), 1).otherwise(0))

df = df.withColumn(
    'price_tier',
    when(col('price') == 0, 'Free')
    .when((col('price') > 0) & (col('price') <= 10), 'Low')
    .when((col('price') > 10) & (col('price') <= 30), 'Medium')
    .otherwise('High')
)

to_vector = udf(lambda x: Vectors.dense([float(x)]) if x is not None else Vectors.dense([0.0]), VectorUDT())
df = df.withColumn("price_vec", to_vector("price"))
scaler = MinMaxScaler(inputCol="price_vec", outputCol="price_scaled")
scaler_model = scaler.fit(df)
df = scaler_model.transform(df).drop("price_vec")

df = df.withColumn("total_ratings", col("positive_ratings") + col("negative_ratings"))
df = df.withColumn(
    "sentiment_score",
    when(col("total_ratings") > 0, col("positive_ratings") / col("total_ratings")).otherwise(None)
)
df = df.withColumn("has_achievements", when(col("achievements") > 0, 1).otherwise(0))

def owners_to_numeric(owners):
    if owners is None:
        return 0
    try:
        ranges = owners.split("-")
        return (int(ranges[0].replace(",", "")) + int(ranges[1].replace(",", ""))) // 2
    except Exception:
        return 0

owners_to_numeric_udf = udf(owners_to_numeric)
df = df.withColumn("owners_numeric", owners_to_numeric_udf(col("owners")))

df = df.withColumn(
    "success_metric",
    (col("positive_ratings") * 0.5 + col("average_playtime") * 0.3 + col("owners_numeric") * 0.2)
)

unsupported_columns = [field.name for field in df.schema.fields if isinstance(field.dataType, (VectorUDT))]
df = df.drop(*unsupported_columns)

output_path = "hdfs://localhost:9000/steam_data/feature_engineered_steam.csv"
df.write.option("header", "true").csv(output_path, mode="overwrite")

print(f"Feature engineering completed. Data saved to: {output_path}")
spark.stop()
