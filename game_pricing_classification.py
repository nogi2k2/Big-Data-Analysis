from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

spark = SparkSession.builder.appName("Game_Pricing_Classification").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

input_path = "hdfs://localhost:9000/steam_data/feature_engineered_steam.csv/"
df = spark.read.csv(input_path, header=True, inferSchema=True)

df = df.withColumn("is_free", when(col("price") == 0, 1).otherwise(0))
df = df.fillna({"average_playtime": 0, "positive_ratings": 0, "negative_ratings": 0, "sentiment_score": 0})

indexer = StringIndexer(inputCol="genres", outputCol="genre_index", handleInvalid="skip")
df = indexer.fit(df).transform(df)

feature_cols = ["genre_index", "average_playtime", "positive_ratings", "negative_ratings", "sentiment_score"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features", handleInvalid="skip")
df = assembler.transform(df)

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
train_df.cache()
test_df.cache()

lr = LogisticRegression(featuresCol="features", labelCol="is_free")
lr_model = lr.fit(train_df)

rf = RandomForestClassifier(featuresCol="features", labelCol="is_free", numTrees=10, maxBins=1554)
rf_model = rf.fit(train_df)

gbt = GBTClassifier(featuresCol="features", labelCol="is_free", maxIter=10, maxBins=1554)
gbt_model = gbt.fit(train_df)

lr_preds = lr_model.transform(test_df)
rf_preds = rf_model.transform(test_df)
gbt_preds = gbt_model.transform(test_df)

evaluator_accuracy = MulticlassClassificationEvaluator(labelCol="is_free", metricName="accuracy")
evaluator_f1 = MulticlassClassificationEvaluator(labelCol="is_free", metricName="f1")
evaluator_auroc = BinaryClassificationEvaluator(labelCol="is_free", metricName="areaUnderROC")

print("\nLogistic Regression Metrics:")
print("  Accuracy:", evaluator_accuracy.evaluate(lr_preds))
print("  F1 Score:", evaluator_f1.evaluate(lr_preds))
print("  AUROC:", evaluator_auroc.evaluate(lr_preds))

print("\nRandom Forest Metrics:")
print("  Accuracy:", evaluator_accuracy.evaluate(rf_preds))
print("  F1 Score:", evaluator_f1.evaluate(rf_preds))
print("  AUROC:", evaluator_auroc.evaluate(rf_preds))

print("\nGradient Boosting Metrics:")
print("  Accuracy:", evaluator_accuracy.evaluate(gbt_preds))
print("  F1 Score:", evaluator_f1.evaluate(gbt_preds))
print("  AUROC:", evaluator_auroc.evaluate(gbt_preds))

print("\nSample Predictions for Logistic Regression:")
lr_preds.select("name", "features", "is_free", "prediction", "probability").show(20, truncate=False)

print("\nSample Predictions for Random Forest:")
rf_preds.select("name", "features", "is_free", "prediction", "probability").show(20, truncate=False)

print("\nSample Predictions for Gradient Boosting:")
gbt_preds.select("name", "features", "is_free", "prediction", "probability").show(20, truncate=False)

spark.stop()
