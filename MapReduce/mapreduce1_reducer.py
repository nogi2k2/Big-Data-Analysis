#!/usr/bin/env python3
import sys

def main():
    current_tier = None
    current_sum = 0.0 
    current_count = 0 

    for line in sys.stdin:
        line = line.strip()
        try:
            price_tier, success_metric = line.split("\t")
            success_metric = float(success_metric)
            if success_metric == float('inf') or success_metric < 0:
                continue
        except ValueError:
            continue

        if current_tier == price_tier:
            current_sum += success_metric
            current_count += 1
        else:
            if current_tier is not None and current_count > 0: 
                avg_success_metric = current_sum / current_count 
                print(f"{current_tier}\t{avg_success_metric:.2f}") 
            current_tier = price_tier
            current_sum = success_metric
            current_count = 1

    if current_tier is not None and current_count > 0:
        avg_success_metric = current_sum / current_count
        print(f"{current_tier}\t{avg_success_metric:.2f}")

if __name__ == "__main__":
    main()

