from pyspark.sql import SparkSession
from pyspark.sql.functions import trim, col, when

spark = SparkSession.builder.appName("Data Cleaning for steam.csv").master('local[*]').getOrCreate()

input_path = "hdfs://localhost:9000/steam_data/steam.csv"
output_path = "hdfs://localhost:9000/steam_data/cleaned_steam.csv"

try:
    print(f"Processing file: steam.csv")

    df = spark.read.csv(input_path, header=True, inferSchema=True)

    if "steam_appid" in df.columns:
        df = df.withColumnRenamed("steam_appid", "app_id")
    if "appid" in df.columns:
        df = df.withColumnRenamed("appid", "app_id")

    cleaned_df = df.dropDuplicates()

    cleaned_df = cleaned_df.select([trim(col(c)).alias(c) if c != "price" else col(c) for c in cleaned_df.columns])

    if 'price' in cleaned_df.columns:
        cleaned_df = cleaned_df.withColumn(
            "price",
            when(trim(col("price")) == "", None).otherwise(trim(col("price")).cast("float"))
        )

    numeric_columns = ["positive_ratings", "negative_ratings", "average_playtime", "median_playtime", "price"]
    for col_name in numeric_columns:
        if col_name in cleaned_df.columns:
            cleaned_df = cleaned_df.withColumn(col_name, col(col_name).cast("float"))

    cleaned_df = cleaned_df.dropna(how='all')

    critical_columns = [col for col in ['app_id', 'name'] if col in cleaned_df.columns]
    cleaned_df = cleaned_df.dropna(subset=critical_columns)

    cleaned_df.write.option("header", "true").csv(output_path, mode="overwrite")
    print(f"Saved cleaned file to: {output_path}")

except Exception as e:
    import logging
    logging.error(f"Error processing file steam.csv: {e}")

print("Data cleaning for steam.csv completed successfully.")
spark.stop()
