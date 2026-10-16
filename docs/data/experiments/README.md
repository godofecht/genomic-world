# Replicated experiment runs

These files package five runs from 2026-10-16. Each arm used the same seed values within its experiment: 20261014, 20268933, 20276852, 20284771 and 20292690. The model reports outcomes across the last quarter of each run, except predator and prey counts, which are taken at the final tick. Confidence intervals use the same Student t and Welch calculations as the Flow experiment runner.

| Experiment | Ticks | Run series | Simulator summary | Command |
|---|---:|---|---|---|
| Range expansion | 3,000 | [CSV](range.csv) | [TXT](range.txt) | `./run.sh experiment range` |
| MEGA-plate | 12,000 | [CSV](megaplate.csv) | [TXT](megaplate.txt) | `./run.sh experiment megaplate` |
| Predator and prey refuge | 20,000 | [CSV](refuge.csv) | [TXT](refuge.txt) | `./run.sh experiment refuge` |
| Phototaxis | 8,000 | [CSV](phototaxis.csv) | [TXT](phototaxis.txt) | `./run.sh experiment phototaxis` |
| Evolved networks | 20,000 | [CSV](networks.csv) | [TXT](networks.txt) | `./run.sh experiment networks` |

Run the complete standard set with `./run.sh experiment-suite`. It runs the five commands above in sequence and rebuilds these packaged files.

Each CSV contains the recorded run series. Each TXT contains the simulator summary. `summary.csv` contains arm means and 95% intervals. `contrasts.csv` contains treatment-control differences and Welch intervals. Run `python3 analysis/publish_experiments.py` after running the five commands to regenerate the packaged files and summary tables.

These runs are model experiments. Their parameters and ticks are not fitted to a species. The comparisons to Hallatschek et al. (2007), Baym et al. (2016), and Gause (1934) concern reported qualitative patterns. The browser and research models do not share all organism, rate, or environmental details with those studies.
