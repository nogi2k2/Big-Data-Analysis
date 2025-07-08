#!/usr/bin/env python3
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    header = next(reader, None)

    if not header:
        return

    try:
        price_tier_idx = header.index("price_tier")
        success_metric_idx = header.index("success_metric")
    except ValueError:
        print("Error: Required columns not found in the header.", file=sys.stderr)
        return

    for row in reader:
        try:
            price_tier = row[price_tier_idx].strip()
            success_metric = float(row[success_metric_idx])

            if not price_tier or price_tier == '0':
                continue

            print(f"{price_tier}\t{success_metric}")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()


