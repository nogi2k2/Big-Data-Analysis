#!/usr/bin/env python3
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    header = next(reader, None)  

    if not header:
        return
    
    try:
        positive_idx = header.index("positive_ratings")
        negative_idx = header.index("negative_ratings")
        sentiment_idx = header.index("sentiment_score")
        success_idx = header.index("success_metric")
    except ValueError:
        print("Error: Required columns not found.", file=sys.stderr)
        return

    for row in reader:
        try:
            positive_ratings = float(row[positive_idx])
            negative_ratings = float(row[negative_idx])
            sentiment_score = float(row[sentiment_idx])
            success_metric = float(row[success_idx])

            print(f"data\t{positive_ratings},{negative_ratings},{sentiment_score},{success_metric}")
        except (ValueError, IndexError):
            continue  

if __name__ == "__main__":
    main()
