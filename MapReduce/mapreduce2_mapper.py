#!/usr/bin/env python3
import sys
import csv

VALID_GENRES = {
    "Action", "Adventure", "Casual", "Indie", "Massively Multiplayer",
    "Racing", "RPG", "Simulation", "Sports", "Strategy", "Early Access",
    "Violent", "Gore"
}

def main():
    reader = csv.reader(sys.stdin)
    header = next(reader, None)
    if not header:
        return  

    try:
        genres_idx = header.index("genres")
        success_metric_idx = header.index("success_metric")
        average_playtime_idx = header.index("average_playtime")
        ratings_idx = header.index("positive_ratings")
        sales_idx = header.index("price")  
    except ValueError:
        print("Error: Required columns not found in the header.", file=sys.stderr)
        return

    for row in reader:
        try:
            genres = row[genres_idx].split(";")  
            success_metric = float(row[success_metric_idx])
            average_playtime = float(row[average_playtime_idx])
            ratings = float(row[ratings_idx])
            sales = float(row[sales_idx])

            for genre in genres:
                genre = genre.strip()
                if genre in VALID_GENRES:  
                    print(f"{genre}\t{success_metric},{average_playtime},{ratings},{sales}")
        except (ValueError, IndexError):
            continue  

if __name__ == "__main__":
    main()
