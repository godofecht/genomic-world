(() => {
  const $ = id => document.getElementById(id);
  const colors = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
  const linePlot = (canvas, series, maxY, xLabel, yLabel) => {
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height, left = 54, right = 18, top = 18, bottom = 38;
    ctx.clearRect(0, 0, w, h);
    ctx.font = '12px Inter, system-ui, sans-serif';
    ctx.strokeStyle = colors('--line'); ctx.fillStyle = colors('--faint'); ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = top + (h - top - bottom) * i / 4;
      ctx.beginPath(); ctx.moveTo(left, y); ctx.lineTo(w - right, y); ctx.stroke();
      ctx.fillText((maxY * (1 - i / 4)).toFixed(maxY <= 1 ? 1 : 0), 10, y + 4);
    }
    ctx.fillText(yLabel, 10, 14); ctx.fillText(xLabel, w - right - 32, h - 8);
    for (const item of series) {
      ctx.strokeStyle = item.color; ctx.lineWidth = 2.6; ctx.beginPath();
      item.values.forEach((v, i) => {
        const x = left + (w - left - right) * i / Math.max(1, item.values.length - 1);
        const y = top + (h - top - bottom) * (1 - clamp(v / maxY, 0, 1));
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }); ctx.stroke();
    }
  };

  // A 64-band, 16-locus allele-frequency model with selection, mutation and migration.
  const cline = $('cline'), bands = 64, loci = 16;
  let allele = [], clineGeneration = 0;
  const clineReset = () => {
    allele = Array.from({ length: loci }, () => Array(bands).fill(0.5));
    clineGeneration = 0; drawCline(); $('clineReadout').textContent = 'Generation 0';
  };
  const thermalTarget = (b, warming) => 0.5 - 0.42 * Math.cos(2 * Math.PI * ((b + 0.5) / bands)) + warming;
  const drawCline = () => {
    const warm = Number($('warm').value), means = [], targets = [];
    for (let b = 0; b < bands; b++) {
      let z = 0; for (let l = 0; l < loci; l++) z += allele[l][b] / loci;
      means.push(z); targets.push(thermalTarget(b, warm));
    }
    linePlot(cline, [
      { values: targets, color: colors('--red') },
      { values: means, color: colors('--green') }
    ], 1, 'latitude', 'trait');
    const rmse = Math.sqrt(means.reduce((sum, x, i) => sum + (x - targets[i]) ** 2, 0) / bands);
    $('clineReadout').textContent = `Generation ${clineGeneration} · mean squared error ${rmse.toFixed(3)}`;
  };
  const runCline = () => {
    const warm = Number($('warm').value), migration = Number($('migration').value), strength = Number($('strength').value);
    for (let gen = 0; gen < 100; gen++) {
      const selected = allele.map(row => row.map((p, b) => {
        const target = thermalTarget(b, warm), z = row.reduce((sum, q) => sum + q / loci, 0);
        const delta = clamp((target - z) * strength * 0.055, -0.04, 0.04);
        return clamp(p + p * (1 - p) * delta + 0.0005 * (1 - 2 * p), 0.001, 0.999);
      }));
      allele = selected.map(row => row.map((p, b) => {
        const left = row[(b + bands - 1) % bands], right = row[(b + 1) % bands];
        return clamp(p * (1 - migration) + migration * (left + right) / 2, 0.001, 0.999);
      }));
    }
    clineGeneration += 100; drawCline();
  };
  for (const id of ['warm', 'migration', 'strength']) $(id).addEventListener('input', () => {
    const suffix = id === 'warm' ? '' : '';
    $(`${id}Out`).textContent = `${Number($(id).value).toFixed(id === 'strength' ? 1 : 2)}${suffix}`;
    drawCline();
  });
  $('runCline').addEventListener('click', runCline); $('resetCline').addEventListener('click', clineReset);

  // Discrete logistic prey growth, predation and predator conversion.
  const pp = $('predprey'); let prey, predator, predStep;
  const predReset = () => { prey = 0.72; predator = 0.18; predStep = 0; drawPred(); };
  const drawPred = () => {
    const preySeries = [], predSeries = [];
    for (let i = 0; i <= predStep; i++) {
      preySeries.push(predHistory[i]?.[0] ?? prey); predSeries.push(predHistory[i]?.[1] ?? predator);
    }
    linePlot(pp, [
      { values: preySeries, color: colors('--green') },
      { values: predSeries, color: colors('--red') }
    ], 1, 'time', 'abundance');
    $('predReadout').textContent = `Step ${predStep} · prey ${prey.toFixed(3)} · predators ${predator.toFixed(3)}`;
  };
  let predHistory = [];
  const resetPred = () => { predHistory = []; predReset(); predHistory = [[prey, predator]]; drawPred(); };
  const runPred = () => {
    const refuge = Number($('refuge').value), growth = Number($('food').value), dt = 0.04;
    for (let i = 0; i < 600; i++) {
      const accessible = prey * (1 - refuge);
      const eaten = 1.8 * accessible * predator;
      const nextPrey = clamp(prey + dt * (growth * prey * (1 - prey) - eaten), 0, 1);
      const nextPredator = clamp(predator + dt * (0.7 * eaten - 0.34 * predator), 0, 1);
      prey = nextPrey; predator = nextPredator; predHistory.push([prey, predator]);
    }
    predStep += 600; drawPred();
  };
  $('refuge').addEventListener('input', () => { $('refugeOut').textContent = `${Math.round(Number($('refuge').value) * 100)}%`; });
  $('food').addEventListener('input', () => { $('foodOut').textContent = Number($('food').value).toFixed(2); });
  $('runPred').addEventListener('click', runPred); $('resetPred').addEventListener('click', resetPred);

  // Stochastic Eden growth on a compact grid. A seeded PRNG makes resets repeatable.
  const frontier = $('frontier'), fw = 190, fh = 74, grid = new Int8Array(fw * fh);
  let frontierStep = 0, seed = 91731;
  const random = () => { seed = (1664525 * seed + 1013904223) >>> 0; return seed / 4294967296; };
  const cell = (x, y) => y * fw + x;
  const frontierReset = () => {
    grid.fill(-1); seed = 91731; frontierStep = 0;
    const count = Number($('founders').value), start = Math.floor((fw - count) / 2);
    for (let i = 0; i < count; i++) grid[cell(start + i, Math.floor(fh / 2))] = i % 2;
    drawFrontier();
  };
  const drawFrontier = () => {
    const ctx = frontier.getContext('2d'), image = ctx.createImageData(fw, fh);
    const blue = colors('--blue'), gold = colors('--accent');
    const rgb = c => c.match(/[\da-f]{2}/gi)?.map(x => parseInt(x, 16)) || [115, 185, 210];
    const a = rgb(blue), b = rgb(gold);
    for (let i = 0; i < grid.length; i++) {
      const color = grid[i] < 0 ? [18, 22, 27] : (grid[i] === 0 ? a : b), k = i * 4;
      image.data[k] = color[0]; image.data[k + 1] = color[1]; image.data[k + 2] = color[2]; image.data[k + 3] = 255;
    }
    const scratch = document.createElement('canvas'); scratch.width = fw; scratch.height = fh;
    scratch.getContext('2d').putImageData(image, 0, 0); ctx.imageSmoothingEnabled = false; ctx.clearRect(0, 0, frontier.width, frontier.height); ctx.drawImage(scratch, 0, 0, frontier.width, frontier.height);
    let aCount = 0, bCount = 0; for (const v of grid) { if (v === 0) aCount++; else if (v === 1) bCount++; }
    const hetero = aCount + bCount ? 2 * aCount * bCount / ((aCount + bCount) ** 2) : 0;
    $('frontierReadout').textContent = `${aCount + bCount} cells · local heterozygosity ${hetero.toFixed(3)} · ${frontierStep} growth rounds`;
  };
  const growFrontier = () => {
    const neighborhood = Number($('neighbors').value), rounds = 95;
    for (let r = 0; r < rounds; r++) {
      const candidates = [];
      for (let y = 1; y < fh - 1; y++) for (let x = 1; x < fw - 1; x++) {
        const i = cell(x, y); if (grid[i] >= 0) continue;
        if (grid[cell(x - 1, y)] >= 0 || grid[cell(x + 1, y)] >= 0 || grid[cell(x, y - 1)] >= 0 || grid[cell(x, y + 1)] >= 0) candidates.push(i);
      }
      if (!candidates.length) break;
      for (let n = 0; n < Math.min(neighborhood * 28, candidates.length); n++) {
        const at = Math.floor(random() * candidates.length), i = candidates[at];
        if (grid[i] >= 0) continue;
        const x = i % fw, y = Math.floor(i / fw), parents = [grid[i - 1], grid[i + 1], grid[i - fw], grid[i + fw]].filter(v => v >= 0);
        if (parents.length) grid[i] = parents[Math.floor(random() * parents.length)];
      }
    }
    frontierStep += rounds; drawFrontier();
  };
  $('neighbors').addEventListener('input', () => { $('neighborsOut').textContent = $('neighbors').value; });
  $('founders').addEventListener('input', () => { $('foundersOut').textContent = $('founders').value; });
  $('runFrontier').addEventListener('click', growFrontier); $('resetFrontier').addEventListener('click', frontierReset);

  $('warmOut').textContent = Number($('warm').value).toFixed(2); $('migrationOut').textContent = Number($('migration').value).toFixed(2); $('strengthOut').textContent = Number($('strength').value).toFixed(1);
  $('refugeOut').textContent = `${Math.round(Number($('refuge').value) * 100)}%`; $('foodOut').textContent = Number($('food').value).toFixed(2);
  $('neighborsOut').textContent = $('neighbors').value; $('foundersOut').textContent = $('founders').value;
  clineReset(); resetPred(); frontierReset();
})();
