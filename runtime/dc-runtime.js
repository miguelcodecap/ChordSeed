/*!
 * Chordseed standalone runtime
 * Renders the app's .dc templates ({{holes}}, <sc-if>, <sc-for>, <dc-import>) in any browser,
 * so the app can run outside claude.ai (GitHub Pages, any static host).
 */
(function () {
  'use strict';

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (u) {
    var s = typeof u === 'function' ? u(this.state, this.props) : u;
    this.state = Object.assign({}, this.state, s || {});
    if (this.__schedule) this.__schedule();
  };
  DCLogic.prototype.forceUpdate = function () { if (this.__schedule) this.__schedule(); };
  window.DCLogic = DCLogic;

  var HOLE = /\{\{\s*([^}]*?)\s*\}\}/g;
  var ONLY = /^\s*\{\{\s*([^}]*?)\s*\}\}\s*$/;

  function literal(p) {
    if (p === 'true') return { v: true };
    if (p === 'false') return { v: false };
    if (p === 'null') return { v: null };
    if (/^-?\d+(\.\d+)?$/.test(p)) return { v: Number(p) };
    if (/^'.*'$|^".*"$/.test(p)) return { v: p.slice(1, -1) };
    return null;
  }
  function resolve(path, scope) {
    var lit = literal(path); if (lit) return lit.v;
    var parts = path.split('.'), cur = scope;
    for (var i = 0; i < parts.length; i++) { if (cur == null) return undefined; cur = cur[parts[i]]; }
    return cur;
  }
  function interp(str, scope) {
    return str.replace(HOLE, function (_, p) { var v = resolve(p, scope); return v == null || v === false ? '' : String(v); });
  }

  /* ---------- compile template DOM into descriptors ---------- */
  var UID = 0;
  function compile(node) {
    if (node.nodeType === 3) {
      var t = node.nodeValue;
      return t.indexOf('{{') >= 0 ? { k: 'text', hole: t } : { k: 'text', t: t };
    }
    if (node.nodeType !== 1) return null;
    var tag = node.localName;
    var kids = []; for (var c = node.firstChild; c; c = c.nextSibling) { var d = compile(c); if (d) kids.push(d); }
    if (tag === 'sc-if') return { k: 'if', id: ++UID, v: node.getAttribute('value'), kids: kids };
    if (tag === 'sc-for') return { k: 'for', id: ++UID, list: node.getAttribute('list'), as: node.getAttribute('as'), kids: kids };
    if (tag === 'dc-import') {
      var props = {};
      for (var a = 0; a < node.attributes.length; a++) { var at = node.attributes[a]; if (at.name !== 'name' && at.name.indexOf('hint-') !== 0) props[at.name] = at.value; }
      return { k: 'import', name: node.getAttribute('name'), props: props };
    }
    var attrs = [], evs = [];
    for (var i = 0; i < node.attributes.length; i++) {
      var A = node.attributes[i], n = A.name;
      if (n.indexOf('hint-') === 0) continue;
      if (/^on[a-z]+$/.test(n)) { var m = A.value.match(ONLY); if (m) evs.push([n.slice(2), m[1]]); continue; }
      var only = A.value.match(ONLY);
      attrs.push({ n: n, ns: A.namespaceURI, raw: only ? only[1] : null, s: A.value, dyn: A.value.indexOf('{{') >= 0 });
    }
    return { k: 'el', tag: tag, ns: node.namespaceURI, attrs: attrs, evs: evs, kids: kids };
  }

  var BOOL = { disabled: 1, checked: 1, selected: 1, hidden: 1, readonly: 1, open: 1, required: 1, multiple: 1, autofocus: 1 };

  /* ---------- build fresh DOM for a render ---------- */
  function mark(s) { var c = document.createComment(s); c.__mk = s; return c; }
  function build(descs, scope, ctx, out, pre) {
    pre = pre || '';
    for (var i = 0; i < descs.length; i++) {
      var d = descs[i];
      if (d.k === 'text') { out.push(document.createTextNode(d.hole ? interp(d.hole, scope) : d.t)); continue; }
      if (d.k === 'if') { var key = d.id + pre, cond = d.v.match(ONLY); out.push(mark('s' + key)); if (cond ? resolve(cond[1], scope) : d.v) build(d.kids, scope, ctx, out, pre); out.push(mark('e' + key)); continue; }
      if (d.k === 'for') {
        var lm = d.list.match(ONLY), list = lm ? resolve(lm[1], scope) : null;
        var fk = d.id + pre; out.push(mark('s' + fk));
        if (list && list.length) for (var j = 0; j < list.length; j++) { var sc = Object.create(scope); sc[d.as] = list[j]; out.push(mark('i' + fk + '.' + j)); build(d.kids, sc, ctx, out, pre + '.' + d.id + ':' + j); }
        out.push(mark('e' + fk));
        continue;
      }
      if (d.k === 'import') { out.push(ctx.renderImport(d, scope)); continue; }
      var el = d.ns && d.ns !== 'http://www.w3.org/1999/xhtml' ? document.createElementNS(d.ns, d.tag) : document.createElement(d.tag);
      for (var a = 0; a < d.attrs.length; a++) {
        var at = d.attrs[a], v;
        if (at.raw !== null) v = resolve(at.raw, scope); else v = at.dyn ? interp(at.s, scope) : at.s;
        if (v == null || v === false) { if (BOOL[at.n] || at.raw !== null) continue; v = ''; }
        if (BOOL[at.n]) { if (v === true || v === 'true' || v === at.n || v === '') { el.setAttribute(at.n, ''); } continue; }
        if (at.n === 'value' && (d.tag === 'input' || d.tag === 'textarea' || d.tag === 'select')) { el.__value = String(v); el.setAttribute('value', String(v)); continue; }
        if (at.ns) el.setAttributeNS(at.ns, at.n, String(v)); else el.setAttribute(at.n, v === true ? '' : String(v));
      }
      if (d.evs.length) { el.__ev = {}; for (var e = 0; e < d.evs.length; e++) { var fn = resolve(d.evs[e][1], scope); if (typeof fn === 'function') el.__ev[d.evs[e][0]] = fn; } }
      var kids = []; build(d.kids, scope, ctx, kids, pre);
      for (var k = 0; k < kids.length; k++) el.appendChild(kids[k]);
      if (el.__value !== undefined) el.value = el.__value;
      out.push(el);
    }
    return out;
  }

  /* ---------- morph live DOM toward the fresh DOM (keeps focus, scroll, listeners) ---------- */
  function bindEvents(el) {
    var ev = el.__ev; if (!ev) return;
    el.__bound = el.__bound || {};
    Object.keys(ev).forEach(function (type) {
      if (el.__bound[type]) return;
      el.__bound[type] = true;
      el.addEventListener(type, function (e) { var h = el.__ev && el.__ev[type]; if (h) return h(e); });
    });
  }
  function morphAttrs(from, to) {
    var i, a;
    for (i = from.attributes.length - 1; i >= 0; i--) { a = from.attributes[i]; if (!to.hasAttribute(a.name) && a.name !== 'data-fit') from.removeAttribute(a.name); }
    for (i = 0; i < to.attributes.length; i++) { a = to.attributes[i]; if (from.getAttribute(a.name) !== a.value) { if (a.namespaceURI) from.setAttributeNS(a.namespaceURI, a.name, a.value); else from.setAttribute(a.name, a.value); } }
    if (to.__value !== undefined && from.value !== to.__value && document.activeElement !== from) from.value = to.__value;
    from.__ev = to.__ev; bindEvents(from);
  }
  function same(a, b) { return a.nodeType === b.nodeType && !a.__mk && !b.__mk && (a.nodeType !== 1 || (a.localName === b.localName && a.namespaceURI === b.namespaceURI && !!a.__comp === !!b.__comp)); }
  function morphChildren(parent, nodes) {
    var cur = parent.firstChild, i = 0;
    for (; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.__mk) {
        var m = cur; while (m && m.__mk !== n.__mk) m = m.nextSibling;
        if (m) { while (cur !== m) { var nx0 = cur.nextSibling; parent.removeChild(cur); cur = nx0; } cur = cur.nextSibling; }
        else parent.insertBefore(n, cur);
        continue;
      }
      if (cur && same(cur, n)) {
        if (n.nodeType === 3) { if (cur.nodeValue !== n.nodeValue) cur.nodeValue = n.nodeValue; }
        else { morphAttrs(cur, n); morphChildren(cur, Array.prototype.slice.call(n.childNodes)); }
        cur = cur.nextSibling;
      } else if (cur && !cur.__mk && cur.nodeType === n.nodeType && n.nodeType !== 1) {
        cur.nodeValue = n.nodeValue; cur = cur.nextSibling;
      } else {
        if (n.nodeType === 1) bindAll(n);
        parent.insertBefore(n, cur);
      }
    }
    while (cur) { var nx = cur.nextSibling; parent.removeChild(cur); cur = nx; }
  }
  function bindAll(el) { bindEvents(el); for (var c = el.firstElementChild; c; c = c.nextElementSibling) bindAll(c); }

  /* ---------- component mounting ---------- */
  var DEFS = {};
  function define(name, templateHTML, scriptSrc) {
    var tpl = document.createElement('template'); tpl.innerHTML = templateHTML;
    var descs = []; for (var c = tpl.content.firstChild; c; c = c.nextSibling) { var d = compile(c); if (d) descs.push(d); }
    var Comp = new Function('DCLogic', scriptSrc + '\n;return typeof Component !== "undefined" ? Component : null;')(DCLogic);
    DEFS[name] = { descs: descs, Comp: Comp };
  }
  function makeCtx() {
    return {
      renderImport: function (d, scope) {
        var def = DEFS[d.name], box = document.createElement('div');
        box.style.display = 'contents'; box.__comp = true;
        if (!def) return box;
        var props = {};
        Object.keys(d.props).forEach(function (k) { var m = d.props[k].match(ONLY); props[k] = m ? resolve(m[1], scope) : d.props[k]; });
        var inst = new def.Comp(props); inst.props = props; inst.state = inst.state || {};
        var vals = inst.renderVals ? inst.renderVals() : {};
        build(def.descs, vals, this, []).forEach(function (n) { box.appendChild(n); });
        return box;
      }
    };
  }
  function mount(name, host) {
    var def = DEFS[name], inst = new def.Comp({}), ctx = makeCtx(), pending = false, mounted = false;
    inst.props = inst.props || {}; inst.state = inst.state || {};
    function render() {
      pending = false;
      var vals;
      try { vals = inst.renderVals ? inst.renderVals() : {}; } catch (e) { console.error('[chordseed] render error', e); return; }
      var nodes = build(def.descs, vals, ctx, []);
      morphChildren(host, nodes);
      if (!mounted) { mounted = true; if (inst.componentDidMount) try { inst.componentDidMount(); } catch (e) { console.error(e); } }
    }
    inst.__schedule = function () { if (!pending) { pending = true; (window.queueMicrotask || setTimeout)(render); } };
    render();
    window.addEventListener('pagehide', function () { if (inst.componentWillUnmount) try { inst.componentWillUnmount(); } catch (e) {} });
    return inst;
  }
  window.ChordseedRuntime = { define: define, mount: mount };
})();
