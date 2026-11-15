// Paddle → Chordseed: marks a user as Pro (or back to Free) in Supabase after a payment event.
// URL: https://chordseed.pages.dev/api/paddle-webhook
// Needs two secrets in Cloudflare Pages → Settings → Variables and Secrets:
//   PADDLE_WEBHOOK_SECRET      (Paddle → Developer tools → Notifications → your destination → secret key)
//   SUPABASE_SERVICE_ROLE_KEY  (Supabase → Project Settings → API keys → secret / service_role)
// Optional: PADDLE_FOUNDER_PRICE_IDS = comma-separated price ids treated as lifetime (defaults below).

const SB_URL = 'https://siafatxbgecgenhnciej.supabase.co';
const FOUNDER_DEFAULT = ['pri_01m7ea7n4pv2kyh2d9vvbskngj'];
const MAX_SKEW_S = 300;

const enc = new TextEncoder();
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');

function safeEq(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

export async function verifySignature(header, raw, secret, nowS = Math.floor(Date.now() / 1000)) {
  if (!header || !secret) return false;
  const parts = Object.fromEntries(header.split(';').map((p) => p.split('=').map((x) => x.trim())).filter((p) => p.length === 2));
  const ts = parts.ts;
  const sigs = header.split(';').map((p) => p.trim()).filter((p) => p.startsWith('h1=')).map((p) => p.slice(3));
  if (!ts || !sigs.length) return false;
  if (Math.abs(nowS - Number(ts)) > MAX_SKEW_S) return false;
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const mac = hex(await crypto.subtle.sign('HMAC', key, enc.encode(ts + ':' + raw)));
  return sigs.some((s) => safeEq(s, mac));
}

// Turns a Paddle event into the row we store, or null if the event doesn't change anything.
export function rowFromEvent(evt, founderIds = FOUNDER_DEFAULT) {
  const type = evt && evt.event_type;
  const d = (evt && evt.data) || {};
  const userId = d.custom_data && d.custom_data.user_id;
  if (!userId || !/^[0-9a-f-]{36}$/i.test(userId)) return null;

  if (type && type.startsWith('subscription.')) {
    const status = d.status; // active | trialing | past_due | paused | canceled
    const live = ['active', 'trialing', 'past_due'].includes(status);
    const end = (d.current_billing_period && d.current_billing_period.ends_at) || null;
    return {
      user_id: userId,
      plan: live ? 'pro' : 'free',
      status: live ? status : 'canceled',
      current_period_end: live ? end : null,
      paddle_customer_id: d.customer_id || null,
      paddle_subscription_id: d.id || null,
      updated_at: new Date().toISOString(),
    };
  }

  if (type === 'transaction.completed' && !d.subscription_id) {
    const items = Array.isArray(d.items) ? d.items : [];
    const founder = items.some((it) => it && it.price && founderIds.includes(it.price.id));
    if (!founder) return null;
    return {
      user_id: userId,
      plan: 'pro',
      status: 'active',
      current_period_end: null, // lifetime
      paddle_customer_id: d.customer_id || null,
      paddle_subscription_id: 'founder:' + d.id,
      updated_at: new Date().toISOString(),
    };
  }
  return null;
}

async function currentRow(env, userId) {
  const r = await fetch(`${SB_URL}/rest/v1/subscriptions?user_id=eq.${userId}&select=paddle_subscription_id,plan`, {
    headers: { apikey: env.SUPABASE_SERVICE_ROLE_KEY, Authorization: `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}` },
  });
  if (!r.ok) return null;
  const rows = await r.json();
  return rows[0] || null;
}

export async function onRequestPost({ request, env }) {
  const raw = await request.text();
  if (!env.PADDLE_WEBHOOK_SECRET || !env.SUPABASE_SERVICE_ROLE_KEY) return new Response('not configured', { status: 503 });
  const ok = await verifySignature(request.headers.get('Paddle-Signature'), raw, env.PADDLE_WEBHOOK_SECRET);
  if (!ok) return new Response('bad signature', { status: 401 });

  let evt;
  try { evt = JSON.parse(raw); } catch { return new Response('bad json', { status: 400 }); }
  const founderIds = env.PADDLE_FOUNDER_PRICE_IDS ? env.PADDLE_FOUNDER_PRICE_IDS.split(',').map((s) => s.trim()) : FOUNDER_DEFAULT;
  const row = rowFromEvent(evt, founderIds);
  if (!row) return new Response('ignored', { status: 200 });

  // A lifetime Founder purchase is never downgraded by an old subscription ending.
  if (row.plan === 'free') {
    const cur = await currentRow(env, row.user_id);
    if (cur && cur.paddle_subscription_id && cur.paddle_subscription_id.startsWith('founder:')) return new Response('kept founder', { status: 200 });
    if (cur && cur.paddle_subscription_id && cur.paddle_subscription_id !== row.paddle_subscription_id) return new Response('other subscription', { status: 200 });
  }

  const r = await fetch(`${SB_URL}/rest/v1/subscriptions?on_conflict=user_id`, {
    method: 'POST',
    headers: {
      apikey: env.SUPABASE_SERVICE_ROLE_KEY,
      Authorization: `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
      Prefer: 'resolution=merge-duplicates,return=minimal',
    },
    body: JSON.stringify(row),
  });
  if (!r.ok) return new Response('db error', { status: 500 }); // Paddle retries
  return new Response('ok', { status: 200 });
}

export function onRequestGet() {
  return new Response('Chordseed Paddle webhook. POST only.', { status: 200, headers: { 'content-type': 'text/plain' } });
}
