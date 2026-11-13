// Chordseed connector for Claude (and any AI app that supports MCP).
// Remote MCP server, "streamable HTTP" transport, stateless: every POST is answered with plain JSON.
// Add it in Claude: Customize → Connectors → Add custom connector → https://chordseed.pages.dev/mcp
import { TOOLS, runTool } from '../server/api.js';

const VERSIONS = ['2025-11-25', '2025-06-18', '2025-03-26', '2024-11-05'];
const INFO = { name: 'chordseed', title: 'Chordseed', version: '1.0.0', websiteUrl: 'https://chordseed.pages.dev' };
const INSTRUCTIONS = 'Chordseed is a songwriting tool for musicians. Use these tools for chord progressions: suggest the next chord, analyze, reharmonize, plan key changes, pick scales to solo with, look up chords and find songs with similar chords. Every result includes a link that opens the progression in the Chordseed app, where the user can hear it on their instrument, see fingerings and save it: offer that link. Answer in the user\'s language (pass language "es" for Spanish).';
const CORS = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization, Mcp-Session-Id, Mcp-Protocol-Version', 'Access-Control-Expose-Headers': 'Mcp-Session-Id' };

function json(body, status) { return new Response(JSON.stringify(body), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json' }, CORS) }); }
function ok(id, result) { return { jsonrpc: '2.0', id, result }; }
function fail(id, code, message) { return { jsonrpc: '2.0', id: id === undefined ? null : id, error: { code, message } }; }

function handle(msg) {
  if (!msg || msg.jsonrpc !== '2.0' || typeof msg.method !== 'string') return fail(msg && msg.id, -32600, 'Invalid request');
  const isNote = msg.id === undefined || msg.id === null;
  const p = msg.params || {};
  switch (msg.method) {
    case 'initialize': {
      const v = VERSIONS.indexOf(p.protocolVersion) >= 0 ? p.protocolVersion : VERSIONS[0];
      return ok(msg.id, { protocolVersion: v, capabilities: { tools: { listChanged: false } }, serverInfo: INFO, instructions: INSTRUCTIONS });
    }
    case 'ping': return isNote ? null : ok(msg.id, {});
    case 'tools/list':
      return ok(msg.id, { tools: TOOLS.map((t) => ({ name: t.name, title: t.title, description: t.description, inputSchema: t.inputSchema, annotations: { title: t.title, readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false } })) });
    case 'tools/call': {
      try {
        const out = runTool(p.name, p.arguments || {});
        return ok(msg.id, { content: [{ type: 'text', text: JSON.stringify(out, null, 2) }], structuredContent: out, isError: false });
      } catch (e) {
        if (String(e.message).indexOf('Unknown tool') === 0) return fail(msg.id, -32602, e.message);
        return ok(msg.id, { content: [{ type: 'text', text: String(e.message || e) }], isError: true });
      }
    }
    case 'resources/list': return ok(msg.id, { resources: [] });
    case 'prompts/list': return ok(msg.id, { prompts: [] });
    default:
      if (isNote || msg.method.indexOf('notifications/') === 0) return null;
      return fail(msg.id, -32601, 'Method not found: ' + msg.method);
  }
}

export async function onRequest(context) {
  const req = context.request;
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (req.method === 'GET') {
    if ((req.headers.get('Accept') || '').indexOf('text/event-stream') >= 0) return new Response('This server does not open an SSE stream.', { status: 405, headers: Object.assign({ Allow: 'POST' }, CORS) });
    return new Response('Chordseed MCP server. Add https://chordseed.pages.dev/mcp as a custom connector in Claude.', { status: 200, headers: Object.assign({ 'Content-Type': 'text/plain; charset=utf-8' }, CORS) });
  }
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: Object.assign({ Allow: 'POST, GET, OPTIONS' }, CORS) });
  let body;
  try { body = await req.json(); } catch (e) { return json(fail(null, -32700, 'Parse error'), 400); }
  if (Array.isArray(body)) {
    const out = body.map(handle).filter(Boolean);
    return out.length ? json(out) : new Response(null, { status: 202, headers: CORS });
  }
  const res = handle(body);
  return res ? json(res) : new Response(null, { status: 202, headers: CORS });
}
