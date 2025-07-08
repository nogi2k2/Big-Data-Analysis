#!/usr/bin/env python3
import sys

def main():
    current_genre = None 
    total_success_metric = 0.0 
    total_playtime = 0.0 
    total_ratings = 0.0 
    total_sales = 0.0 
    count = 0

    for line in sys.stdin:
        line = line.strip()
        try:
            genre, metrics = line.split("\t")
            success_metric, average_playtime, ratings, sales = map(float, metrics.split(",")) 
        except ValueError:
            continue

        if current_genre == genre: 
            total_success_metric += success_metric
            total_playtime += average_playtime
            total_ratings += ratings
            total_sales += sales
            count += 1
        else:
            if current_genre is not None:
                avg_success_metric = total_success_metric / count if count > 0 else 0
                avg_playtime = total_playtime / count if count > 0 else 0
                avg_ratings = total_ratings / count if count > 0 else 0
                avg_sales = total_sales / count if count > 0 else 0
                print(f"{current_genre}\t{avg_success_metric:.2f},{avg_playtime:.2f},{avg_ratings:.2f},{avg_sales:.2f}")

            current_genre = genre
            total_success_metric = success_metric
            total_playtime = average_playtime
            total_ratings = ratings
            total_sales = sales
            count = 1

    if current_genre:
        avg_success_metric = total_success_metric / count if count > 0 else 0
        avg_playtime = total_playtime / count if count > 0 else 0
        avg_ratings = total_ratings / count if count > 0 else 0
        avg_sales = total_sales / count if count > 0 else 0
        print(f"{current_genre}\t{avg_success_metric:.2f},{avg_playtime:.2f},{avg_ratings:.2f},{avg_sales:.2f}")

if __name__ == "__main__":
    main()
