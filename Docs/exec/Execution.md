# Pipeline Execution Guide

This guide provides step-by-step instructions for executing the Steam Games data analysis pipeline

## Prerequisites

Ensure that Hadoop, Spark, and MongoDB are properly installed and configured on your system
[Setup Instructions](../setup/Setup.md)

## Step-by-Step Execution

### 1. Format Namenode (First Time Only)

```bash
hdfs namenode -format
```

### 2. Start Hadoop DFS Daemon

```bash
start-dfs.sh
```

Verify that processes are running:
```bash
jps
```

### 3. SSH into Localhost

Hadoop pseudo-distributed mode requires SSH access to localhost for proper daemon management and file access

```bash
ssh localhost
```

### 4. Start Spark (Optional)

Starting Spark provides access to the Spark UI for monitoring active processes, but it's optional since the PySpark scripts manage their own Spark sessions

```bash
start-master.sh
start-worker.sh spark://$(hostname -f):7077 # Can visit spark master UI @ http://localhost:8080
```

This starts both the Spark master and worker for local parallel execution

### 5. Upload Dataset to HDFS

```bash
hdfs dfs -mkdir /steam_data
hdfs dfs -put <path_to_steam_csv_data> /steam_data
```

### 6. Run Spark Scripts

Execute the following scripts in order:

```bash
spark-submit data_cleaning.py
spark-submit feature_engineering.py
spark-submit eda_steam_games.py
spark-submit game_pricing_classification.py
spark-submit success_metrics_weights.py
```

### 7. Execute MapReduce Jobs

After `feature_engineering.py` completes (producing `feature_engineered_steam.csv`), run the MapReduce jobs

> **Note:** Due to shell formatting issues with line endings and whitespace, either type commands manually or format as single-line commands when copy-pasting.

#### Job 1: Game Ratings Analysis
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
  -input /steam_data/feature_engineered_steam.csv \
  -output /output1 \
  -mapper "python3 MapReduce/mapreduce1_mapper.py" \
  -reducer "python3 MapReduce/mapreduce1_reducer.py" \
  -file "MapReduce/mapreduce1_mapper.py" \
  -file "MapReduce/mapreduce1_reducer.py"
```

#### Job 2: Genre Statistics
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
  -input /steam_data/feature_engineered_steam.csv \
  -output /output2 \
  -mapper "python3 MapReduce/mapreduce2_mapper.py" \
  -reducer "python3 MapReduce/mapreduce2_reducer.py" \
  -file "MapReduce/mapreduce2_mapper.py" \
  -file "MapReduce/mapreduce2_reducer.py"
```

#### Job 3: Sentiment Correlation
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
  -input /steam_data/feature_engineered_steam.csv \
  -output /output3 \
  -mapper "python3 MapReduce/mapreduce3_mapper.py" \
  -reducer "python3 MapReduce/mapreduce3_reducer.py" \
  -file "MapReduce/mapreduce3_mapper.py" \
  -file "MapReduce/mapreduce3_reducer.py"
```

### 8. Download MapReduce Outputs

```bash
hdfs dfs -get /output1/part-00000 MapReduce/mapreduce1_output.txt
hdfs dfs -get /output2/part-00000 MapReduce/mapreduce2_output.txt
hdfs dfs -get /output3/part-00000 MapReduce/mapreduce3_output.txt
```

### 9. Convert Outputs to JSON (Optional)

For MongoDB storage and querying:

```bash
python convert_to_json.py
```

**Outputs:**
- `mapreduce1_output.json`
- `mapreduce2_output.json`
- `mapreduce3_output.json`

### 10. Import Data to MongoDB

```bash
mongoimport --db steam_games --collection game_ratings --file mapreduce1_output.json --jsonArray
mongoimport --db steam_games --collection genre_stats --file mapreduce2_output.json --jsonArray
mongoimport --db steam_games --collection sentiment_corr --file MapReduce/mapreduce3_output.json
```

**Note:** The third file contains a single JSON object and cannot be imported as a JSON array.

### 11. Query Data in MongoDB

Launch the MongoDB shell:
```bash
mongosh
```

#### Example Queries:

**A. View game ratings:**
```javascript
db.game_ratings.find().pretty()
```

**B. Sort by best performing tier:**
```javascript
db.game_ratings.find().sort({ value: -1 })
```

**C. View genre statistics:**
```javascript
db.genre_stats.find().pretty()
```

**D. View sentiment correlation:**
```javascript
db.sentiment_corr.findOne()
```

## Troubleshooting

- Ensure all services (Hadoop, Spark, MongoDB) are running before execution
- Verify HDFS is accessible and has sufficient storage space
- Check that all Python scripts and MapReduce files are in the correct directories
- Confirm that the dataset path is correct 