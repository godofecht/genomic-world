# Genomic World

A genomic simulator for a 2D world, written in Flow. Tens of thousands of
diploid organisms forage, breed and evolve on a 256 x 256 torus. Each one
carries a bit-packed genome, and the population genetics are computed live.

![Genomic World](out/world.gif)

The GIF is produced by `./run.sh record` and is not committed.

## Run it

```
./run.sh              live window
./run.sh record 300   headless, writes out/world.gif
./run.sh bench        throughput and per-phase timing
./run.sh test         self-checking tests and a determinism check
```

Requires Flow 2.0 (`flow` on the PATH) and a C11 compiler. With Homebrew
`libomp` installed, `run.sh` puts it on the compiler's search paths and the
parallel loops run on every core. Without it they compile serial and give the
same results.

## Keys

| Key | Action |
|---|---|
| 1 to 4 | View: ancestry, climate, food, genetic load |
| P | Pause |
| [ and ] | Halve or double simulation steps per frame (1 to 16) |
| B | Open or close the mountain passes |
| W | Warm the climate by 0.3, or cool it back |
| M | Mutation rate: 1e-4, 5e-4, 2.5e-3 per locus per gamete |
| X | Bottleneck: kill 90 percent at random |
| R | New world from a new seed |

## The model

### Genome

Four chromosomes, diploid. One chromosome is one 32-bit word with one
biallelic locus per bit, so a genome is eight words.

| Chromosome | Bits 0 to 15 | Bits 16 to 31 |
|---|---|---|
| 0 | thermal optimum | speed |
| 1 | sensing radius | body size |
| 2 | breeding threshold | housekeeping loci |
| 3 | 30 neutral marker loci, read as colour | |

A trait is the dosage of allele 1 over its sixteen loci on both homologs, 0
to 32, scaled into the trait's range. Housekeeping loci carry recessive
deleterious alleles. Each locus homozygous for one raises the basal cost by
30 percent, and a child homozygous at four or more is not viable.

Meiosis takes one chromosome at a time. It picks a starting homolog, then
with probability 0.5 crosses over at a uniform breakpoint. The gamete word is
`(first & mask) | (second & ~mask)`. Mutations per gamete are drawn from a
Poisson distribution and flip uniform loci. Loci that share a chromosome are
linked: adjacent loci separate in 1.6 percent of gametes, opposite ends in 50
percent (measured in `tests/test_genome.flow`).

### Ecology

Food regrows in each cell toward a fertility set by value noise, faster in
the growing season. An agent samples food at its sensing radius in eight
directions, moves toward the best, eats from its cell, and pays per tick:

```
basal * size * (1 + 0.3 * load)
+ sense_cost * radius
+ move_cost * size * speed^2          (if it moved)
+ thermal_cost * size * (T - T_opt)^2
```

Mature agents with energy above their genetic threshold breed with a mate in
the surrounding 3 x 3 cells. Each parent contributes one gamete.

### World and climate

Temperature depends on latitude: cold at the top and bottom rows, hot across
the middle. The climate is a Flow `flow` model in `sim/climate.flow`, so
the compiler integrates it with RK4. It has a 200-tick seasonal cycle and a
warming offset that relaxes toward a target over about 600 ticks.

Two mountain ridges split the torus into an inner and an outer region. Each
ridge has two passes at temperate latitudes. A flood fill of the terrain
labels the regions, and F_ST is computed between them.

### What you can watch

- A thermal cline forms: the correlation between thermal optimum and local
  temperature rises from about 0.2 to 0.9 within 2000 ticks.
- Sensing and body-size alleles fall, because both cost energy.
- Closing the passes stops gene flow and F_ST stays higher than with them
  open.
- Warming pushes the equator past the hottest reachable genotype, which is
  a range limit set by the genetic architecture.
- The burden of deleterious alleles settles at mutation-selection balance,
  and rises with the mutation rate.

## Performance

Measured with `./run.sh bench` on an Apple M4 Max (14 cores), macOS 26.2,
Flow 2.0.0 with the flowc C backend, Apple clang at `-O3`, libomp. 3000 ticks
from seed 20261013, population 34k to 62k, one run each.

| | 14 threads | 1 thread |
|---|---|---|
| ticks per second | 948 | 182 |
| agent-ticks per second | 43.6 M | 8.4 M |
| frame (stats and render, 51k agents) | 1.3 ms | 6.5 ms |

What makes it fast:

- Agents are stored as structure of arrays. A genome is eight `u32` words.
  Trait expression is a masked popcount and meiosis is a mask, a shift and an
  XOR.
- Every random draw comes from a hash of (agent seed, tick, purpose), so the
  movement loop runs in parallel with no shared generator. Results are
  identical on any thread count. `run.sh test` checks this by hashing the
  full state at 1 and 8 threads.
- Feeding runs in parallel over rows of cells, using a counting-sort spatial
  index rebuilt every tick. Each cell's food is touched by one thread only.
- Compaction is double-buffered. A serial pass assigns each survivor its
  destination slot, a parallel pass scatters every column into the back
  buffer, and the buffers swap. This took compaction from 65 percent of the
  tick to 33 percent and doubled throughput.
- Allele counting runs in parallel over loci, so each thread owns its
  counters.
- The whole window is drawn into one RGB buffer and blitted once per frame.

## Tests

`./run.sh test` runs:

- `tests/test_genome.flow`: popcount, gametes carry only parental alleles,
  no recombinants without crossover, recombinant fraction, Mendelian
  segregation, linkage, Poisson mutation count, the phenotype map, load.
- `tests/test_world.flow`: the spatial index, food bounds, agents never on
  impassable terrain, the energy cap, order-preserving compaction, the
  climate model, and no crossings over a closed ridge.
- `tests/test_evolution.flow`: a cline forms under thermal selection and
  does not form without it, closed passes give higher F_ST than open ones,
  and a higher mutation rate gives a higher burden.
- `tests/determinism.flow`: the same state hash at 1 and 8 threads.

Each test was checked against an injected bug. Breaking the crossover mask
fails test 3 of the genome suite. Removing the thermal cost fails test 1 of
the evolution suite.

## Layout

```
genomic_world.flow    the windowed app
bench.flow            headless benchmark
sim/config.flow       sizes and model constants
sim/state.flow        World and Agents records
sim/rng.flow          counter-based random numbers
sim/bits.flow         popcount and masks
sim/genome.flow       locus map, expression, meiosis, mutation
sim/climate.flow      the Climate flow model
sim/world.flow        terrain, regions, temperature, food
sim/population.flow   founding, spatial index, compaction
sim/behaviour.flow    foraging, metabolism, feeding
sim/reproduction.flow mate search and offspring
sim/step.flow         the tick, phase by phase
sim/stats.flow        allele frequencies, F_ST, cline, history
sim/canvas.flow       framebuffer, text and numbers
sim/render.flow       views and the genetics panel
tests/                self-checking tests
```
