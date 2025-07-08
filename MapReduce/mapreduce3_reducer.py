#!/usr/bin/env python3
import sys
from math import sqrt

def calculate_correlation(n, sum_x, sum_y, sum_xy, sum_x2, sum_y2): 
    numerator = n * sum_xy - sum_x * sum_y
    denominator = sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    return numerator / denominator if denominator != 0 else 0

def main():
    n = 0
    sum_pos = sum_neg = sum_sent = sum_succ = 0
    sum_pos_sq = sum_neg_sq = sum_sent_sq = sum_succ_sq = 0 
    sum_pos_succ = sum_neg_succ = sum_sent_succ = 0 

    for line in sys.stdin:
        line = line.strip()
        try:
            _, data = line.split("\t")
            positive_ratings, negative_ratings, sentiment_score, success_metric = map(float, data.split(","))
        except ValueError:
            continue

        n += 1
        sum_pos += positive_ratings
        sum_neg += negative_ratings
        sum_sent += sentiment_score
        sum_succ += success_metric

        sum_pos_sq += positive_ratings**2
        sum_neg_sq += negative_ratings**2
        sum_sent_sq += sentiment_score**2
        sum_succ_sq += success_metric**2

        sum_pos_succ += positive_ratings * success_metric
        sum_neg_succ += negative_ratings * success_metric
        sum_sent_succ += sentiment_score * success_metric

    corr_pos_succ = calculate_correlation(n, sum_pos, sum_succ, sum_pos_succ, sum_pos_sq, sum_succ_sq)
    corr_neg_succ = calculate_correlation(n, sum_neg, sum_succ, sum_neg_succ, sum_neg_sq, sum_succ_sq)
    corr_sent_succ = calculate_correlation(n, sum_sent, sum_succ, sum_sent_succ, sum_sent_sq, sum_succ_sq)

    print(f"Correlation between Positive Ratings and Success: {corr_pos_succ:.2f}")
    print(f"Correlation between Negative Ratings and Success: {corr_neg_succ:.2f}")
    print(f"Correlation between Sentiment Score and Success: {corr_sent_succ:.2f}")

if __name__ == "__main__":
    main()
