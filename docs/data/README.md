# LTEE fitness data

`ltee-fitness.csv` is the `Concatenated.LTEE.data.all.csv` file from the
Wiser, Ribeck and Lenski Dryad record. The record identifies it as the
competition data for each population against the oppositely marked ancestor.
Dryad lists the dataset as reusable under CC0.

Run `python3 analysis/ltee_fit.py` from the repository root to regenerate
`docs/data/ltee-fitness-mean.csv`. The script averages available replicate fitness
values within each generation and includes bins with at least four values.
It fits `w(t) = 1 + a t^b` by least squares on those binned means. This is a
descriptive fit to empirical data. It is not a fit of the spatial Life World
simulator.

Source: Wiser, M. J., Ribeck, N. and Lenski, R. E. (2014), "Data from:
Long-term dynamics of adaptation in asexual populations",
[Dryad dataset](https://doi.org/10.5061/dryad.0hc2m).

The plotted bins are in `ltee-fitness-mean.csv`; the plot is generated as
`ltee-fitness.svg` by the same script. The plotted power law summarizes the
measurements and does not set Life World parameters.

The latest five-arm experiment set and its raw time series, means and Welch
contrasts are in [`experiments/`](experiments/README.md). These simulations
compare model outcomes with qualitative patterns reported in published work.
Their rates and time scales have no species calibration.
