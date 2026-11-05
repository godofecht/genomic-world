# Causal validation plan: phototaxis and evolved networks

Status: **implementation proposed; replicated revised results not yet obtained**.

This change does **not** convert the older negative results into positive results.
All plots and numeric tables generated before this patch refer to the original
forward-light-sensor and zero-neuron-cost model. Retain them as an archival
baseline, not as validation of this revision.

## Identified mechanisms

**Phototaxis.** The original input 6 was the intensity difference between a
forward-facing sample and the current cell, passed directly into a signed
turn output. That scalar is not left/right directional error, and founders
had no light-to-turn weight. A gradient can consequently change where cells
reproduce without causing directional swimming.

The revised input is `4 * daylight * (light_left - light_right)`, sampled at
the existing lateral sensing distance and gated by the physical eyespot and
`blind_light`. It excludes local food and detritus, which had contaminated
the original sensory measurement. The phototaxis preset now starts from an
explicit, inherited weight of +3 from input 6 to turning: left-brighter
turns left and right-brighter turns right. This is a **seeded reflex**.
Consequently, success here would demonstrate directional steering from the
implemented circuit, **not the evolution of phototaxis**.

**Evolved networks.** Previously, a growing genetic neuron list imposed no
explicit neuron-number metabolic cost. Inactive networks still underwent
mutation, making size growth a poor proxy for selection. Every expressed
evolved neuron now consumes `0.0005` energy per tick in **both** the active
and inert arms, regardless of its behavioural contribution. Inert networks
continue to be computed and inherited and are silenced only at their output.
This lets selection disfavour unhelpful complexity, but it does not
guarantee selection for additional neurons.

## Tests and replication

Run `./run.sh test` for the new `tests/test_causal_sensors.flow` assay.
The one-tick test places an organism facing north on a field growing brighter
to the east; it checks that the phototaxis genotype turns right relative to
the blinded control, that blinded-gradient and even-light controls coincide,
and that extra expressed neurons carry the expected energy charge.

Run `GW_REPS=12 ./run.sh experiment phototaxis` for the original longitudinal
population-level endpoint (mean x-coordinate) and brightest-quarter share,
with gradient, even light and blinded-gradient arms. Run
`GW_REPS=12 ./run.sh experiment networks` for network size and
`GW_REPS=12 ./run.sh experiment network-value` for mean living energy and
births per 1,000 organism-ticks. The network-value assay's birth rate is
cumulative from tick zero; it is not a controlled estimate of individual
lifetime reproductive success.

In all replicated experiments treatment and controls share seeds. The runner
now uses a 95% paired Student-t interval on within-seed differences, rather
than a Welch interval that treats each arm as independent. Individual-arm
intervals remain ordinary Student-t intervals. Analyses across multiple
endpoints are exploratory and are not adjusted for multiplicity.

For a **causal** phototaxis conclusion, the gradient arm must differ from
the blinded-gradient arm in a replicated endpoint, not only from even light.
The one-tick steering test is a mechanistic unit check, not an independent
demonstration of population-level taxis. A reversed-gradient intervention,
and an otherwise matched photoreceptor-knockout genotype, would strengthen
the next iteration.

For a **selection** conclusion, first compare active and inert neurons with
the same metabolic cost. A size difference is not proof of advantageous
complexity: additionally require evidence of higher reproduction or survival
and demonstrate inheritance and persistence over independent seeds. A
different mean energy among survivors is not itself sufficient, because
survivor composition can change.

## Sensitivity and limitations

Sweep neuron upkeep around 0, 0.00025, 0.0005 and 0.001 per tick, and founder
light-to-turn weight around 0, 1.5, 3 and 4 (the core decoder saturates at its
representable bound). Avoid selecting the best seed or tuning to a positive
result. Treat the settings in this branch as an explicit hypothesis, not
species-calibrated physical parameters.

Flow and the macOS-native viewer/compiler are not installed in the current
editing environment, so compilation and simulation results have **not** been
verified here. Do not copy numbers from the archived charts into new tables.

When the revised experiments have completed successfully, update
`docs/methods.html`, `README.md`, and plots using the new output CSVs and
record the revision commit, seeds, ticks, replicate count, effect estimates
and confidence intervals for each outcome.
