# Genomic World

Life World and the Genomic World: organisms that grow from their genomes and evolve, written in Flow.

**Try it in your browser:** [Open the live demo](https://godofecht.github.io/genomic-world/), then go to the [interactive models](https://godofecht.github.io/genomic-world/demos.html).

![The Life World open ocean seen from above. Chains of round cells in red, blue, green and pink swim through dark blue water. A gold circle marks one followed predator, a fan of pink and red cells. A panel on the left shows that predator's body, energy bar and brain wiring. A panel on the right shows the community make-up, energy intake and the commonest body forms.](docs/media/ocean_zoom.jpg)

## What this is

This repository holds two evolution simulators. Both are written in [Flow](https://github.com/flooooooooooow/flow), a programming language made by the same author. Flow code is compiled to C and then to a native program.

The Genomic World is a population genetics simulator. Tens of thousands of diploid organisms (each carries two copies of every chromosome, one from each parent) look for food, breed and evolve on a square map that wraps round at the edges. The map is cold at the top and bottom and hot in the middle. Each organism has a genome of 128 genes on four chromosomes, and the program measures how gene frequencies change as it runs.

The Life World runs on the same genetic engine. Here each organism grows a body from its genome, cell by cell, and has a small brain that is also coded in its genes. You watch an ocean or a lab dish fill with creatures that graze, hunt, mate and die, and their family lines evolve.

The project website also has four small browser models. They are separate, simpler programs written in JavaScript, made for exploring one idea each.

## What you can learn from it

Biology:

- Natural selection. Organisms whose temperature preference matches where they live keep more energy and leave more offspring, so a gradient in gene frequency (a cline) forms from north to south.
- Genotype and phenotype. Each trait is the sum of many small gene effects plus random environmental noise, so the trait you see is not fixed by the genes alone.
- Meiosis and crossing over. Each parent passes on one gamete (sex cell) made by mixing its two chromosome copies.
- Mutation, dominance and harmful alleles. An allele is one version of a gene. Harmful alleles that are partly recessive stay in the population at a low level.
- Genetic drift and bottlenecks. Chance alone changes gene frequencies, most of all in small populations. Press **X** in the Genomic World to kill 90 percent of the population at random.
- Isolation and gene flow. Mountain ridges split the world. Closing the passes stops organisms crossing, and the two halves become more genetically different.
- Predator and prey numbers, after Gause's experiments with protists in the 1930s.
- How bacteria evolve antibiotic resistance, after the MEGA-plate experiment.

Statistics:

- Correlation, regression and confidence intervals. The experiments run five times with different random seeds and report a mean and a 95 percent confidence interval.
- Comparing a treatment group with a control group, and checking whether the difference could be zero.

Computer Science:

- Simulating a large population fast: parallel loops, and random numbers that give the same result on any number of processor cores.
- Testing a simulation against mathematical theory.

## Run it

### In your browser

1. [Open the interactive models page](https://godofecht.github.io/genomic-world/demos.html).
2. Each of the four models has sliders and buttons. Move a slider, then press the run button and watch the graph.

The four models:

- **Can a population track a warming world?** Sliders: **Warming**, **Migration**, **Selection strength**. Buttons: **Run 100 generations**, **Reset**.
- **Does a refuge change the outcome?** Sliders: **Prey protected by refuge**, **Prey growth rate**. Buttons: **Run 600 steps**, **Reset**.
- **How does drift carve a growing frontier?** Sliders: **Parent neighborhood**, **Founder count**. Buttons: **Grow colony**, **Reset**.
- **How do selection and drift change allele frequency?** Sliders: **Starting allele frequency**, **Selection coefficient**, **Diploid population size**, **Generations**. Buttons: **Run simulation**, **Reset**.

The home page of the site shows a video of the Life World and links to the experiment write-ups.

### On your own computer

**You will need:**

- A Mac. The windowed programs draw with macOS frameworks (Core Animation and CoreText). The author ran everything on macOS 26.2. Other systems have not been tested.
- Flow 2.0, with the `flow` command on your PATH. The [Flow repository](https://github.com/flooooooooooow/flow) gives install steps, including Homebrew.
- A C11 compiler. On a Mac, Apple's clang comes with the Xcode Command Line Tools.
- Optional: `libomp` from [Homebrew](https://brew.sh) so the simulation runs on every core. Without it the results are the same, only slower.
- Optional: [ffmpeg](https://ffmpeg.org) for `./run.sh life-video`, and Python 3 for the scripts in `analysis/`.

Steps:

1. Download the code.

   ```bash
   git clone https://github.com/godofecht/genomic-world.git
   cd genomic-world
   ```

2. Open the Genomic World in a window.

   ```bash
   ./run.sh
   ```

   A map of the world appears, coloured by ancestry, with a panel of genetics statistics.

3. Open the Life World, full screen.

   ```bash
   ./run.sh life
   ```

   Press **Tab** to choose a world and **H** to list every key.

4. Run the tests and the checks against theory.

   ```bash
   ./run.sh test
   ```

   Each test file prints its results. The script exits with an error if any test fails or if one thread and eight threads give different results.

Other commands:

```text
./run.sh record 300   headless, writes out/world.gif
./run.sh bench        throughput, per-phase timing, population genetics
./run.sh validate     validation against theory only
./run.sh export       run headless, write a VCF sample to out/
./run.sh equilibrium  calibrate, solve the attractors, compare cold and warm starts
./run.sh life-bench   headless life world: forms, trophic roles, energy, selection
./run.sh shot         headless renders of the life world (settings in life_shot.flow)
./run.sh life-video N N frames rendered headless, to out/life.mp4
./run.sh experiment NAME   one replicated, controlled experiment, to out/exp/
./run.sh experiment-suite  all five experiments, packaged in docs/data/experiments/
```

"Headless" means the program runs without opening a window. The experiment names are `phototaxis`, `refuge`, `networks`, `range` and `megaplate`.

#### Genomic World controls

| Key | Action |
|---|---|
| 1 to 4 | View: ancestry, climate, food, deleterious alleles |
| P | Pause |
| [ and ] | Halve or double simulation steps per frame (1 to 16) |
| B | Open or close the mountain passes |
| W | Warm the climate by 0.3, or cool it back |
| M | Mutation rate: 1e-4, 5e-4, 2.5e-3 per locus per gamete |
| X | Bottleneck: kill 90 percent at random |
| A | Re-found the population on the mean-field attractor |
| E | Export a sample of 1000 to out/sample.vcf |
| R | New world from a new seed |

#### Life World controls

When the world menu is open (press **Tab**):

| Key | Action |
|---|---|
| Up and Down arrows | Choose a world |
| M | Change how organisms are built: body plan, morphology or combined |
| D | 2D or 3D bodies |
| Return | Start the chosen world |
| Tab or Esc | Close the menu |

While a world is running:

| Key or mouse | Action |
|---|---|
| Space or P | Pause |
| [ and ] | Fewer or more ticks per frame (1 to 64) |
| Arrow keys | Pan |
| Mouse wheel | Zoom |
| Drag | Pan |
| Right-drag | Turn the camera, in the 3D view |
| Click | Follow an organism |
| H | Show or hide the list of keys |
| I | Hide or show the panels |
| 3 | 2D or 3D view |
| V | Pixels, natural, bright-field or dark-field |
| F | Show the flow |
| G | Quality: fast, balanced or full resolution |
| O | Open or close the ocean's passes |
| W | Warm or cool the climate |
| R | Same world, new seed |
| Z | Whole world in view |
| Return | Full screen on or off |
| Esc | Close help, stop following, leave full screen, then quit |
| Q | Quit |

## How it works

Every organism carries its genome as eight 32-bit numbers. Each bit is one gene with two possible alleles, 0 or 1. Words 0 to 3 are the chromosomes from the mother and words 4 to 7 those from the father. Some genes set traits such as speed, body size and preferred temperature. Some are harmful mutations. Thirty are neutral markers that only set the organism's colour, so you can see family lines spread.

Each tick (one step of the simulation) every organism senses food, moves, eats and pays an energy cost. Being big, fast or far from your preferred temperature costs more. Organisms die when their energy runs out, when they get old, or by chance. When two neighbours have enough energy they breed. The child gets one gamete from each parent, made by the same meiosis code, with crossing over and new mutations. Nothing in the code says which traits should win. Selection comes only from who survives and breeds.

The Life World adds development. Part of the genome is a short program of cell-identity genes. A body grows from one cell, round by round, and each gene says whether a cell grows a neighbour and what kind. Genes can be duplicated or deleted, so new body parts can appear over time.

| File or folder | What is in it |
|---|---|
| `run.sh` | Every build and run command |
| `genomic_world.flow` | The Genomic World window and its keys |
| `life_world.flow` | The Life World window and its keys |
| `sim/config.flow` | World size and default constants |
| `sim/genome.flow` | Genes, meiosis and mutation |
| `sim/behaviour.flow` | Foraging, energy costs and death |
| `sim/reproduction.flow` | Choosing a mate and making offspring |
| `sim/stats.flow` | Allele frequencies, F_ST and heritability |
| `life/` | The Life World: genomes, body growth, brains, habitats |
| `viz/` | Drawing the worlds on screen |
| `tests/` | Self-checking tests |
| `validate.flow` | Checks of the genetic engine against theory |
| `docs/` | The project website, including the browser models in `docs/demos.js` |
| `analysis/` | Python scripts for the experiment tables and the E. coli fitness data |

## Ideas to try

1. Change a browser model. In `docs/demos.js`, the Wright-Fisher model draws 20 replicate lines (`length: 20`). Change that number, and the `/20` in the readout text below it. Open `docs/demos.html` in your browser to see the result.
2. Change a setting without editing code. The Genomic World reads settings from environment variables (values set in the terminal before a command). Run a world with the passes closed and a higher mutation rate, then press **4** to see the harmful alleles.

   ```bash
   GW_PASSES=0 GW_MU=2.5e-3 ./run.sh
   ```

3. Make life more expensive. In `sim/config.flow`, raise `MOVE_COST` or `BASAL_COST`. Watch whether speed and body size evolve to be smaller.
4. Change the age limit. In `sim/config.flow`, change `MAX_AGE` and `MATURE_AGE`, then watch the **GEN TICKS** reading (generation time in ticks) in the statistics panel.
5. Build a new lab experiment. Read how the presets are set up in `life/habitat.flow`, copy one, and change its light, food or antibiotic layout.
6. Test a claim. Pick an experiment in `life_experiment.flow`, run it with `./run.sh experiment NAME`, and check whether the treatment and control intervals overlap.

## Technical details

The rest of this README is the original technical description, kept in full.

### Overview

An individual-based, spatially explicit eco-evolutionary simulator, written in Flow. Tens of thousands of diploid organisms forage, breed and evolve on a 256 x 256 torus with a latitudinal temperature gradient. Each one carries a phased, bit-packed genome of 128 loci on four chromosomes. Population genetic statistics are computed live, and samples export as VCF (Variant Call Format, the standard text file for genetic variants).

Requires Flow 2.0 (`flow` on the PATH) and a C11 compiler. With Homebrew `libomp` installed, `run.sh` puts it on the compiler's search paths and the parallel loops run on every core. Without it they compile serial and give the same results.

### Parameters

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

```bash
GW_SEED=7 GW_PASSES=0 GW_OUT=out/closed ./run.sh export
```

Every parameter value is written into the VCF header.

### The model

#### Genome

Diploid, four chromosomes, one biallelic locus per bit of a 32-bit word. Haplotypes are phased: words 0 to 3 come from the maternal gamete, 4 to 7 from the paternal one.

| Chromosome | Bits 0 to 15 | Bits 16 to 31 |
|---|---|---|
| 0 | thermal optimum | speed |
| 1 | sensing radius | body size |
| 2 | breeding threshold | deleterious loci |
| 3 | 30 neutral marker loci, read as colour | |

Trait loci are additive. Each locus has its own effect size, drawn from an exponential distribution and scaled so a trait's sixteen effects sum to one. A few loci are large and most are small. The genotypic value is `sum(effect * dosage) / 2` on a 0 to 1 scale. At birth each trait gets independent environmental noise with SD `env_sd`, so heritability is below one and can be measured.

Deleterious loci act on viability at birth. Each has its own selection coefficient, exponential with mean 0.03, and a shared dominance h = 0.25. Viability is multiplicative across loci: `(1 - h s)` per heterozygous locus and `(1 - s)` per homozygous one. Mutation at these loci is forward-biased: back mutation runs at a tenth of the forward rate.

Meiosis draws a Poisson number of crossovers per chromosome with mean equal to the map length, at uniform gaps between loci, with no interference. That is Haldane's model, and the recombination fraction between loci d Morgans apart is `(1 - e^(-2d)) / 2`. Mutations per gamete are Poisson; loci are hit uniformly.

#### Ecology and life history

Food regrows in each cell toward a fertility set by value noise, faster in the growing season. An agent samples food at its sensing radius in eight directions, moves toward the best, eats from its cell, and pays per tick:

```text
basal * size
+ sense_cost * radius
+ move_cost * size * speed^2          (if it moved)
+ thermal * size * (T - T_opt)^2      (Gaussian stabilising selection on T_opt)
```

Agents die when energy runs out, at age 400, or at a background rate of 0.003 per tick. They are simultaneous hermaphrodites that do not self. A mature agent with energy above its genetic threshold picks a mate uniformly from eligible agents in the surrounding 3 x 3 cells. The offspring gets one gamete from each parent and survives viability selection.

#### World and climate

Temperature depends on latitude: cold at the top and bottom rows, hot across the middle. The climate is a Flow `flow` model in `sim/climate.flow`, so the compiler integrates it with RK4. It has a 200-tick seasonal cycle and a warming offset that relaxes toward a target over about 600 ticks.

Two mountain ridges split the torus into an inner and an outer region. Each ridge has two passes at temperate latitudes. A flood fill of the terrain labels the regions.

#### Statistics computed live

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

### Validation

`validate.flow` runs the simulator's own meiosis, mutation and viability code in a Wright-Fisher population (`sim/wf.flow`) and compares with theory. The latest run, from `out/validation.tsv`:

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

Haldane's map function is checked directly in `tests/test_genome.flow`: recombination fractions of 0.0304, 0.2016 and 0.4329 against 0.0312, 0.2016 and 0.4323.

Each check was confirmed able to fail. Giving heterozygotes the full homozygote cost fails all three mutation-selection cases. Breaking the crossover mask fails the gamete test. Removing thermal selection fails the cline test.

### What a run shows

Seed 20261013, defaults, 3000 ticks (about 15 generations):

- Thermal optimum tracks latitude: r rises from 0.33 to 0.84.
- Sensing and body-size alleles fall, because both cost energy.
- h2 by parent-offspring regression is 0.93 against 0.86 from Vg/Vp. Mates are neighbours on a cline, so their phenotypes are correlated, and the regression overestimates.
- With the passes closed, F_ST between regions is 0.27 against 0.20 with them open (`tests/test_evolution.flow`, seed 777001, 1500 ticks).
- The deleterious burden climbs toward mutation-selection balance and rises with the mutation rate.

### Attractors and warm start

The patterns the agents produce relax toward fixed points of deterministic mean-field models. `sim/meanfield.flow` writes those models down, integrates them to their attractors, and `sim/warmstart.flow` founds the agents there.

Mutation-selection balance at each deleterious locus is a Flow evolution model (`flow Purge`, one instance per locus):

```text
q evolves as u (1 - q) - v q - s q (1 - q) (h + (1 - 2h) q) / wbar
```

Its attractor matches the fixed point of the exact discrete recursion at all 16 loci (`tests/test_meanfield.flow`). It needs no calibration.

The thermal cline is a reaction-diffusion system for the 16 thermal loci across 64 latitude bands: Gaussian stabilising selection toward local temperature, Nagylaki's dispersal term with the measured density gradient, mutation, and quasi-linkage-equilibrium disequilibrium `D_ij = sigma2 p_i' p_j' / r_ij` (Barton 1983). Dispersal is solved implicitly with a cyclic tridiagonal solve, so it converges in about 5800 steps of one generation. Selection width and dispersal are measured from the agents (`sim/calibrate.flow`): lifetime reproductive success against phenotype mismatch at the birthplace gives omega2 = 0.040 at defaults, a clean Gaussian surface over 1.8 million deaths.

Results from `./run.sh equilibrium` (seed 20261013, defaults, 40000 ticks per run, about 180 generations):

| | Cold start | Warm start | Attractor |
|---|---|---|---|
| deleterious alleles per genome, tick 0 | 0.00 | 3.40 | 3.40 |
| at tick 20000 | 0.99 | 3.36 | 3.40 |
| at tick 40000 | 1.52 | 3.39 | 3.40 |
| Purge transient from q = 0, tick 40000 | 1.63 predicted | | |
| cline RMS from attractor, tick 0 | 0.39 | 0.003 | 0 |
| cline RMS from attractor, tick 40000 | 0.061 | 0.060 | 0 |

- A cold start needs about 931 generations (about 203,000 ticks, roughly 9 minutes at this run's speed) to reach 90 percent of the balance burden. The Purge models predict that transient: 0.33 against 0.35 observed at tick 5000, 1.03 against 0.99 at tick 20000. Solving the attractor takes 0.5 ms, and the warm start holds within 2 percent of it.
- The cline attractor with linkage disequilibrium sits 0.038 RMS from the agents' cline at the time it was calibrated; the linkage-equilibrium version sits 0.070 away. The agents carry 1.2 to 3.4 times the linkage-equilibrium genetic variance where the cline is steepest.
- The cline attractor moves. Speed, size and sensing keep evolving under the energy budget for hundreds of generations, so selection strengthens (omega2 0.040 at tick 8000, 0.028 at tick 36000) and dispersal falls (sigma2 401 to 354). Recalibrated at tick 36000, the attractor again sits 0.041 RMS from the agents. A warm start therefore skips the first 1500 to 4000 ticks of cline formation. The slow ecological drift after that still has to be simulated.

### Life world

`./run.sh life` opens a second world on the same genetic engine, full screen at the panel's native resolution. Organisms grow bodies from their genomes, sense, decide, eat, fight, mate and die, and their lineages evolve. Tab chooses the world and how organisms are built; H lists every key.

#### Genome and development

Each organism is diploid. Its genome has two parts.

- A fixed part: 640 loci per haplotype on twenty chromosomes. Morphology and physiology (size, elongation, lobes, pigment, pattern, flagella, cilia, spines, membrane, chlorophyll, toxin resistance, cytostome, eyespot, lipid, raptorial organelles, developmental rounds), a brain of 72 weights, a thermal optimum, a breeding threshold and neutral colour markers. These recombine by the genomic world's meiosis (Haldane's map).
- A developmental program: a list of cell-identity genes, two words each. A gene says what type of cell an identity is, how long it keeps growing, and for each direction whether it grows a neighbour and which identity that neighbour takes. Programs cross over at most once per meiosis; sometimes the crossover is misaligned by one gene, which duplicates or deletes a gene, as unequal crossing-over does. Point mutations, duplications and deletions add to this. The number of identities, and so of distinct cell kinds and organs, is not fixed.

A body grows from one cell, round by round, in 2D (four directions) or 3D (six), and the upper half is mirrored so every body is bilaterally symmetric. A gene that grows its own identity repeats a segment; a timer stops it. Only the scratch grid bounds a body (31 cells each way in 2D, 15 in 3D); in tests random programs grow bodies of up to 8,965 cells. Energetics bound them long before that.

Of two alleles at a program gene, each field takes the larger value (growing is dominant over not growing). Mates must have developmental signatures within 10 bits of each other, so forms that diverge stop interbreeding.

#### Three ways to build an organism

- Body plan: cells of eight types do everything. Mouths graze, motors swim, eyes see (ahead on the midline, to the sides off it), armour and spikes fight, stores hold energy, photosynthetic cells make it from light. Each cell type has a fixed look.
- Morphology: one cell, built as a protist is. Size and shape set mass and drag; flagella and cilia swim; a cytostome grazes; raptorial organelles hunt, as Didinium's do; spines and a thick membrane defend; chlorophyll photosynthesises and greens the cell; an eyespot sees, as Euglena's stigma does; lipid stores energy. The cell is drawn from the same genes: outline, nucleus, chloroplasts, droplets, beating flagella, cilia in metachronal waves, spines.
- Combined: the multicellular body of the first mode, with each cell made better or worse at its job (factor 0.5 to 1.5) by the morphological genes, at a running cost, and sized and tinted by them.

Bodies can be 2D or 3D in any multicellular mode. 3D bodies swim in the same plane; their frontal area sets their drag.

#### Behaviour

Each brain has two parts, both genetic.

- A fixed core: ten inputs, four hidden neurons that feed back on themselves, two outputs, 72 weights. Inputs: food ahead and to each side, the nearest prey and threat, the nearest possible mate, its own energy, the light gradient along its heading, the current across its body (a lateral line), and a bias. Outputs are turning and thrust.
- An evolved network on top of it: a third gene list in the genome, one gene per neuron. A neuron gene sets its activation (tanh, logistic, a clipped rectifier, or sine, which feeding itself makes a rhythm generator), a bias, a self-connection, three incoming connections (from senses, the core's hidden neurons or other evolved neurons, by index modulo the network's size) and its pull on turning and thrust. Neurons are added by an insertion mutation that starts nearly silent, as NEAT adds nodes, and are duplicated, deleted and rewired like any gene list; misaligned crossing-over adds or drops them too. Evolved neurons update together from the senses, the core's new state and their own last values, so loops among them carry information forward.

The founders have no evolved neurons and a silent hidden core, so anything a network does has evolved. Networks do grow: in a 30,000-tick ocean run the mean reached 11.6 neurons and the largest 18. A controlled experiment (below) shows that in Gause's dish this growth is mutation pressure: networks that evolve but drive nothing grow as large as active ones. No selection for larger networks is detectable there.

#### Ecology

- Grazing on algae (the food field), which regrows toward the water's fertility.
- Photosynthesis: light from the sun or a lamp, shared among the photosynthetic cells of one grid cell beyond six of them, and drawing on the cell's nutrient, so autotrophs compete with the algae and each other.
- Detritus: every death leaves its biomass where it fell. Mouths scavenge it; bacteria (implicit) return it to the water as nutrient.
- Predation: attack against defence, within a reach that grows with body size. Spikes cut grazing efficiency, so predators depend on prey.
- Reproduction: sexual in the ocean; in the lab, cells divide, with occasional sex in protist presets, as Paramecium conjugates.
- Toxin: where there is antibiotic, energy drains unless resistance covers it; resistance costs upkeep.

#### Habitats and experiments

| Preset | Setting | After |
|---|---|---|
| Open ocean | gyres around ridges and passes, drifting upwelling, day and night, seasons | the original life world |
| Petri dish | liquid culture under a lamp, gently stirred | |
| Range expansion | two neutral strains spread from a drop on agar; nutrients diffuse | Hallatschek, Hersen, Ramanathan and Nelson (2007), PNAS 104: 19926 |
| Predator and prey | a predator and its prey in a small dish | Gause (1934), The Struggle for Existence |
| Predator and prey with a refuge | sediment at one side where prey cannot be caught | Gause (1934) |
| MEGA-plate | a long agar plate, antibiotic in bands rising to the middle | Baym, Lieberman, Chase, Gross and Kishony (2016), Science 353: 1147 |
| Phototaxis | a slide lit from one end, poor medium, green swimmers with eyespots | |
| Serial transfer | a tenth moves to fresh medium every 600 ticks | Lenski, Rose, Simpson and Tadler (1991), American Naturalist 138: 1315 |

These are simplified versions. What they show is measured below.

#### Evidence: replicated, controlled experiments

`./run.sh experiment NAME` runs treatment and control arms from the same five seeds and writes every time series to `out/exp/NAME.csv`, and reports each outcome over the last quarter of the run as a mean with a 95 percent confidence interval, and the difference between arms with a 95 percent Welch interval. Run the complete set with `./run.sh experiment-suite`; it packages the results in `docs/data/experiments/` for the project page.

| Experiment | Outcome | Treatment | Control | Difference (95% CI) | Reading |
|---|---|---|---|---|---|
| Range expansion, agar against stirred liquid | local over global heterozygosity | 0.058 | 0.935 | -0.877 (-0.929 to -0.825) | Strains segregate at an expanding front by drift and stay mixed in liquid, as Hallatschek et al. found |
| MEGA-plate, drug against no drug | mean resistance | 0.387 | 0.003 | 0.384 (0.368 to 0.399) | Resistance evolves only under the drug; every drug replicate reached the top band (highest resistance 0.875 against 0.228) |
| Predator and prey, no refuge against refuge | prey alive at the end | 44 | 2,224 | -2,180 (-2,405 to -1,955) | Prey counts are higher with the refuge across five runs |
| Phototaxis, gradient against even light | mean position (128 = no bias) | 158.5 | 128.3 | 30.2 (15.3 to 45.0) | Cells gather toward the lamp |
| Phototaxis, gradient against blinded light sense | mean position | 158.5 | 160.3 | -1.8 (-19.4 to 15.8) | Gathering does not need the sense: within 8,000 ticks it comes from growth where light is strong; steering adds nothing measurable |
| Networks, active against inert | mean evolved neurons | 2.87 | 3.95 | -1.09 (-3.02 to 0.85) | The interval includes zero; these runs give no evidence that active networks grew larger |

Two earlier single-run statements did not survive these controls and have been withdrawn: that cells steer toward the light, and that larger networks were being selected. An earlier refuge experiment used a predator that could graze when prey ran out (`out/exp/refuge_facultative.txt`, a local output file that is not in the repository). The founding predator now has no cytostome, matching Didinium's prey-specific feeding role.

The packaged runs, with raw time series, means and Welch contrasts, are in [docs/data/experiments/](docs/data/experiments/README.md).

#### Viewing

The window opens full screen at the panel's native resolution. The world is drawn by a software renderer in Flow (`viz/`) and shown through two Core Animation layers (`viz/display.flow`): the world, which on a large panel is drawn at half resolution with the water at a quarter and scaled by the GPU, and the overlay, drawn at full resolution with CoreText type.

- Pixels, the default: each world cell takes its colour straight from the simulation's grids (algae, detritus, flow, terrain), and each body cell is a square of its type's colour where the developmental program put it; single cells are rasterised from their morphological genes. Drawn at half size and scaled by the GPU with nearest filtering; a full-screen frame takes about 12 ms.
- 2D view, smooth styles: water shaded from the world's fields (algae, detritus, vorticity, caustics, relief lit from the upper left, shore foam), marine snow carried by the currents, organisms, and effects for births, kills and deaths. At night organisms glow.
- 3D view: the camera orbits; the ground is ray-marched over the terrain height field, so ridges and vessel rims stand up; every body cell is a lit sphere in a depth buffer.
- Styles: natural colour, bright-field (pale field, translucent cells, as under a microscope), dark-field (black field, cells lit at the edges).
- The inspector shows a followed organism: portrait, life, energy, its brain with live activity (the core, and every evolved neuron with its wiring, activation and current value), and its developmental program gene by gene, or in morphology mode its trait values.
- The panel shows the commonest forms and the rarest: forms held by the fewest organisms, the most complex first among equals.

Every life-world run gives the same state hash on 1 and 8 threads, in each of the three modes (`run.sh test`).

### E. coli fitness reference data

`docs/data/ltee-fitness.csv` is competition fitness data from the Long-Term Evolution Experiment (LTEE) with E. coli, from Wiser, Ribeck and Lenski (2014) on Dryad. `python3 analysis/ltee_fit.py` bins it by generation and fits `w(t) = 1 + a t^b`. This is a descriptive fit to empirical data. It does not set Life World parameters. See [docs/data/README.md](docs/data/README.md).

### Performance

Measured with `./run.sh bench` on an Apple M4 Max (14 cores), macOS 26.2, Flow 2.0.0 with the flowc C backend, Apple clang at `-O3`, libomp. 3000 ticks from seed 20261013, about 49k agents at the end, one run each.

| | 14 threads | 1 thread |
|---|---|---|
| ticks per second | 793 | 153 |
| agent-ticks per second | 33.9 M | 6.5 M |
| frame (stats and render) | 1.4 ms | 6.7 ms |

- Agents are stored as structure of arrays; a genome is eight `u32` words.
- Every random draw comes from a hash of (agent seed, tick, purpose), so parallel loops need no shared generator and results are identical on any thread count. `run.sh test` checks this at 1 and 8 threads.
- Feeding runs in parallel over rows of cells using a counting-sort spatial index. Compaction is double-buffered: a serial pass assigns destinations, a parallel pass scatters, and the buffers swap.
- The window is drawn into one RGB buffer and blitted once per frame.

### Tests

`./run.sh test` runs:

- `tests/test_genome.flow`: popcount, gametes carry only parental alleles, no recombinants on a zero-length map, Haldane recombination fractions, Mendelian segregation, Poisson mutation count, forward-biased mutation, effect sizes, dominance and viability.
- `tests/test_world.flow`: the spatial index, food bounds, agents never on impassable terrain, the energy cap, order-preserving compaction, the climate model, no crossings over a closed ridge.
- `tests/test_evolution.flow`: a cline forms under thermal selection and not without it, closed passes raise F_ST, a higher mutation rate raises the burden.
- `tests/test_meanfield.flow`: the cyclic solver, Purge attractors against the discrete recursion, local adaptation without dispersal, a flat cline under fast dispersal.
- `tests/test_fluid.flow`: the linear steady state cell by cell, the projection removing at least 90 percent of the divergence, wall cells at rest, and 2000 steps at full forcing staying finite and bounded.
- `tests/test_life.flow`: the founders' body; random programs grow bilaterally symmetric bodies in 2D and 3D, unchanged by swapping homologs; gametes carry only parental alleles and parental program genes; unequal crossing-over, duplication and deletion change program length both ways; morphological genes act on function; short runs in each mode keep the cell arena packed and every organism alive and embodied.
- `tests/determinism.flow`: the same state hash at 1 and 8 threads.
- `tests/life_determinism.flow`: the same, for the ocean in body-plan mode, Gause's dish in morphology mode, and a petri dish of 3D combined bodies.
- `validate.flow`: the theory checks above.

### Layout

```text
genomic_world.flow     the windowed app
bench.flow             headless benchmark
validate.flow          genetic engine against theory
export_run.flow        headless run and VCF export
equilibrium.flow       attractors against cold and warm starts
life_world.flow        the life world app, full screen
life_bench.flow        headless life world
life_shot.flow         headless renders and frame sequences
life_experiment.flow   replicated, controlled experiments
sim/config.flow        sizes and default constants
sim/params.flow        GW_ environment overrides
sim/state.flow         World and Agents records
sim/rng.flow           counter-based random numbers
sim/bits.flow          popcount and masks
sim/genome.flow        architecture, expression, meiosis, mutation
sim/wf.flow            Wright-Fisher harness for validation
sim/meanfield.flow     attractors: Purge flow model, reaction-diffusion cline
sim/calibrate.flow     selection width, dispersal, density from the agents
sim/warmstart.flow     founding the agents on the attractor
sim/climate.flow       the Climate flow model
sim/world.flow         terrain, regions, temperature, food
sim/population.flow    founding, spatial index, compaction
sim/behaviour.flow     foraging, metabolism, feeding, mortality
sim/reproduction.flow  mate choice and offspring
sim/step.flow          the tick, phase by phase
sim/stats.flow         allele frequencies, F_ST, heritability, dispersal
sim/sampling.flow      VCF and TSV export
life/lconfig.flow      sizes, modes, habitats, rates
life/lgenome.flow      fixed loci, developmental programs, meiosis
life/develop.flow      sparse 2D and 3D body growth
life/creature.flow     the organism record, morphology, phenotype
life/brain.flow        the genetic brain with a recurrent layer
life/lworld.flow       the tick: medium, sensing, feeding, predation, breeding
life/habitat.flow      habitats and experiment presets
life/census.flow       forms, trophic roles, energy flows, histories
life/ocean.flow        the Ocean and Sun flow models
life/fluid.flow        stable fluids with walls
viz/display.flow       full screen through Core Animation (Objective-C runtime)
viz/typo.flow          CoreText typography
viz/fb.flow            frame buffers and anti-aliased drawing
viz/camera.flow        the 2D camera
viz/scene.flow         shading the world: ocean, vessels, microscope styles
viz/tracers.flow       marine snow and event effects
viz/bodies.flow        drawing organisms in each mode
viz/view3d.flow        the 3D view
viz/hud.flow           the overlay, inspector, menu and help
viz/view.flow          one frame, world and overlay
sim/textbuf.flow       text output buffer
sim/canvas.flow        framebuffer, text and numbers
sim/render.flow        views and the genetics panel
tests/                 self-checking tests
analysis/              experiment packaging and the LTEE fit (Python)
tools/                 experiment plots (Python)
docs/                  the project website and browser models
```

## Project status

The results in this README come from the author's own runs on macOS.

What it would take to be a research tool. Done: deterministic, seeded runs; a formal model description (`docs/model.html`, written to the ODD protocol, a standard template for describing agent-based models); population-genetic checks of the shared genetic engine; replicated, controlled experiments with confidence intervals for the life world. Still to do:

- Quantitative checks against theory in the life world, as the Genomic World has: for example the rate at which sector boundaries coarsen at an expanding front, and neutral heterozygosity decay against an estimated effective population size.
- Calibration: rates and units tied to a real organism for any claim beyond qualitative.
- A setting where evolved networks pay, with a control showing selection on them, before claiming anything about the evolution of behaviour.
- Sensitivity analysis: how each result depends on the hand-set constants.
- More replicates, and outside review by a biologist.

Known gaps. These are limits of the model as it stands.

- 128 biallelic loci. There is no sequence, no infinite-sites mutation, and no tree-sequence recording, so coalescent and IBD analyses are out of reach. For those, SLiM with tskit is the standard tool.
- Parameters are scaled for speed. The mutation rate per locus, population size and ticks per generation are not calibrated to any species.
- Fitness for the five traits emerges from an energy budget with hand-set constants. Selection coefficients on those traits are not parameters and are not measured.
- No pleiotropy, epistasis, genotype-by-environment interaction, plasticity or maternal effects.
- Hermaphrodites without selfing. No separate sexes and no mate choice on phenotype.
- Deleterious alleles act on viability at birth only. Fecundity and adult survival are unaffected by them.
- The cline is checked against a mean-field model (above), which still misses by about 0.04 RMS, most at the cold edges. Isolation by distance against 1 / Nb is not yet checked.
- The other four traits have no attractor model: their selection comes from the energy budget and has no closed form, so a warm start leaves them at frequency one half.

## Licence

This repository has no licence yet. By default that means you may read the code here, but you may not copy, change or reuse it without the author's permission.

The E. coli fitness data in `docs/data/ltee-fitness.csv` comes from a Dryad dataset that is reusable under CC0 (public domain).

## Credits

Written by godofecht in [Flow](https://github.com/flooooooooooow/flow).

Sources the model and experiments build on:

- Haldane's map function for recombination.
- Hudson's F_ST estimator, as given by Bhatia et al. (2013).
- Kimura (1962) on the probability of fixation.
- Barton (1983) and Nagylaki on clines and dispersal.
- NEAT, for the way new neurons are added.
- Hallatschek, Hersen, Ramanathan and Nelson (2007), PNAS 104: 19926.
- Gause (1934), The Struggle for Existence.
- Baym, Lieberman, Chase, Gross and Kishony (2016), Science 353: 1147.
- Lenski, Rose, Simpson and Tadler (1991), American Naturalist 138: 1315.
- Wiser, M. J., Ribeck, N. and Lenski, R. E. (2014), "Data from: Long-term dynamics of adaptation in asexual populations", [Dryad dataset](https://doi.org/10.5061/dryad.0hc2m).
