#!/usr/bin/env python3
"""Fit a descriptive power law to the archived LTEE competition data.

This analysis summarizes the published fitness measurements. It does not
calibrate the spatial Life World simulator.
"""

import csv
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "data" / "ltee-fitness.csv"
SUMMARY = ROOT / "docs" / "data" / "ltee-fitness-mean.csv"


def load_means():
    measurements = defaultdict(list)
    with SOURCE.open(newline="") as source:
        for row in csv.DictReader(source):
            try:
                generation = int(row["Generation"])
                fitness = float(row["Fitness"])
            except (TypeError, ValueError):
                continue
            if generation >= 0 and math.isfinite(fitness) and fitness > 0:
                measurements[generation].append(fitness)

    return [
        (generation, len(values), sum(values) / len(values))
        for generation, values in sorted(measurements.items())
        if len(values) >= 4
    ]


def fit_power_law(points):
    positive = [(t, mean - 1.0) for t, _, mean in points if t > 0]
    best = None
    for step in range(5001):
        exponent = 0.05 + step * 0.0002
        powers = [t**exponent for t, _ in positive]
        effects = [effect for _, effect in positive]
        scale = sum(x * y for x, y in zip(powers, effects)) / sum(
            x * x for x in powers
        )
        sse = sum((y - scale * x) ** 2 for x, y in zip(powers, effects))
        if best is None or sse < best[0]:
            best = (sse, exponent, scale)
    return best


def main():
    points = load_means()
    sse, exponent, scale = fit_power_law(points)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY.open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["generation", "replicates", "mean_relative_fitness"])
        writer.writerows((t, n, f"{mean:.9f}") for t, n, mean in points)

    rmse = math.sqrt(sse / sum(1 for t, _, _ in points if t > 0))
    print(f"mean points: {len(points)}")
    print(f"generation range: {points[0][0]} to {points[-1][0]}")
    print(f"fit: relative_fitness = 1 + {scale:.9g} * generation^{exponent:.4f}")
    print(f"in-sample RMSE: {rmse:.5f}")
    print(f"summary: {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
