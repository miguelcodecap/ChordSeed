// Creates a Polar checkout for the signed-in Chordseed user and returns its URL.
// POST /api/checkout  { plan: 'month' | 'year' | 'founder' }  with header  Authorization: Bearer <supabase access token>
// Secrets in Cloudflare Pages: POLAR_ACCESS_TOKEN (Polar → Settings → Developers → New token, scopes checkouts:write)
// Optional: POLAR_SANDBOX=1 to use sandbox-api.polar.sh

const SB_URL = 'https://siafatxbgecgenhnciej.supabase.co';
const SB_KEY = 'sb_publishable_wbMAklnoQrY6-P0vM1KVlw_l0llY6fK';
const APP = 'https://chordseed.pages.dev/app/';
export const POLAR_PRODUCTS = {
  month: '18a98a24-6821-4769-894f-1255d78c18df',
  year: '93a518d5-60ad-49e3-a08f-3ce8e2924fc7',
  founder: 'd817d8e9-3f98-4a31-9585-0a50317b3484',
};

const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS' };
const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', ...cors } });

export function onRequestOptions() { return new Response(null, { status: 204, headers: cors }); }

export async function onRequestPost({ request, env }) {
  const TOKEN = env.POLAR_ACCESS_TOKEN || env.POLAR_ACCES_TOKEN; // the secret was saved with this spelling in Cloudflare
  if (!TOKEN) return json({ error: 'not_configured' }, 503);
  let body = {}; try { body = await request.json(); } catch { /* empty */ }
  const product = POLAR_PRODUCTS[body.plan];
  if (!product) return json({ error: 'bad_plan' }, 400);
  const auth = request.headers.get('authorization') || '';
  if (!auth.startsWith('Bearer ')) return json({ error: 'login' }, 401);
  const u = await fetch(`${SB_URL}/auth/v1/user`, { headers: { apikey: SB_KEY, Authorization: auth } });
  if (!u.ok) return json({ error: 'login' }, 401);
  const user = await u.json();
  if (!user || !user.id) return json({ error: 'login' }, 401);
  const api = env.POLAR_SANDBOX === '1' ? 'https://sandbox-api.polar.sh' : 'https://api.polar.sh';
  const r = await fetch(`${api}/v1/checkouts/`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${TOKEN}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      products: [product],
      external_customer_id: user.id,
      customer_email: user.email || undefined,
      metadata: { user_id: user.id, plan: body.plan },
      success_url: `${APP}?paid=1`,
    }),
  });
  const out = await r.json().catch(() => ({}));
  if (!r.ok || !out.url) return json({ error: 'upstream', detail: (out && (out.detail || out.error)) ? String(JSON.stringify(out.detail || out.error)).slice(0, 300) : r.status }, 502);
  return json({ url: out.url });
}
