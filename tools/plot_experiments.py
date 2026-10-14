#!/usr/bin/env python3
"""Charts for the replicated experiments.

Reads out/exp/NAME.csv (written by ./run.sh experiment NAME) and writes
docs/media/exp_NAME.svg: the first metric against time, one line per arm
(the mean over replicates) with a band from the lowest to the highest
replicate. Standard library only.

Usage: tools/plot_experiments.py NAME [NAME ...]
"""

import csv
import sys
from collections import defaultdict

LABELS = {
    "phototaxis": "Mean position along the slide (128 = no bias)",
    "refuge": "Prey alive",
    "networks": "Mean evolved neurons per organism",
    "range": "Local over global heterozygosity",
    "megaplate": "Mean resistance",
}
COLOURS = ["#f2c46e", "#6ec8ff", "#e058c8"]


def load(name):
    series = defaultdict(lambda: defaultdict(dict))
    arms = []
    with open(f"out/exp/{name}.csv") as f:
        for row in csv.DictReader(f):
            arm = row["arm"]
            if arm not in arms:
                arms.append(arm)
            series[arm][int(row["tick"])][int(row["rep"])] = float(row["m1"])
    return arms, series


def chart(name):
    arms, series = load(name)
    w, h = 720, 360
    left, right, top, bottom = 64, 16, 20, 56
    ticks = sorted({t for a in arms for t in series[a]})
    values = [v for a in arms for t in series[a] for v in series[a][t].values()]
    lo, hi = min(values + [0.0]), max(values)
    if hi <= lo:
        hi = lo + 1.0
    tmax = max(ticks)

    def sx(t):
        return left + (w - left - right) * t / tmax

    def sy(v):
        return top + (h - top - bottom) * (1.0 - (v - lo) / (hi - lo))

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'font-family="Inter, system-ui, sans-serif" font-size="12">',
           f'<rect width="{w}" height="{h}" fill="#12161b"/>']
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        y = sy(v)
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{w - right}" y2="{y:.1f}" stroke="#222830"/>')
        out.append(f'<text x="{left - 8}" y="{y + 4:.1f}" fill="#9a948a" text-anchor="end">{v:.3g}</text>')
    for k in range(5):
        t = tmax * k / 4
        out.append(f'<text x="{sx(t):.1f}" y="{h - bottom + 18}" fill="#9a948a" text-anchor="middle">{int(t)}</text>')
    out.append(f'<text x="{(left + w - right) / 2}" y="{h - 14}" fill="#9a948a" text-anchor="middle">tick</text>')
    out.append(f'<text x="{left}" y="{top - 6}" fill="#ece6da">{LABELS.get(name, name)}</text>')
    for i, arm in enumerate(arms):
        col = COLOURS[i % len(COLOURS)]
        ts = sorted(series[arm])
        upper = [(sx(t), sy(max(series[arm][t].values()))) for t in ts]
        lower = [(sx(t), sy(min(series[arm][t].values()))) for t in ts]
        band = " ".join(f"{x:.1f},{y:.1f}" for x, y in upper + lower[::-1])
        out.append(f'<polygon points="{band}" fill="{col}" fill-opacity="0.15"/>')
        line = " ".join(f"{sx(t):.1f},{sy(sum(series[arm][t].values()) / len(series[arm][t])):.1f}" for t in ts)
        out.append(f'<polyline points="{line}" fill="none" stroke="{col}" stroke-width="2"/>')
        out.append(f'<rect x="{left + 10 + i * 170}" y="{h - 38}" width="10" height="10" fill="{col}"/>')
        out.append(f'<text x="{left + 26 + i * 170}" y="{h - 29}" fill="#ece6da">{arm}</text>')
    out.append("</svg>")
    with open(f"docs/media/exp_{name}.svg", "w") as f:
        f.write("\n".join(out))
    print(f"docs/media/exp_{name}.svg")


if __name__ == "__main__":
    for name in sys.argv[1:]:
        chart(name)
