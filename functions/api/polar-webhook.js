// Polar → Chordseed: marks a user as Pro (or back to the beta/free state) in Supabase.
// URL: https://chordseed.pages.dev/api/polar-webhook   (Polar → Settings → Webhooks, format "Raw")
// Secrets in Cloudflare Pages: POLAR_WEBHOOK_SECRET, SUPABASE_SERVICE_ROLE_KEY
// Signature: Standard Webhooks (webhook-id, webhook-timestamp, webhook-signature "v1,<base64>").

const SB_URL = 'https://siafatxbgecgenhnciej.supabase.co';
const FOUNDER = ['d817d8e9-3f98-4a31-9585-0a50317b3484'];
const MAX_SKEW_S = 300;
const enc = new TextEncoder();

function b64ToBytes(b64) { const bin = atob(b64); const out = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i); return out; }
function bytesToB64(buf) { let s = ''; new Uint8Array(buf).forEach((b) => { s += String.fromCharCode(b); }); return btoa(s); }
function safeEq(a, b) { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; }

// Polar's SDK signs with the UTF-8 bytes of the full secret string (including any "whsec_" prefix).
// Standard Webhooks libraries instead base64-decode what follows "whsec_". Accept either so both setups work.
function secretKeys(secret) {
  const keys = [enc.encode(secret)];
  if (secret.startsWith('whsec_')) { try { keys.push(b64ToBytes(secret.slice(6))); } catch { /* not base64 */ } }
  return keys;
}

export async function verify(headers, raw, secret, nowS = Math.floor(Date.now() / 1000)) {
  const id = headers.get('webhook-id'), ts = headers.get('webhook-timestamp'), sigs = headers.get('webhook-signature');
  if (!id || !ts || !sigs || !secret) return false;
  if (Math.abs(nowS - Number(ts)) > MAX_SKEW_S) return false;
  const given = sigs.split(' ').map((p) => p.split(',')).filter((p) => p[0] === 'v1' && p[1]).map((p) => p[1]);
  for (const kb of secretKeys(secret)) {
    const key = await crypto.subtle.importKey('raw', kb, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const mac = bytesToB64(await crypto.subtle.sign('HMAC', key, enc.encode(`${id}.${ts}.${raw}`)));
    if (given.some((g) => safeEq(g, mac))) return true;
  }
  return false;
}

function userIdOf(d) {
  const c = d.customer || {};
  const id = c.external_id || (d.metadata && d.metadata.user_id) || (c.metadata && c.metadata.user_id);
  return id && /^[0-9a-f-]{36}$/i.test(id) ? id : null;
}

export function rowFromEvent(evt) {
  const type = evt && evt.type, d = (evt && evt.data) || {};
  const userId = userIdOf(d);
  if (!userId) return null;
  const now = new Date().toISOString();
  if (type && type.startsWith('subscription.')) {
    const live = ['active', 'trialing', 'past_due'].includes(d.status) && type !== 'subscription.revoked';
    return {
      user_id: userId, plan: live ? 'pro' : 'free', status: live ? d.status : 'canceled',
      current_period_end: live ? (d.current_period_end || null) : null,
      paddle_customer_id: d.customer_id ? 'polar:' + d.customer_id : null,
      paddle_subscription_id: d.id ? 'polar:' + d.id : null,
      updated_at: now,
    };
  }
  if (type === 'order.paid' && !d.subscription_id && FOUNDER.includes(d.product_id)) {
    return {
      user_id: userId, plan: 'pro', status: 'active', current_period_end: null,
      paddle_customer_id: d.customer_id ? 'polar:' + d.customer_id : null,
      paddle_subscription_id: 'founder:' + d.id, updated_at: now,
    };
  }
  if (type === 'order.refunded' && !d.subscription_id && FOUNDER.includes(d.product_id)) {
    return { user_id: userId, plan: 'free', status: 'canceled', current_period_end: null, paddle_subscription_id: 'founder:' + d.id, updated_at: now };
  }
  return null;
}

function sbHeaders(key, extra = {}) { const h = { apikey: key, ...extra }; if (!String(key).startsWith('sb_')) h.Authorization = `Bearer ${key}`; return h; }

export async function onRequestPost({ request, env }) {
  const raw = await request.text();
  if (!env.POLAR_WEBHOOK_SECRET || !env.SUPABASE_SERVICE_ROLE_KEY) return new Response('not configured', { status: 503 });
  if (!(await verify(request.headers, raw, env.POLAR_WEBHOOK_SECRET))) return new Response('bad signature', { status: 401 });
  let evt; try { evt = JSON.parse(raw); } catch { return new Response('bad json', { status: 400 }); }
  const row = rowFromEvent(evt);
  if (!row) return new Response('ignored', { status: 202 });
  if (row.plan === 'free') {
    const cur = await fetch(`${SB_URL}/rest/v1/subscriptions?user_id=eq.${row.user_id}&select=paddle_subscription_id`, { headers: sbHeaders(env.SUPABASE_SERVICE_ROLE_KEY) }).then((r) => r.ok ? r.json() : []).catch(() => []);
    const c = cur[0];
    if (c && c.paddle_subscription_id && c.paddle_subscription_id.startsWith('founder:') && c.paddle_subscription_id !== row.paddle_subscription_id) return new Response('kept founder', { status: 202 });
    if (c && c.paddle_subscription_id && c.paddle_subscription_id !== row.paddle_subscription_id) return new Response('other subscription', { status: 202 });
  }
  // While the public beta lasts, a cancelled/refunded user goes back to the free-beta Pro, not to Free.
  const BETA_END = '2027-03-01';
  if (row.plan === 'free' && new Date().toISOString() < BETA_END) Object.assign(row, { plan: 'pro', status: 'trialing', current_period_end: BETA_END, paddle_subscription_id: null, paddle_customer_id: null });
  const r = await fetch(`${SB_URL}/rest/v1/subscriptions?on_conflict=user_id`, {
    method: 'POST',
    headers: sbHeaders(env.SUPABASE_SERVICE_ROLE_KEY, { 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=minimal' }),
    body: JSON.stringify(row),
  });
  if (!r.ok) { const t = (await r.text().catch(() => '')).slice(0, 300); return new Response('db error ' + r.status + ' ' + t, { status: 500 }); }
  return new Response('ok', { status: 202 });
}

export function onRequestGet() { return new Response('Chordseed Polar webhook. POST only.', { headers: { 'content-type': 'text/plain' } }); }
