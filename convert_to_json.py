import json

with open("MapReduce/mapreduce1_output.txt", "r") as file:
    data = []
    for line in file:
        try:
            key, value = line.strip().split("\t")
            value = float(value)
            data.append({
                "key": key,
                "value": value
            })
        except ValueError:
            print(f"Skipping malformed line: {line.strip()}")

with open("MapReduce/mapreduce1_output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file for MapReduce1 successfully created.")

import json

with open("MapReduce/mapreduce2_output.txt", "r") as file:
    data = []
    for line in file:
        try:
            genre, metrics = line.strip().split("\t")
            success_metric, average_playtime, positive_ratings, negative_ratings = map(float, metrics.split(","))
            data.append({
                "genre": genre,
                "success_metric": success_metric,
                "average_playtime": average_playtime,
                "positive_ratings": positive_ratings,
                "negative_ratings": negative_ratings
            })
        except ValueError:
            print(f"Skipping malformed line (incorrect number of metrics): {line.strip()}")

with open("MapReduce/mapreduce2_output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file for MapReduce2 successfully created.")

with open("MapReduce/mapreduce3_output.txt", "r") as file:
    data = {}
    for line in file:
        try:
            parts = line.strip().split(":")
            metric_description = parts[0].strip()
            correlation_value = float(parts[1].strip())
            data[metric_description] = correlation_value
        except (ValueError, IndexError):
            print(f"Skipping malformed line: {line.strip()}")

with open("MapReduce/mapreduce3_output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file for MapReduce3 successfully created.")
