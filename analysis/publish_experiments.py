#!/usr/bin/env python3
"""Package the latest replicated experiment runs for the research site."""

import csv
import math
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "out" / "exp"
DEST = ROOT / "docs" / "data" / "experiments"
EXPERIMENTS = {
    "range": (3000, ("local / global heterozygosity", "organisms")),
    "megaplate": (12000, ("mean resistance", "highest resistance")),
    "refuge": (20000, ("prey alive at end", "predators alive at end")),
    "phototaxis": (8000, ("mean position (128 = no bias)", "share in brightest quarter")),
    "networks": (20000, ("mean evolved neurons", "largest network")),
}


def t95(df):
    thresholds = ((1.5, 12.706), (2.5, 4.303), (3.5, 3.182), (4.5, 2.776),
                  (5.5, 2.571), (6.5, 2.447), (7.5, 2.365), (8.5, 2.306),
                  (9.5, 2.262), (11.0, 2.228), (13.5, 2.179), (17.5, 2.131),
                  (25.0, 2.086), (40.0, 2.042))
    for limit, value in thresholds:
        if df < limit:
            return value
    return 1.96


def summarize(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    half = t95(len(values) - 1) * math.sqrt(variance / len(values))
    return mean, mean - half, mean + half, variance / len(values)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    summary_rows = []
    comparison_rows = []
    for name, (ticks, outcome_names) in EXPERIMENTS.items():
        for ext in ("csv", "txt"):
            source = SOURCE / f"{name}.{ext}"
            if not source.is_file():
                raise SystemExit(f"Missing run output: {source}")
            shutil.copy2(source, DEST / source.name)

        grouped = {}
        with (SOURCE / f"{name}.csv").open(newline="") as stream:
            for row in csv.DictReader(stream):
                tick = int(row["tick"])
                if name == "refuge":
                    keep = tick == ticks
                else:
                    keep = tick * 4 >= ticks * 3
                if keep:
                    grouped.setdefault(row["arm"], {}).setdefault(int(row["rep"]), []).append(
                        (float(row["m1"]), float(row["m2"]))
                    )

        arm_values = {}
        for arm, replicates in grouped.items():
            arm_values[arm] = [
                tuple(sum(sample[k] for sample in samples) / len(samples) for k in range(2))
                for _, samples in sorted(replicates.items())
            ]
            for outcome in range(2):
                vals = [rep[outcome] for rep in arm_values[arm]]
                mean, lo, hi, variance = summarize(vals)
                summary_rows.append((name, outcome_names[outcome], arm, len(vals),
                                     f"{mean:.9f}", f"{lo:.9f}", f"{hi:.9f}"))

        treatment = next(iter(arm_values))
        for control in list(arm_values)[1:]:
            for outcome in range(2):
                a = [row[outcome] for row in arm_values[treatment]]
                b = [row[outcome] for row in arm_values[control]]
                ma, _, _, va = summarize(a)
                mb, _, _, vb = summarize(b)
                se2 = va + vb
                denominator = va * va / (len(a) - 1) + vb * vb / (len(b) - 1)
                df = (se2 * se2 / denominator) if denominator else 1000.0
                half = t95(df) * math.sqrt(se2)
                delta = ma - mb
                comparison_rows.append((name, outcome_names[outcome], treatment, control,
                                        len(a), f"{delta:.9f}", f"{delta-half:.9f}",
                                        f"{delta+half:.9f}"))

    with (DEST / "summary.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("experiment", "outcome", "arm", "replicates", "mean", "ci95_low", "ci95_high"))
        writer.writerows(summary_rows)
    with (DEST / "contrasts.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("experiment", "outcome", "treatment", "control", "replicates_per_arm", "difference", "welch_ci95_low", "welch_ci95_high"))
        writer.writerows(comparison_rows)
    print(f"Packaged {len(EXPERIMENTS)} experiments in {DEST.relative_to(ROOT)}")
    print(f"Summary rows: {len(summary_rows)}; treatment-control contrasts: {len(comparison_rows)}")


if __name__ == "__main__":
    main()
