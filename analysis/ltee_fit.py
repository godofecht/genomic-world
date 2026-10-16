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
PLOT = ROOT / "docs" / "data" / "ltee-fitness.svg"


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


def write_plot(points, scale, exponent):
    width, height = 760, 390
    left, right, top, bottom = 82, 24, 32, 68
    x0, x1 = math.log10(min(t for t, _, _ in points if t > 0)), math.log10(max(t for t, _, _ in points))
    y0, y1 = 0.98, max(mean for _, _, mean in points) + 0.035

    def xy(generation, fitness):
        x = left + (math.log10(generation) - x0) / (x1 - x0) * (width - left - right)
        y = height - bottom - (fitness - y0) / (y1 - y0) * (height - top - bottom)
        return x, y

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">LTEE relative fitness measurements and descriptive fit</title>',
             '<desc id="desc">Binned mean relative fitness from the E. coli Long-Term Evolution Experiment, with a fitted power law. The curve summarizes empirical measurements. Life World parameters remain uncalibrated to these data.</desc>',
             '<rect width="100%" height="100%" fill="#12161b"/>',
             '<g stroke="#39414a" stroke-width="1">']
    for fraction in (0, 0.25, 0.5, 0.75, 1):
        y = height - bottom - fraction * (height - top - bottom)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>')
    parts.append('</g><g fill="#b9b1a5" font-family="sans-serif" font-size="12">')
    for fraction in (0, 0.25, 0.5, 0.75, 1):
        val = y0 + fraction * (y1 - y0)
        y = height - bottom - fraction * (height - top - bottom)
        parts.append(f'<text x="{left-12}" y="{y+4:.1f}" text-anchor="end">{val:.2f}</text>')
    for generation in (500, 1000, 5000, 10000, 50000):
        x, _ = xy(generation, y0)
        parts.append(f'<text x="{x:.1f}" y="{height-bottom+23}" text-anchor="middle">{generation:,}</text>')
    parts.append(f'<text x="{(left+width-right)/2:.1f}" y="{height-10}" text-anchor="middle">Generations (log scale)</text>')
    parts.append(f'<text transform="translate(19 {(height-top-bottom)/2+top}) rotate(-90)" text-anchor="middle">Relative fitness</text></g>')
    path = []
    for i in range(161):
        generation = 500 * (50000 / 500) ** (i / 160)
        fitness = 1.0 + scale * generation**exponent
        x, y = xy(generation, fitness)
        path.append(f'{"M" if i == 0 else "L"}{x:.2f},{y:.2f}')
    parts.append(f'<path d="{" ".join(path)}" fill="none" stroke="#f2c46e" stroke-width="2.5"/>')
    for generation, count, mean in points:
        if generation > 0:
            x, y = xy(generation, mean)
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.4" fill="#8bc6a8"><title>{generation} generations, n={count}, mean={mean:.4f}</title></circle>')
    parts.extend(['<g font-family="sans-serif" font-size="12" fill="#ece6da">',
                  f'<circle cx="{left+8}" cy="18" r="4" fill="#8bc6a8"/><text x="{left+18}" y="22">Measured bin means</text>',
                  f'<line x1="{left+166}" y1="18" x2="{left+188}" y2="18" stroke="#f2c46e" stroke-width="2.5"/><text x="{left+196}" y="22">Descriptive power-law fit</text>',
                  '</g></svg>'])
    PLOT.write_text('\n'.join(parts) + '\n', encoding='utf-8')


def main():
    points = load_means()
    sse, exponent, scale = fit_power_law(points)
    write_plot(points, scale, exponent)
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
    print(f"plot: {PLOT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
