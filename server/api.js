// Chordseed tools shared by the Claude connector (/mcp) and the in-app assistant (/api/assistant).
// Every answer comes from the app's own engine (server/engine.js, built from src/Main.dc.html).
import * as E from './engine.js';

export const APP_URL = 'https://chordseed.pages.dev/app/';
const MOOD_IDS = ['any', 'happy', 'sad', 'epic', 'dreamy', 'tense', 'dark'];
const MOOD_ALIAS = { melancholic: 'sad', melancholy: 'sad', triste: 'sad', melancolico: 'sad', 'melancólico': 'sad', alegre: 'happy', epico: 'epic', 'épico': 'epic', 'soñador': 'dreamy', sonador: 'dreamy', tenso: 'tense', oscuro: 'dark' };
const GENRES = Object.keys(E.RE_STYLES);

function lang(a) { return a && a.language === 'es' ? 'es' : 'en'; }
function moodId(m) { m = String(m || 'any').toLowerCase().trim(); m = MOOD_ALIAS[m] || m; return MOOD_IDS.indexOf(m) >= 0 ? m : 'any'; }
function genreId(g) {
  g = String(g || '').toLowerCase().trim();
  if (GENRES.indexOf(g) >= 0) return g;
  const hit = GENRES.find((id) => [E.RE_STYLES[id].en[0], E.RE_STYLES[id].es[0]].some((n) => n.toLowerCase().indexOf(g) >= 0));
  return g && hit ? hit : 'pop';
}
function clamp(n, lo, hi, d) { n = Number(n); return isFinite(n) ? Math.max(lo, Math.min(hi, Math.round(n))) : d; }

export function chordsOf(input, need) {
  const r = E.parseChordList(input);
  if (r.bad.length) throw new Error('Could not read these chords: ' + r.bad.join(', ') + '. Use names like C, Am, F#m7, Bbmaj7, Dsus4, G7 (Latin names like Do, Lam, Sol7 also work).');
  if (need && r.chords.length < need) throw new Error('Give at least ' + need + ' chord' + (need > 1 ? 's' : '') + '.');
  return r.chords.slice(0, 16);
}
function keyName(k, l) {
  const n = E.spell(k.t, E.flatsFor(k.t, k.mode), false);
  return n + (k.mode === 'maj' ? (l === 'es' ? ' mayor' : ' major') : (l === 'es' ? ' menor' : ' minor'));
}
function nm(c, k) { return E.chordName(c, k); }
function parseKey(s) {
  s = String(s || '').trim();
  const m = s.match(/^([A-Ga-g](?:#|b)?|do|re|mi|fa|sol|la|si)\s*(.*)$/i);
  if (!m) throw new Error('Could not read the key "' + s + '". Use e.g. "C major", "A minor", "F#m", "Bb".');
  const c = E.parseChordName(m[1]); if (!c) throw new Error('Could not read the key "' + s + '".');
  const rest = m[2].toLowerCase();
  const minor = /^(m|min|minor|menor)\b/.test(rest) || rest === 'm';
  return { t: c.pc, mode: minor ? 'min' : 'maj' };
}
export function appLink(chords, mood) {
  const names = chords.map((c) => nm(c, E.detect(chords)));
  let u = APP_URL + '?p=' + encodeURIComponent(names.join(','));
  if (mood && mood !== 'any') u += '&mood=' + mood;
  return u;
}

export const TOOLS = [
  {
    name: 'suggest_next_chords',
    title: 'Suggest the next chord',
    description: 'Given a chord progression, suggest which chords can come next, ranked by how well they fit the key, the chosen mood and genre. Returns the detected key, Roman numerals, harmonic function and a link to open the result in Chordseed.',
    inputSchema: { type: 'object', properties: {
      chords: { type: 'string', description: 'The progression so far, e.g. "C G Am F". Latin names (Do Sol Lam Fa) also work.' },
      mood: { type: 'string', enum: MOOD_IDS, description: 'Feeling to aim for. Default any.' },
      genre: { type: 'string', enum: GENRES, description: 'Style that shapes the chord colors. Default pop.' },
      complexity: { type: 'integer', minimum: 0, maximum: 5, description: '0 = simple triads … 5 = rich jazz extensions.' },
      surprise: { type: 'integer', minimum: 0, maximum: 2, description: '0 = only in-key chords, 1 = some, 2 = bold.' },
      phrase_length: { type: 'integer', minimum: 1, maximum: 8, description: 'How many chords each suggestion adds (1 = just the next chord).' },
      language: { type: 'string', enum: ['en', 'es'] }
    }, required: ['chords'] },
    run(a) {
      // Same ranking as the app's generator (renderVals → cand/chains), without rendering the page.
      const l = lang(a), ch = chordsOf(a.chords, 1), mood = moodId(a.mood), g = genreId(a.genre);
      const st = { mood, sur: clamp(a.surprise, 0, 2, 1), cx: clamp(a.complexity, 0, 5, 0), count: clamp(a.phrase_length, 1, 8, 1) };
      const k = E.detect(ch), pool = E.POOL[k.mode], last = ch[ch.length - 1], lastP = E.findIn(pool, k.t, last);
      const cand = pool.filter((p) => !((k.t + p.o) % 12 === last.pc && p.q === last.q)).map((p) => ({ p, sc: E.scoreOf(p, lastP, st) })).sort((x, y) => y.sc - x.sc).slice(0, 5);
      const top = cand.length ? cand[0].sc : 1;
      const style = E.RE_STYLES[g];
      const disp = (p) => { let sx = E.sfx(p, st.cx); if (st.cx > 0 && a.genre && style) { const v = style[p.q === 'dim' ? 'dim' : (p.f === 'D' && p.q === 'M' ? 'D' : p.q)]; if (v) sx = p.q === 'm' && v.indexOf('m') !== 0 ? 'm' : v; } return E.mkSx((k.t + p.o) % 12, sx === 'M' ? '' : sx); };
      const chains = cand.map((c) => {
        const chain = [c.p]; let prev = c.p;
        for (let n = 1; n < st.count; n++) {
          const nx = pool.filter((x) => x !== prev && chain.filter((y) => y === x).length < 2).map((x) => ({ x, sc: E.scoreOf(x, prev, st) * (chain.indexOf(x) >= 0 ? 0.55 : 1) })).sort((p1, p2) => p2.sc - p1.sc);
          if (!nx.length) break; chain.push(nx[0].x); prev = nx[0].x;
        }
        return { c, chain };
      });
      return {
        progression: ch.map((c) => nm(c, k)).join(' '), key: keyName(k, l), mood, genre: style[l][0],
        suggestions: chains.map((x) => ({
          chords: x.chain.map((p) => nm(disp(p), k)).join(' '), roman: x.chain.map((p) => p.r).join(' '),
          function: E.FN[x.c.p.f][l], fit: Math.max(5, Math.round(x.c.sc / top * 100)) + '%',
          matches_mood: mood !== 'any' && x.chain.every((p) => p.m && p.m.indexOf(mood) >= 0), why: x.c.p[l]
        })),
        open_in_chordseed: appLink(ch, mood)
      };
    }
  },
  {
    name: 'analyze_progression',
    title: 'Analyze a progression',
    description: 'Explain a chord progression: its key, Roman numerals, known pattern, mood and the harmonic techniques it uses (cadences, borrowed chords, secondary dominants…).',
    inputSchema: { type: 'object', properties: { chords: { type: 'string', description: 'e.g. "Am F C G"' }, language: { type: 'string', enum: ['en', 'es'] } }, required: ['chords'] },
    run(a) {
      const l = lang(a), es = l === 'es', ch = chordsOf(a.chords, 2);
      E.__setLang(l);
      const k0 = E.detectAll(ch)[0];
      const an = E.analyze(ch, es, (c) => nm(c, k0));
      const mood = E.MOODS.filter((m) => m[0] === an.mood)[0];
      return {
        key: keyName(an.k, l), chords_that_fit_the_key: an.k.fit + '/' + ch.length,
        alternative_reading: an.alt && an.alt.score >= an.k.score - 0.6 ? keyName(an.alt, l) : null,
        chords: an.items.map((x) => ({ chord: nm(x.c, an.k), roman: x.roman, function: x.fn ? E.FN[x.fn][l] : (es ? 'Fuera de la tonalidad' : 'Outside the key'), note: x.note })),
        pattern: an.pattern ? { name: an.pattern.P[l][0], roman: an.pattern.roman, about: an.pattern.P[l][1] } : null,
        mood: mood ? mood[es ? 1 : 2] : null,
        techniques: (an.devices || []).map((d) => ({ where: d.at, name: d.title, about: d.desc })),
        open_in_chordseed: appLink(ch)
      };
    }
  },
  {
    name: 'reharmonize',
    title: 'Reharmonize',
    description: 'Give a progression new colors in a chosen style: richer extensions, substitute chords, secondary dominants and tritone subs, keeping the melody-friendly shape.',
    inputSchema: { type: 'object', properties: {
      chords: { type: 'string' }, style: { type: 'string', enum: GENRES, description: 'Default jazz.' },
      level: { type: 'integer', minimum: 0, maximum: 2, description: '0 = only add color, 1 = moderate substitutions, 2 = bold.' },
      language: { type: 'string', enum: ['en', 'es'] }
    }, required: ['chords'] },
    run(a) {
      const l = lang(a), ch = chordsOf(a.chords, 2), k = E.detect(ch), st = genreId(a.style || 'jazz'), lv = clamp(a.level, 0, 2, 1);
      const cols = E.reharm(ch, k, { style: st, level: lv, keep: lv === 0 ? 'keep' : 'free', pass: false, end: 'same', v: 0 });
      const out = []; cols.forEach((col) => col.outs.forEach((o) => out.push(o.c)));
      return {
        original: ch.map((c) => nm(c, k)).join(' '), key: keyName(k, l), style: E.RE_STYLES[st][l][0],
        reharmonized: out.map((c) => nm(c, k)).join(' '),
        changes: cols.map((col) => ({ from: nm(col.orig, k), to: col.outs.map((o) => nm(o.c, k)).join(' '), kind: col.outs.map((o) => o.tag).join(', ') })),
        open_in_chordseed: appLink(out)
      };
    }
  },
  {
    name: 'key_change',
    title: 'Plan a key change',
    description: 'Find chord routes to modulate smoothly from one key to another (pivot chord, ii–V, direct dominant, chromatic slide).',
    inputSchema: { type: 'object', properties: { from_key: { type: 'string', description: 'e.g. "C major", "Am"' }, to_key: { type: 'string', description: 'e.g. "G major", "F#m"' }, language: { type: 'string', enum: ['en', 'es'] } }, required: ['from_key', 'to_key'] },
    run(a) {
      const l = lang(a), O = parseKey(a.from_key), D = parseKey(a.to_key);
      const routes = E.modRoutes(O, D);
      const label = { pivot: 'Pivot chord', iiV: 'ii–V into the new key', direct: 'Direct dominant', chrom: 'Chromatic slide' };
      return {
        from: keyName(O, l), to: keyName(D, l),
        routes: routes.map((r) => ({ type: label[r.id] || r.id, chords: r.chords.map((c) => nm(c, D)).join(' → '), smoothness: r.smooth + '/3', open_in_chordseed: appLink(r.chords) }))
      };
    }
  },
  {
    name: 'scales_for_progression',
    title: 'Scales to improvise over a progression',
    description: 'Which scales to solo or write melodies with over a progression: one scale for the whole thing plus the best scales over each chord, with their notes.',
    inputSchema: { type: 'object', properties: { chords: { type: 'string' }, language: { type: 'string', enum: ['en', 'es'] } }, required: ['chords'] },
    run(a) {
      const l = lang(a), ch = chordsOf(a.chords, 1), k = E.detect(ch), fl = E.flatsFor(k.t, k.mode);
      const sc = (root, id) => ({ name: E.spell(root, fl, false) + ' ' + E.SCALES[id][l][0], about: E.SCALES[id][l][1], notes: E.SCALES[id].iv.map((i) => E.spell((root + i) % 12, fl, false)).join(' ') });
      return {
        key: keyName(k, l), whole_progression: sc(k.t, k.mode === 'maj' ? 'ion' : 'aeo'),
        per_chord: ch.map((c) => ({ chord: nm(c, k), scales: E.scalesForChord(c, k).filter((id) => E.SCALES[id]).map((id) => sc(c.pc, id)) }))
      };
    }
  },
  {
    name: 'chord_info',
    title: 'Chord info',
    description: 'Notes, intervals and a guitar fingering for any chord symbol, plus chords that can substitute for it.',
    inputSchema: { type: 'object', properties: { chord: { type: 'string', description: 'e.g. "F#m7b5", "Bbmaj7", "Lam"' }, key: { type: 'string', description: 'Optional key for substitutes, e.g. "C major".' }, language: { type: 'string', enum: ['en', 'es'] } }, required: ['chord'] },
    run(a) {
      const c = E.parseChordName(a.chord); if (!c) throw new Error('Could not read the chord "' + a.chord + '".');
      const k = a.key ? parseKey(a.key) : { t: c.pc, mode: c.q === 'M' ? 'maj' : 'min' };
      const fl = a.key ? E.flatsFor(k.t, k.mode) : [1, 3, 8, 10].indexOf(c.pc) >= 0;
      const IV = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', 'b7', '7'];
      const ivs = E.chordIvls(c);
      return {
        chord: E.spell(c.pc, fl, false) + (c.sx || ''), notes: ivs.map((i) => E.spell((c.pc + i) % 12, fl, false)).join(' '),
        intervals: ivs.map((i) => (i >= 12 ? ({ 14: '9', 17: '11', 21: '13' })[i] || String(i) : IV[i])).join(' '),
        guitar_frets_low_to_high: E.guitarFrets(c).map((f) => (f < 0 ? 'x' : String(f))).join(' '),
        substitutes: E.substitutes(c, k).map((s) => ({ chord: nm(s.c, k), why: s.why[lang(a) === 'es' ? 0 : 1] }))
      };
    }
  },
  {
    name: 'find_similar_songs',
    title: 'Songs with similar chords',
    description: 'Real songs that use the same or a similar progression, the user\'s genre first, with the original key of each song.',
    inputSchema: { type: 'object', properties: { chords: { type: 'string' }, genre: { type: 'string', enum: GENRES }, language: { type: 'string', enum: ['en', 'es'] } }, required: ['chords'] },
    run(a) {
      // Transposition-free match against the app's song list (same idea as the app's "Songs" block).
      const l = lang(a), ch = chordsOf(a.chords, 2), g = a.genre ? genreId(a.genre) : null, k = E.detect(ch);
      const qc = (sx) => (/^m(?!aj)/.test(sx) ? (sx === 'm7b5' ? 'd' : 'm') : (String(sx).indexOf('dim') === 0 ? 'd' : 'M'));
      const toks = (list) => list.map((c, i) => [c.pc, c.q]);
      const U = toks(ch.map((c) => ({ pc: c.pc, q: c.q === 'dim' ? 'd' : c.q })));
      const same = (A, B, shift) => A.length === B.length && A.every((x, i) => (x[0] + shift) % 12 === B[i][0] && x[1] === B[i][1]);
      const out = [];
      E.SONGS.forEach((S) => {
        const SC = S.c.map((q) => [(S.k + q[0]) % 12, qc(q[1])]);
        let best = null;
        for (let r = 0; r < SC.length; r++) {
          const rot = SC.slice(r).concat(SC.slice(0, r));
          const shift = (U[0][0] - rot[0][0] + 12) % 12;
          if (same(rot, U, shift)) { best = { kind: 'same', shift }; break; }
          let run = 0; while (run < Math.min(rot.length, U.length) && (rot[run][0] + shift) % 12 === U[run][0] && rot[run][1] === U[run][1]) run++;
          if (run >= 3 && (!best || run > best.run)) best = { kind: 'shares', shift, run };
        }
        if (!best) return;
        const fl = E.flatsFor(S.k, S.m), kD = { t: (S.k + best.shift) % 12, mode: S.m };
        const orig = S.c.map((q) => E.spell((S.k + q[0]) % 12, fl, false) + (q[1] === 'M' ? '' : q[1])).join(' ');
        const mine = S.c.map((q) => nm(E.mkSx((S.k + q[0] + best.shift) % 12, q[1] === 'M' ? '' : q[1]), kD)).join(' ');
        out.push({
          score: (best.kind === 'same' ? 100 : 10 * best.run) + (g && (S.g === g || ((E.GENRE_REL[g] || []).indexOf(S.g) >= 0)) ? (S.g === g ? 50 : 20) : 0),
          title: String(S.t).split('|')[l === 'es' ? 0 : 1] || String(S.t).split('|')[0], artist: String(S.a).split('|')[0],
          style: S.tag ? S.tag[l === 'es' ? 0 : 1] : (E.RE_STYLES[S.g] ? E.RE_STYLES[S.g][l][0] : S.g),
          match: best.kind === 'same' ? (l === 'es' ? 'misma progresión' : 'same progression') : (l === 'es' ? 'comparte ' + best.run + ' acordes seguidos' : 'shares ' + best.run + ' chords in a row'),
          original_key: E.spell(S.k, fl, false) + (S.m === 'maj' ? '' : 'm'), roman: S.r, chords_original: orig, chords_in_your_key: mine
        });
      });
      out.sort((x, y) => y.score - x.score);
      return { your_key: keyName(k, l), songs: out.slice(0, 10).map((x) => { delete x.score; return x; }), note: out.length ? undefined : (l === 'es' ? 'No hay canciones en la lista de Chordseed con esta progresión.' : 'No songs in Chordseed\'s list use this progression.') };
    }
  },
  {
    name: 'open_in_chordseed',
    title: 'Open in Chordseed',
    description: 'Make a link that opens Chordseed with this progression loaded, so the user can hear it with their instrument, see the fingerings, keep building and save it.',
    inputSchema: { type: 'object', properties: { chords: { type: 'string' }, mood: { type: 'string', enum: MOOD_IDS } }, required: ['chords'] },
    run(a) { const ch = chordsOf(a.chords, 1); return { link: appLink(ch, moodId(a.mood)), progression: ch.map((c) => nm(c, E.detect(ch))).join(' ') }; }
  }
];

export function runTool(name, args) {
  const t = TOOLS.find((x) => x.name === name);
  if (!t) throw new Error('Unknown tool: ' + name);
  return t.run(args || {});
}
