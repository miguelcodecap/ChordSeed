import { guitarFrets, parseChordName, chordName } from '/home/claude/chordseed/server/engine.js';
import { createRequire } from 'module'; const require = createRequire(import.meta.url);
const E = require(process.env.CE || './chordear.js');
const SR = 44100, N = 16384;
let seed = 7; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
function ks(f, dur, vel) { const n = Math.floor(SR * dur), out = new Float32Array(n), p = Math.max(2, Math.round(SR / f)); const buf = new Float32Array(p); for (let i = 0; i < p; i++) buf[i] = (rnd() * 2 - 1) * vel; let idx = 0; for (let i = 0; i < n; i++) { const a = buf[idx], b = buf[(idx + 1) % p]; const v = 0.996 * 0.5 * (a + b); out[i] = a; buf[idx] = v; idx = (idx + 1) % p; } return out; }
function render(midis, noise) { const dur = 1.4, n = Math.floor(SR * dur), mix = new Float32Array(n); midis.forEach((m, k) => { const det = (rnd() - 0.5) * 0.24; const s = ks(440 * Math.pow(2, (m + det - 69) / 12), dur, 0.6 + rnd() * 0.4); const off = Math.floor(k * 0.012 * SR); for (let i = 0; i + off < n; i++) mix[i + off] += s[i]; }); for (let i = 0; i < n; i++) mix[i] += (rnd() * 2 - 1) * noise; return mix; }
function fft(re, im) { const n = re.length; for (let i = 1, j = 0; i < n; i++) { let bit = n >> 1; for (; j & bit; bit >>= 1) j ^= bit; j ^= bit; if (i < j) { [re[i], re[j]] = [re[j], re[i]];[im[i], im[j]] = [im[j], im[i]]; } } for (let len = 2; len <= n; len <<= 1) { const ang = -2 * Math.PI / len, wr = Math.cos(ang), wi = Math.sin(ang); for (let i = 0; i < n; i += len) { let cr = 1, ci = 0; for (let j = 0; j < len / 2; j++) { const ur = re[i + j], ui = im[i + j], vr = re[i + j + len / 2] * cr - im[i + j + len / 2] * ci, vi = re[i + j + len / 2] * ci + im[i + j + len / 2] * cr; re[i + j] = ur + vr; im[i + j] = ui + vi; re[i + j + len / 2] = ur - vr; im[i + j + len / 2] = ui - vi; const t = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = t; } } } }
function spectrum(sig) { const acc = new Float32Array(N / 2); const starts = [0.12, 0.3, 0.48].map(t => Math.floor(t * SR)); starts.forEach(st => { const re = new Float64Array(N), im = new Float64Array(N); for (let i = 0; i < N; i++) { const w = 0.42 - 0.5 * Math.cos(2 * Math.PI * i / (N - 1)) + 0.08 * Math.cos(4 * Math.PI * i / (N - 1)); re[i] = (sig[st + i] || 0) * w; } fft(re, im); for (let i = 0; i < N / 2; i++) acc[i] += Math.hypot(re[i], im[i]); }); return acc; }
const STD = [40, 45, 50, 55, 59, 64];
const QS = { M: '', m: 'm', '7': '7', maj7: 'maj7', m7: 'm7', sus4: 'sus4', sus2: 'sus2', dim: 'dim', '6': '6', m6: 'm6', add9: 'add9', '9': '9' };
const names = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'];
const tests = [];
for (const r of names) for (const q of ['', 'm', '7', 'maj7', 'm7', 'sus4', 'sus2', 'dim']) tests.push(r + q);
// extra tunings: hand voicings (midi) e.g. Drop D D5/D, open G G, DADGAD Dsus4
const extra = [['D', [38, 45, 50, 54, 57, 62]], ['G', [38, 43, 50, 55, 59, 62]], ['Dsus4', [38, 45, 50, 55, 57, 62]], ['C', [36, 43, 48, 52, 55, 60]], ['E', [40, 47, 52, 56, 59, 64]], ['Am', [45, 52, 57, 60, 64]], ['F', [41, 48, 53, 57, 60, 65]], ['Bm', [47, 54, 59, 62, 66]]];
let ok = 0, top3 = 0, total = 0; const fails = []; const byQ = {};
function run(label, midis, noise) {
  const sig = render(midis, noise), sp = spectrum(sig), pk = E.cePeaks(sp, SR, N), notes = E.ceNotes(pk.peaks), cands = E.ceRank(notes, null);
  const want = parseChordName(label); const nm = c => names[c.pc] + QS[c.id];
  const eq = c => c.pc === want.pc && (QS[c.id] === (want.sx || '') );
  const qk = (want.sx||'M'); byQ[qk] = byQ[qk] || [0,0,0]; byQ[qk][2]++; if (cands[0] && eq(cands[0])) byQ[qk][0]++; if (cands.some(eq)) byQ[qk][1]++;
  total++; if (cands[0] && eq(cands[0])) ok++; else fails.push(label + ' -> ' + cands.map(nm).join('/') + ' notes:' + notes.map(n => names[n.m % 12] + Math.floor(n.m / 12 - 1)).join(' '));
  if (cands.some(eq)) top3++;
}
for (const noise of [0.002, 0.03]) {
  for (const t of tests) { const c = parseChordName(t); const fr = guitarFrets(c); const midis = fr.map((f, i) => f >= 0 ? STD[i] + f : null).filter(x => x !== null); run(t, midis, noise); }
  for (const [l, m] of extra) run(l, m, noise);
}
console.log('top1', ok, '/', total, ' top3', top3, '/', total);
console.log(fails.filter(f=>/^[A-G][b#]?(m7|) ->/.test(f)).slice(0,30).join('\n'));console.log(Object.entries(byQ).map(([k,v])=>k+': '+v[0]+'/'+v[1]+'/'+v[2]).join('  '));
