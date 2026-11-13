// Lumen, Chordseed's in-app assistant (Pro). POST /api/assistant
// Body: { messages: [{ role: 'user'|'assistant', content: string }], context: { chords: 'C G Am', language: 'es'|'en', instrument, genre, mood } }
// Header: Authorization: Bearer <Supabase access token of the signed-in user>
// Needs the secret ANTHROPIC_API_KEY (Cloudflare Pages → Settings → Variables and Secrets).
import { TOOLS, runTool, chordsOf, appLink } from '../../server/api.js';

const SB_URL = 'https://siafatxbgecgenhnciej.supabase.co';
const SB_KEY = 'sb_publishable_wbMAklnoQrY6-P0vM1KVlw_l0llY6fK';
const MODEL = 'claude-haiku-5-5';
const DAILY_LIMIT = 40, GUEST_LIMIT = 4;
const MAX_TURNS = 12, MAX_CHARS = 2000, MAX_STEPS = 4;
const CORS = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, Authorization' };

function reply(body, status) { return new Response(JSON.stringify(body), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json' }, CORS) }); }
function sb(env, path, token, init) {
  return fetch((env.SUPABASE_URL || SB_URL) + path, Object.assign({}, init, { headers: Object.assign({ apikey: env.SUPABASE_KEY || SB_KEY, Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' }, (init && init.headers) || {}) }));
}

const PROPOSE = {
  name: 'propose_progression',
  description: 'Show the user a chord progression as a card with a button that loads it into their Chordseed progression. Use it whenever you recommend specific chords.',
  input_schema: { type: 'object', properties: { chords: { type: 'string', description: 'e.g. "Am F C G"' }, label: { type: 'string', description: 'Short title, e.g. "Chorus idea"' } }, required: ['chords'] }
};

function systemPrompt(ctx) {
  const es = ctx.language === 'es';
  return [
    'You are Lumen, the guide of Chordseed, a songwriting app for musicians (an owl-masked forest alchemist with a lantern: warm, wise, never childish).',
    'Help with anything about making music: chords, progressions, harmony, melody, rhythm, song structure, lyrics ideas, arranging, practicing and playing their instrument. Use the tools for chord facts instead of guessing, and use propose_progression whenever you suggest concrete chords so the user can load them with one tap.',
    'Keep answers short and practical (a few sentences or a short list). Do not reproduce copyrighted song lyrics. Politely steer unrelated requests back to music.',
    'Reply in ' + (es ? 'Spanish' : 'the user\'s language (default English)') + '.',
    'User context: instrument = ' + (ctx.instrument || 'unknown') + '; genre = ' + (ctx.genre || 'unknown') + '; mood = ' + (ctx.mood || 'any') + '; current progression in the app = ' + (ctx.chords || 'empty') + '.'
  ].join('\n');
}

async function claude(env, system, messages) {
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({
      model: env.ASSISTANT_MODEL || MODEL, max_tokens: 900,
      system: [{ type: 'text', text: system, cache_control: { type: 'ephemeral' } }],
      tools: TOOLS.filter((t) => t.name !== 'open_in_chordseed').map((t) => ({ name: t.name, description: t.description, input_schema: t.inputSchema })).concat([PROPOSE]),
      messages
    })
  });
  if (!r.ok) throw new Error('Claude API ' + r.status + ': ' + (await r.text()).slice(0, 300));
  return r.json();
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (request.method !== 'POST') return reply({ error: 'method' }, 405);
  if (!env.ANTHROPIC_API_KEY) return reply({ error: 'not_configured', message: 'The assistant is not set up yet.' }, 503);

  // 1) Who is asking? Signed-in Pro users get the daily limit; guests get a few free questions.
  const token = (request.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
  let guest = !token;
  if (token) {
    const u = await sb(env, '/auth/v1/user', token);
    if (!u.ok) return reply({ error: 'login' }, 401);
    const user = await u.json();
    const s = await sb(env, '/rest/v1/subscriptions?select=plan,status,current_period_end&user_id=eq.' + encodeURIComponent(user.id), token);
    const sub = s.ok ? (await s.json())[0] : null;
    const pro = !!(sub && sub.plan === 'pro' && ['active', 'trialing', 'past_due'].indexOf(sub.status) >= 0 && (!sub.current_period_end || new Date(sub.current_period_end) > new Date()));
    if (!pro) return reply({ error: 'pro' }, 402);
  }

  // 2) Read the conversation.
  let body;
  try { body = await request.json(); } catch (e) { return reply({ error: 'bad_request' }, 400); }
  const ctx = body.context || {};
  const msgs = (Array.isArray(body.messages) ? body.messages : []).slice(-MAX_TURNS)
    .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string' && m.content.trim())
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_CHARS) }));
  while (msgs.length && msgs[0].role !== 'user') msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') return reply({ error: 'bad_request' }, 400);

  // 3) Daily limit (counts one per question).
  let used, limit;
  if (guest) {
    const ip = request.headers.get('CF-Connecting-IP') || request.headers.get('X-Forwarded-For') || 'unknown';
    const dig = await crypto.subtle.digest('SHA-256', new TextEncoder().encode((env.GUEST_SALT || 'chordseed-lumen') + '|' + ip));
    const h = Array.from(new Uint8Array(dig)).map((x) => x.toString(16).padStart(2, '0')).join('');
    const g = await fetch((env.SUPABASE_URL || SB_URL) + '/rest/v1/rpc/assistant_bump_guest', { method: 'POST', headers: { apikey: env.SUPABASE_KEY || SB_KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ h }) });
    used = g.ok ? Number(await g.json()) : Infinity;
    limit = Number(env.ASSISTANT_GUEST_LIMIT || GUEST_LIMIT);
    if (used > limit) return reply({ error: 'guest_limit', limit }, 429);
  } else {
    const b = await sb(env, '/rest/v1/rpc/assistant_bump', token, { method: 'POST', body: '{}' });
    used = b.ok ? Number(await b.json()) : 0;
    limit = Number(env.ASSISTANT_DAILY_LIMIT || DAILY_LIMIT);
    if (used > limit) return reply({ error: 'limit', limit }, 429);
  }

  // 4) Ask Claude, running Chordseed's own tools when it needs them.
  const system = systemPrompt(ctx), cards = [];
  let convo = msgs.slice(), res;
  try {
    for (let step = 0; step < MAX_STEPS; step++) {
      res = await claude(env, system, convo);
      if (res.stop_reason !== 'tool_use') break;
      const results = res.content.filter((c) => c.type === 'tool_use').map((c) => {
        try {
          if (c.name === 'propose_progression') {
            const ch = chordsOf(c.input.chords, 1);
            cards.push({ chords: String(c.input.chords).trim(), label: c.input.label || '', link: appLink(ch) });
            return { type: 'tool_result', tool_use_id: c.id, content: 'Shown to the user with a button to load it.' };
          }
          const extra = c.input && !c.input.language && ctx.language === 'es' ? { language: 'es' } : {};
          return { type: 'tool_result', tool_use_id: c.id, content: JSON.stringify(runTool(c.name, Object.assign({}, c.input, extra))) };
        } catch (e) { return { type: 'tool_result', tool_use_id: c.id, content: String(e.message || e), is_error: true }; }
      });
      convo = convo.concat([{ role: 'assistant', content: res.content }, { role: 'user', content: results }]);
    }
  } catch (e) {
    return reply({ error: 'upstream', message: String(e.message || e).slice(0, 200) }, 502);
  }
  const text = (res.content || []).filter((c) => c.type === 'text').map((c) => c.text).join('\n').trim();
  return reply({ text, cards, used, limit, guest });
}
