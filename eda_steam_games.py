from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, count, split, explode, when, desc

spark = SparkSession.builder.appName("Steam Game EDA").getOrCreate()

input_path = "hdfs://localhost:9000/steam_data/feature_engineered_steam.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

print("Schema:")
df.printSchema()

print(f"Total rows: {df.count()}, Total columns: {len(df.columns)}")

df_filtered = df.filter(col("genres").isNotNull() & (col("genres") != "") & (col("genres") != "0"))

df_filtered = df_filtered.withColumn("genre_array", split(col("genres"), ";"))
exploded_df = df_filtered.withColumn("genre", explode(col("genre_array")))

print("Top Genres by Success Metric:")
exploded_df.groupBy("genre").agg(mean("success_metric").alias("avg_success")) \
    .orderBy(desc("avg_success")).show(10, truncate=False)

print("Genres with the Highest Average Play Time:")
exploded_df.groupBy("genre").agg(mean("average_playtime").alias("avg_playtime")) \
    .orderBy(desc("avg_playtime")).show(10, truncate=False)

print("Correlation between Price and Success Metric:")
price_success_corr = df.stat.corr("price", "success_metric")
print(f"Correlation: {price_success_corr}")

print("Pricing Tiers and Success Metric:")
df.withColumn("price_tier", when(col("price") == 0, "Free")
              .when(col("price") <= 10, "Low")
              .when((col("price") > 10) & (col("price") <= 30), "Medium")
              .otherwise("High")) \
    .groupBy("price_tier").agg(mean("success_metric").alias("avg_success"),
                               count("*").alias("game_count")) \
    .orderBy(desc("avg_success")).show(truncate=False)

print("Sentiment Score vs Success Metric:")
df.groupBy("sentiment_score").agg(mean("success_metric").alias("avg_success")) \
    .orderBy(desc("avg_success")).show(10)

print("Positive Ratings vs Success Metric Correlation:")
positive_success_corr = df.stat.corr("positive_ratings", "success_metric")
print(f"Correlation: {positive_success_corr}")

print("Price Range vs Average Playtime:")
df.withColumn("price_range", when(col("price") < 10, "<10")
              .when((col("price") >= 10) & (col("price") < 30), "10-30")
              .otherwise("30+")) \
    .groupBy("price_range").agg(mean("average_playtime").alias("avg_playtime")) \
    .orderBy(desc("avg_playtime")).show(truncate=False)
