# Genomic World

An individual-based, spatially explicit eco-evolutionary simulator, written
in Flow. Tens of thousands of diploid organisms forage, breed and evolve on a
256 x 256 torus with a latitudinal temperature gradient. Each one carries a
phased, bit-packed genome of 128 loci on four chromosomes. Population
genetic statistics are computed live, and samples export as VCF.

![Genomic World](out/world.gif)

The GIF is produced by `./run.sh record` and is not committed.

## Run it

```
./run.sh              live window
./run.sh record 300   headless, writes out/world.gif
./run.sh bench        throughput, per-phase timing, population genetics
./run.sh test         tests, determinism check, validation against theory
./run.sh validate     validation against theory only
./run.sh export       run headless, write a VCF sample to out/
```

Requires Flow 2.0 (`flow` on the PATH) and a C11 compiler. With Homebrew
`libomp` installed, `run.sh` puts it on the compiler's search paths and the
parallel loops run on every core. Without it they compile serial and give the
same results.

## Keys

| Key | Action |
|---|---|
| 1 to 4 | View: ancestry, climate, food, deleterious alleles |
| P | Pause |
| [ and ] | Halve or double simulation steps per frame (1 to 16) |
| B | Open or close the mountain passes |
| W | Warm the climate by 0.3, or cool it back |
| M | Mutation rate: 1e-4, 5e-4, 2.5e-3 per locus per gamete |
| X | Bottleneck: kill 90 percent at random |
| E | Export a sample of 1000 to out/sample.vcf |
| R | New world from a new seed |

## Parameters

Set any of these in the environment; unset ones keep their defaults.

| Variable | Meaning | Default |
|---|---|---|
| GW_SEED | world seed | 20261013 |
| GW_MU | mutation rate per locus per gamete | 5e-4 |
| GW_DOM | dominance h of deleterious alleles | 0.25 |
| GW_SEL_MEAN | mean selection coefficient at deleterious loci | 0.03 |
| GW_MAP | map length per chromosome, Morgans | 1.0 |
| GW_ENV_SD | environmental SD, on the 0 to 1 trait scale | 0.1 |
| GW_THERMAL | strength of thermal selection | 0.05 |
| GW_MORTALITY | background death rate per tick | 0.003 |
| GW_PASSES | 1 open, 0 closed | 1 |
| GW_OUT | directory for exported files | out |
| GW_TICKS, GW_SAMPLE | export run length and sample size | 3000, 1000 |

```
GW_SEED=7 GW_PASSES=0 GW_OUT=out/closed ./run.sh export
```

Every parameter value is written into the VCF header.

## The model

### Genome

Diploid, four chromosomes, one biallelic locus per bit of a 32-bit word.
Haplotypes are phased: words 0 to 3 come from the maternal gamete, 4 to 7
from the paternal one.

| Chromosome | Bits 0 to 15 | Bits 16 to 31 |
|---|---|---|
| 0 | thermal optimum | speed |
| 1 | sensing radius | body size |
| 2 | breeding threshold | deleterious loci |
| 3 | 30 neutral marker loci, read as colour | |

Trait loci are additive. Each locus has its own effect size, drawn from an
exponential distribution and scaled so a trait's sixteen effects sum to one.
A few loci are large and most are small. The genotypic value is
`sum(effect * dosage) / 2` on a 0 to 1 scale. At birth each trait gets
independent environmental noise with SD `env_sd`, so heritability is below
one and can be measured.

Deleterious loci act on viability at birth. Each has its own selection
coefficient, exponential with mean 0.03, and a shared dominance h = 0.25.
Viability is multiplicative across loci: `(1 - h s)` per heterozygous locus
and `(1 - s)` per homozygous one. Mutation at these loci is forward-biased:
back mutation runs at a tenth of the forward rate.

Meiosis draws a Poisson number of crossovers per chromosome with mean equal
to the map length, at uniform gaps between loci, with no interference. That
is Haldane's model, and the recombination fraction between loci d Morgans
apart is `(1 - e^(-2d)) / 2`. Mutations per gamete are Poisson; loci are hit
uniformly.

### Ecology and life history

Food regrows in each cell toward a fertility set by value noise, faster in
the growing season. An agent samples food at its sensing radius in eight
directions, moves toward the best, eats from its cell, and pays per tick:

```
basal * size
+ sense_cost * radius
+ move_cost * size * speed^2          (if it moved)
+ thermal * size * (T - T_opt)^2      (Gaussian stabilising selection on T_opt)
```

Agents die when energy runs out, at age 400, or at a background rate of
0.003 per tick. They are simultaneous hermaphrodites that do not self. A
mature agent with energy above its genetic threshold picks a mate uniformly
from eligible agents in the surrounding 3 x 3 cells. The offspring gets one
gamete from each parent and survives viability selection.

### World and climate

Temperature depends on latitude: cold at the top and bottom rows, hot across
the middle. The climate is a Flow `flow` model in `sim/climate.flow`, so
the compiler integrates it with RK4. It has a 200-tick seasonal cycle and a
warming offset that relaxes toward a target over about 600 ticks.

Two mountain ridges split the torus into an inner and an outer region. Each
ridge has two passes at temperate latitudes. A flood fill of the terrain
labels the regions.

### Statistics computed live

| Statistic | Definition |
|---|---|
| allele frequency | every locus, whole population |
| F_ST | Hudson's estimator, inner vs outer region, 30 marker loci, ratio of sums (Bhatia et al. 2013) |
| marker heterozygosity | mean 2pq over marker loci |
| adaptation | Pearson r between thermal optimum and local temperature |
| h2 P-O | slope of offspring on mid-parent thermal phenotype |
| h2 Vg/Vp | Vg / (Vg + Ve) from genotypic values |
| generation time | mean parental age at birth |
| sigma | axial dispersal per generation, parent's birthplace to offspring's |
| Nb | Wright's neighbourhood size, 4 pi D sigma^2 |
| genetic load | 1 - mean viability |

## Validation

`validate.flow` runs the simulator's own meiosis, mutation and viability code
in a Wright-Fisher population (`sim/wf.flow`) and compares with theory. The
latest run, from `out/validation.tsv`:

| Case | Setting | Theory | Simulated | Tolerance |
|---|---|---|---|---|
| drift, H_t/H_0 = (1 - 1/2N)^t | N=100, t=50 | 0.778 | 0.782 | 0.04 |
| | t=100 | 0.606 | 0.605 | 0.04 |
| | t=200 | 0.367 | 0.372 | 0.04 |
| mutation-drift, 2pq = 4Nu/(1+8Nu) | N=200, u=5e-4 | 0.2222 | 0.2236 | 0.02 |
| mutation-selection, q = u/(hs) | s=0.1, h=0.5 | 0.0100 | 0.0103 | 15% |
| | s=0.1, h=0.25 | 0.0200 | 0.0193 | 15% |
| mutation-selection, q = sqrt(u/s) | s=0.1, h=0 | 0.0707 | 0.0694 | 15% |
| LD decay, D_t = D_0 (1-r)^t | 1 gap, t=10 | 0.1820 | 0.1808 | 0.01 |
| | 8 gaps, t=10 | 0.0263 | 0.0253 | 0.01 |
| selection, p' = p(1+s)/(1+ps) | s=0.05, gen 25 | 0.271 | 0.270 | 4 SE |
| | gen 50 | 0.557 | 0.551 | 4 SE |
| | gen 100 | 0.935 | 0.937 | 4 SE |
| fixation, 1/2N | N=100, neutral | 0.0050 | 0.0050 | 0.0035 |
| fixation, Kimura 1962 | N=100, s=0.02 | 0.0392 | 0.0382 | 0.009 |

Haldane's map function is checked directly in `tests/test_genome.flow`:
recombination fractions of 0.0304, 0.2016 and 0.4329 against 0.0312, 0.2016
and 0.4323.

Each check was confirmed able to fail. Giving heterozygotes the full
homozygote cost fails all three mutation-selection cases. Breaking the
crossover mask fails the gamete test. Removing thermal selection fails the
cline test.

## What a run shows

Seed 20261013, defaults, 3000 ticks (about 15 generations):

- Thermal optimum tracks latitude: r rises from 0.33 to 0.84.
- Sensing and body-size alleles fall, because both cost energy.
- h2 by parent-offspring regression is 0.93 against 0.86 from Vg/Vp. Mates
  are neighbours on a cline, so their phenotypes are correlated, and the
  regression overestimates.
- With the passes closed, F_ST between regions is 0.27 against 0.20 with
  them open (`tests/test_evolution.flow`, seed 777001, 1500 ticks).
- The deleterious burden climbs toward mutation-selection balance and rises
  with the mutation rate.

## Known gaps

These are limits of the model as it stands.

- 128 biallelic loci. There is no sequence, no infinite-sites mutation, and
  no tree-sequence recording, so coalescent and IBD analyses are out of
  reach. For those, SLiM with tskit is the standard tool.
- Parameters are scaled for speed. The mutation rate per locus, population
  size and ticks per generation are not calibrated to any species.
- Fitness for the five traits emerges from an energy budget with
  hand-set constants. Selection coefficients on those traits are not
  parameters and are not measured.
- No pleiotropy, epistasis, genotype-by-environment interaction, plasticity
  or maternal effects.
- Hermaphrodites without selfing. No separate sexes and no mate choice on
  phenotype.
- Deleterious alleles act on viability at birth only. Fecundity and adult
  survival are unaffected by them.
- The spatial model has no closed-form check of its own. Cline width against
  sigma / sqrt(s), and isolation by distance against 1 / Nb, are the
  natural next validations; the founding structure has to decay first.

## Performance

Measured with `./run.sh bench` on an Apple M4 Max (14 cores), macOS 26.2,
Flow 2.0.0 with the flowc C backend, Apple clang at `-O3`, libomp. 3000 ticks
from seed 20261013, about 49k agents at the end, one run each.

| | 14 threads | 1 thread |
|---|---|---|
| ticks per second | 793 | 153 |
| agent-ticks per second | 33.9 M | 6.5 M |
| frame (stats and render) | 1.4 ms | 6.7 ms |

- Agents are stored as structure of arrays; a genome is eight `u32` words.
- Every random draw comes from a hash of (agent seed, tick, purpose), so
  parallel loops need no shared generator and results are identical on any
  thread count. `run.sh test` checks this at 1 and 8 threads.
- Feeding runs in parallel over rows of cells using a counting-sort spatial
  index. Compaction is double-buffered: a serial pass assigns destinations,
  a parallel pass scatters, and the buffers swap.
- The window is drawn into one RGB buffer and blitted once per frame.

## Tests

`./run.sh test` runs:

- `tests/test_genome.flow`: popcount, gametes carry only parental alleles,
  no recombinants on a zero-length map, Haldane recombination fractions,
  Mendelian segregation, Poisson mutation count, forward-biased mutation,
  effect sizes, dominance and viability.
- `tests/test_world.flow`: the spatial index, food bounds, agents never on
  impassable terrain, the energy cap, order-preserving compaction, the
  climate model, no crossings over a closed ridge.
- `tests/test_evolution.flow`: a cline forms under thermal selection and not
  without it, closed passes raise F_ST, a higher mutation rate raises the
  burden.
- `tests/determinism.flow`: the same state hash at 1 and 8 threads.
- `validate.flow`: the theory checks above.

## Layout

```
genomic_world.flow     the windowed app
bench.flow             headless benchmark
validate.flow          genetic engine against theory
export_run.flow        headless run and VCF export
sim/config.flow        sizes and default constants
sim/params.flow        GW_ environment overrides
sim/state.flow         World and Agents records
sim/rng.flow           counter-based random numbers
sim/bits.flow          popcount and masks
sim/genome.flow        architecture, expression, meiosis, mutation
sim/wf.flow            Wright-Fisher harness for validation
sim/climate.flow       the Climate flow model
sim/world.flow         terrain, regions, temperature, food
sim/population.flow    founding, spatial index, compaction
sim/behaviour.flow     foraging, metabolism, feeding, mortality
sim/reproduction.flow  mate choice and offspring
sim/step.flow          the tick, phase by phase
sim/stats.flow         allele frequencies, F_ST, heritability, dispersal
sim/sampling.flow      VCF and TSV export
sim/textbuf.flow       text output buffer
sim/canvas.flow        framebuffer, text and numbers
sim/render.flow        views and the genetics panel
tests/                 self-checking tests
```
