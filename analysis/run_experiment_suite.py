#!/usr/bin/env python3
"""Run and package the standard five-experiment FlowGenomics suite."""

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = ("range", "megaplate", "refuge", "phototaxis", "networks")


def main():
    env = os.environ.copy()
    env.pop("GW_TICKS", None)
    env["GW_REPS"] = "5"
    for name in NAMES:
        subprocess.run(["./run.sh", "experiment", name], cwd=ROOT, env=env, check=True)
    subprocess.run(["python3", "analysis/publish_experiments.py"], cwd=ROOT, env=env, check=True)


if __name__ == "__main__":
    main()
