/* Chordseed chord ear: spectrum -> notes -> ranked chord candidates. Pure functions, no DOM. */
var CE_CFG = { pr: 100, gap: 9, lu: 1.0, lm: 1.0, bb: 0.06, ftol: 0.012, subr: 0.08, sub: 0.06, pw: 0.5, al: 27, be: 320, stop: 0.3, thr: 0.04, fund: 0.1, pres: 0.22 };
var CE_TYPES = [
  // id (app QUALS id), intervals, weight penalty (simpler chords win ties)
  { id: 'M', iv: [0, 4, 7], pen: 0 },
  { id: 'm', iv: [0, 3, 7], pen: 0 },
  { id: '7', iv: [0, 4, 7, 10], pen: 0.035 },
  { id: 'maj7', iv: [0, 4, 7, 11], pen: 0.035 },
  { id: 'm7', iv: [0, 3, 7, 10], pen: 0.035 },
  { id: 'sus4', iv: [0, 5, 7], pen: 0.03 },
  { id: 'sus2', iv: [0, 2, 7], pen: 0.03 },
  { id: 'dim', iv: [0, 3, 6], pen: 0.04 },
  { id: '6', iv: [0, 4, 7, 9], pen: 0.045 },
  { id: 'm6', iv: [0, 3, 7, 9], pen: 0.045 },
  { id: 'add9', iv: [0, 2, 4, 7], pen: 0.045 },
  { id: '9', iv: [0, 2, 4, 7, 10], pen: 0.06 }
];
function ceMtof(m) { return 440 * Math.pow(2, (m - 69) / 12); }
function ceFtom(f) { return 69 + 12 * Math.log(f / 440) / Math.LN2; }

// mags: linear magnitude per bin (length fftSize/2), sr: sample rate
function cePeaks(mags, sr, fftSize) {
  var binHz = sr / fftSize, out = [], max = 0, i;
  var lo = Math.max(2, Math.floor(60 / binHz)), hi = Math.min(mags.length - 2, Math.floor(4200 / binHz));
  for (i = lo; i <= hi; i++) if (mags[i] > max) max = mags[i];
  if (max <= 0) return { peaks: out, max: 0 };
  var thr = max * CE_CFG.thr;
  for (i = lo; i <= hi; i++) {
    var a = mags[i];
    if (a < thr || a < mags[i - 1] || a < mags[i + 1] || a < mags[i - 2] || a < mags[i + 2]) continue;
    // parabolic interpolation on log magnitude
    var l = Math.log(mags[i - 1] + 1e-12), c = Math.log(a + 1e-12), r = Math.log(mags[i + 1] + 1e-12);
    var d = l - 2 * c + r, off = d ? 0.5 * (l - r) / d : 0;
    if (off > 0.5 || off < -0.5) off = 0;
    out.push({ f: (i + off) * binHz, a: a / max });
  }
  return { peaks: out, max: max };
}

// Iterative multi-pitch estimation over spectral peaks (harmonic summation + partial subtraction)
function ceNotes(peaks) {
  var res = peaks.map(function (p) { return { f: p.f, a: p.a }; });
  var notes = [], first = 0;
  var tol = 0.035; // ~60 cents
  var match = function (f, t) { var best = null, bd = 1, tt = t || tol; res.forEach(function (p) { var d = Math.abs(p.f / f - 1); if (d < tt && d < bd && p.a > 0.002) { bd = d; best = p; } }); return best; };
  for (var it = 0; it < 6; it++) {
    var bestS = 0, bestM = -1;
    for (var m = 36; m <= 77; m++) {
      var f0 = ceMtof(m), s = 0, fund = match(f0, CE_CFG.ftol);
      if (!fund || fund.a < CE_CFG.fund) continue; // require some energy at the fundamental (guitar always has it)
      for (var h = 1; h <= 8; h++) { var p = match(f0 * h); if (p) s += Math.sqrt(p.a) * (1 / (0.6 + 0.4 * h)); }
      // octave-error guard: a note one octave down from a strong note only gets credit for odd harmonics it explains
      if (s > bestS) { bestS = s; bestM = m; }
    }
    if (bestM < 0) break;
    // octave correction: a lower note whose own fundamental is present and whose odd harmonics explain peaks wins
    [12].forEach(function (d) {
      var lowM = bestM - d; if (lowM < 36) return;
      var fl = ceMtof(lowM), fp = match(fl), hp = match(ceMtof(bestM)); if (!fp || fp.a < CE_CFG.sub || (hp && fp.a < hp.a * CE_CFG.subr)) return;
      var odd = 0; [3, 5].forEach(function (h) { var q = match(fl * h); if (q && q.a > 0.05) odd++; });
      if (odd >= 1 && d === 12 ? true : odd >= 1) { bestM = lowM; }
    });
    if (!first) first = bestS;
    if (bestS < first * CE_CFG.stop) break;
    var f1 = ceMtof(bestM), base = match(f1), a1 = base ? base.a : 0;
    notes.push({ m: bestM, s: bestS, a: a1 });
    // subtract this note's expected partials
    for (var h2 = 1; h2 <= 10; h2++) {
      var pp = match(f1 * h2); if (!pp) continue;
      pp.a = 0;
    }
  }
  // prune notes that sit exactly on a strong harmonic (h3, h5, h6, h7) of a lower detected note and are much weaker
  notes = notes.filter(function (n) {
    return !notes.some(function (o) { var d = n.m - o.m; return (d === 19 || d === 28 || d === 31 || d === 34) && n.s < o.s * CE_CFG.pr; });
  });
  return notes;
}

// keyPcs: optional array of pitch classes of the current key (context), returns top candidates
function ceRank(notes, keyPcs) {
  if (!notes.length) return [];
  var chroma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], bass = null;
  notes.forEach(function (n) { chroma[n.m % 12] += Math.sqrt(n.s); if (bass === null || n.m < bass) bass = n.m; });
  var bpc = bass % 12, norm = Math.sqrt(chroma.reduce(function (t, v) { return t + v * v; }, 0)) || 1;
  var cn = chroma.map(function (v) { return v / norm; });
  var present = cn.map(function (v) { return v > CE_CFG.pres; });
  var cands = [];
  for (var r = 0; r < 12; r++) {
    CE_TYPES.forEach(function (T) {
      var tv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
      T.iv.forEach(function (iv, k) { tv[(r + iv) % 12] = k === 2 && T.iv.length >= 3 && iv === 7 ? 0.75 : 1; });
      var tn = Math.sqrt(tv.reduce(function (t, v) { return t + v * v; }, 0));
      var dot = 0; for (var i = 0; i < 12; i++) dot += cn[i] * tv[i] / tn;
      // must contain the root and the defining note (3rd / sus / dim 5th) when they matter
      var hasRoot = present[r];
      var def = T.iv[1]; var hasDef = present[(r + def) % 12];
      var extraOut = 0; for (var j = 0; j < 12; j++) if (present[j] && !tv[j]) extraOut++;
      var missing = 0; T.iv.forEach(function (iv) { if (!present[(r + iv) % 12] && iv !== 7) missing++; });
      var mx = Math.max.apply(null, chroma) || 1, wv = chroma.map(function (v) { return v / mx; });
      var expl = 0, unex = 0, miss = 0;
      for (var q = 0; q < 12; q++) { if (tv[q]) expl += wv[q]; else unex += wv[q]; }
      T.iv.forEach(function (iv) { var w = wv[(r + iv) % 12]; if (w < CE_CFG.pres) miss += (iv === 7 ? 0.35 : 1); });
      var sc = expl - CE_CFG.lu * unex - CE_CFG.lm * miss - T.pen * 4 + (bpc === r ? CE_CFG.bb * 4 : 0);
      if (keyPcs && keyPcs.length) { var inKey = T.iv.every(function (iv) { return keyPcs.indexOf((r + iv) % 12) >= 0; }); if (inKey) sc += 0.03; }
      cands.push({ pc: r, id: T.id, score: sc, bass: bpc });
    });
  }
  cands.sort(function (a, b) { return b.score - a.score; });
  var top = cands.slice(0, 3), best = top[0] ? top[0].score : 0;
  return top.filter(function (c, i) { return i === 0 || c.score > best - CE_CFG.gap; });
}

if (typeof module !== 'undefined') module.exports = { CE_CFG: CE_CFG, cePeaks: cePeaks, ceNotes: ceNotes, ceRank: ceRank, CE_TYPES: CE_TYPES, ceMtof: ceMtof };
