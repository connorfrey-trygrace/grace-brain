// Grace Q&A Board — a read-only overlay for the AhaSlides presenter.
// Runs as a bookmarklet inside a logged-in presenter.ahaslides.com tab.
// Reads /api/question/list (GET only — never writes to AhaSlides), lets a
// moderator curate what shows, and drives a separate display window for the projector.
(() => {
  const VERSION = '__BUILD_VERSION__';
  // Same build already running: show/hide it. Older build: tear it down and start fresh,
  // so re-installing the bookmark takes effect without reloading AhaSlides.
  if (window.__graceQA) {
    if (window.__graceQA.version === VERSION) { window.__graceQA.toggle(); return; }
    try { window.__graceQA.destroy ? window.__graceQA.destroy() : document.getElementById('gqa')?.remove(); } catch {}
    document.getElementById('gqa-css')?.remove();
  }

  const m = location.pathname.match(/presentation\/(\d+)/);
  if (location.host !== 'presenter.ahaslides.com' || !m) {
    alert('Open your AhaSlides presentation (presenter.ahaslides.com/presentation/…) first, then click the bookmarklet.');
    return;
  }
  const PID = m[1];
  const KEY = 'graceQA:' + PID;
  const POLL_MS = 4000;

  const C = { stable: '#1C3B6B', active: '#2F97A0', cinder: '#ABABAB', cloud: '#E3E3E3', ink: '#1C3B6B' };

  // Brand: Grace Brand Guideline 2019 — four colors only, Lato (the book's free face),
  // Light headers vs heavy wide-tracked small caps; logo reversed to white on Stable Blue (p16),
  // >=144px wide on screen (p17), clear space >= the width of the "g" on every side (p18).
  const LOGO = '__LOGO_DATA_URI__';
  const joinMatch = (document.body.innerText.match(/ahaslides\.com\/[A-Z0-9]{3,}/) || [])[0];

  const defaults = { featured: [], hero: null, hidden: [], custom: [], showVotes: false, latestMode: 'popup', showTop: true, showThemes: true, themeMetric: 'count', tagOverride: {}, mode: 'featured',
    heading: "You've been asking", sub: 'Sunday Night Q&A' };
  let S;
  try { S = Object.assign({}, defaults, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch { S = { ...defaults }; }
  if (S.sub === 'Questions from the room') S.sub = defaults.sub;
  S.tagOverride = S.tagOverride || {};   // question id -> [tag keys]; replaces the old single-category overrides
  if (!S.relatedV) { S.mode = 'related'; S.relatedV = 1; }   // one-time switch to the new default
  if (!S.latestV) { S.latestMode = 'always'; S.latestV = 1; }  // latest question lives in the footer now
  if ('showLatest' in S) { if (S.showLatest === false) S.latestMode = 'off'; delete S.showLatest; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch {} };

  let questions = [];          // approved, not deleted, not private
  let lastOk = null, lastErr = null;
  const seenAtOpen = new Set();
  let firstLoad = true;
  let filter = 'all', search = '', catFilter = '';   // catFilter: a tag key, 'none' (untagged) or ''
  let displayWin = null;

  // Live room signals, mirrored from what AhaSlides itself shows the presenter:
  // people online + "Participants are typing" are read from AhaSlides' own widgets on this page
  // (they keep running under the overlay); reaction totals come from its sync store.
  const STATS_MS = 2000;
  const REACTION_SLIDE = 1;   // reaction counters are kept per slide; the Q&A slide is slide 1 in this deck
  const EMOJI = { heart: '❤️', like: '👍', laugh: '😂', wow: '😮', sad: '😢' };
  const live = { online: null, typing: 0, reactions: null };

  // Typing: AhaSlides' presenter keeps a socket.io connection open (edit or present mode) and
  // receives "user-is-typing" -> [participantId, true] when someone starts typing a question,
  // repeated about every 16s while they keep going; there is no "stopped" event. We attach a
  // listen-only handler to that same socket (found through the page's webpack runtime) and
  // count participants heard from in the last TYPING_MS. Nothing is ever emitted.
  const TYPING_MS = 17000;
  const typers = new Map();   // participantId -> last heard (ms)
  let typingSock = null, hookTries = 0;
  const onTyping = (a, b) => {
    const [id, flag] = Array.isArray(a) ? a : [a, b];
    if (flag === false) typers.delete(id); else typers.set(id || 'anon', Date.now());
    pollTyping();
  };
  function hookTyping() {
    if (typingSock) return true;
    if (hookTries++ > 5) return false;   // scanning the module table isn't free: give up after a few tries
    try {
      const key = Object.keys(window).find(k => /^webpackChunk/.test(k));
      if (!key) return false;
      let req = null;
      window[key].push([[Symbol('graceQA')], {}, r => { req = r; }]);
      const id = req && Object.keys(req.m).find(m => { const src = String(req.m[m]); return src.length < 5000 && src.includes('getSocket') && src.includes('setSocketId'); });
      if (!id) return false;
      const mod = req(id), svc = Object.values(mod).find(x => x && typeof x.getSocket === 'function');
      const sock = svc && svc.getSocket();
      if (!sock || typeof sock.on !== 'function') return false;
      sock.on('user-is-typing', onTyping);
      typingSock = sock;
      return true;
    } catch { return false; }
  }
  function pollTyping() {
    const now = Date.now();
    for (const [id, t] of typers) if (now - t > TYPING_MS) typers.delete(id);
    // fall back to AhaSlides' own bubble (present mode) if the socket hook is unavailable
    live.typing = typers.size || (document.querySelector('.chat-bubble.show') ? 1 : 0);
    renderStats();
  }
  async function pollStats() {
    const os = document.querySelector('.user-online-status');
    const n = os ? parseInt(os.parentElement.textContent.replace(/\D/g, ''), 10) : NaN;
    live.online = Number.isFinite(n) ? n : null;
    if (!typingSock) hookTyping();
    pollTyping();
    try {
      const path = `/ST2/livestats-default-prd-us01/REACTION_COUNT/PER_REACTION_TYPE/${PID}/${REACTION_SLIDE}`;
      const r = await fetch('/api/aha-sync/kv/paths?path=' + encodeURIComponent(path), { credentials: 'include', method: 'GET', cache: 'no-store' });
      if (r.ok) {
        const next = {};
        for (const kv of (await r.json()).keysvalues || []) next[kv.key.split('/').pop()] = +kv.value || 0;
        if (live.reactions) for (const [k, v] of Object.entries(next)) {
          const burst = Math.min(v - (live.reactions[k] || 0), 8);   // cap a flood to 8 floaters per type
          for (let i = 0; i < burst; i++) setTimeout(() => floatReaction(k), i * 180);
        }
        live.reactions = next;
      }
    } catch {}
    renderStats();
  }

  // ---------- data ----------
  async function poll() {
    try {
      const r = await fetch('/api/question/list/?id=' + PID, { credentials: 'include', method: 'GET', cache: 'no-store' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const all = await r.json();
      const next = all.filter(q => q.status === 'approved' && !q.deleted && !q.isPrivate);
      if (firstLoad) { next.forEach(q => seenAtOpen.add(q.id)); firstLoad = false; }
      else next.filter(q => !knownIds.has(q.id) && !S.hidden.includes(q.id)).forEach(q => { popQueue.push(q); lastArrival = q.id; });
      popQueue.splice(0, Math.max(0, popQueue.length - 3));   // a burst only replays the newest 3
      if (knownIds.size && next.some(q => !knownIds.has(q.id)) && typers.size) {
        const oldest = [...typers.entries()].sort((a, b) => a[1] - b[1])[0][0]; typers.delete(oldest);
      }
      next.forEach(q => knownIds.add(q.id));
      const sig = JSON.stringify(next.map(q => [q.id, q.title, q.voteCount, q.answered]));
      questions = next;
      lastOk = new Date(); lastErr = null;
      // only rebuild when something changed, so a poll never swallows a click mid-press
      if (sig === lastSig) { renderStatus(); return; }
      lastSig = sig;
    } catch (e) { lastErr = e.message; renderStatus(); return; }
    render();
  }
  let lastSig = null;
  const knownIds = new Set(), popQueue = [];
  let lastArrival = null;   // id of the newest question that arrived while the board was open
  let popping = false;
  const POP_MS = 8000;
  const statusText = () => lastErr ? `Can't reach AhaSlides (${lastErr}) — retrying` : lastOk ? `Live · updated ${lastOk.toLocaleTimeString()}` : 'Connecting…';
  function renderStatus() {
    const n = panel && panel.querySelector('.st:not(.live)');
    if (n) { n.textContent = statusText(); n.className = 'st' + (lastErr ? ' err' : ''); }
  }

  const byId = id => typeof id === 'string'
    ? S.custom.find(c => c.id === id)
    : questions.find(q => q.id === id);
  const textOf = item => item ? (item.title ?? item.text) : '';
  // every audience question is attributed; host cards (string ids) are not
  const whoOf = item => !item || typeof item.id === 'string' ? '' : (item.audienceName || '').trim() || 'Anon';

  // "Same category": every other question in the QOTN's category (answered or not), most-voted
  // first. Two cards on screen; every SWAP_MS one of them (alternating left/right) fades out and
  // the next question in the category fades in, so the board changes gradually, never all at once.
  const SWAP_MS = 7000, FADE_MS = 1400;
  const rel = { heroId: null, slots: [], next: 0, turn: 0 };
  function relatedPool() {
    const hero = byId(S.hero);
    if (!hero || typeof hero.id === 'string') return [];   // host card: no category to follow
    const k = mainTag(hero);
    if (!k) return [];
    return questions.filter(q => q.id !== hero.id && !S.hidden.includes(q.id) && tagsOf(q).includes(k))
      .sort((a, b) => b.voteCount - a.voteCount);
  }
  // keep the two slots valid (hero changed, a question hidden or re-categorised) without reshuffling
  function syncSlots() {
    const pool = relatedPool(), ids = pool.map(q => q.id);
    if (rel.heroId !== S.hero) { rel.heroId = S.hero; rel.slots = []; rel.next = 0; rel.turn = 0; }
    rel.slots = rel.slots.filter(id => ids.includes(id));
    while (rel.slots.length < Math.min(2, pool.length)) {
      const cand = pool.find((q, i) => i >= rel.next && !rel.slots.includes(q.id)) || pool.find(q => !rel.slots.includes(q.id));
      rel.slots.push(cand.id); rel.next = (ids.indexOf(cand.id) + 1) % pool.length;
    }
    return pool;
  }
  function swapOne() {
    if (S.mode !== 'related') return;
    const pool = syncSlots();
    if (pool.length <= 2) return;
    const ids = pool.map(q => q.id);
    let i = rel.next % pool.length, guard = 0;
    while (rel.slots.includes(ids[i]) && guard++ < pool.length) i = (i + 1) % pool.length;
    rel.slots[rel.turn % rel.slots.length] = ids[i];
    rel.next = (i + 1) % pool.length;
    rel.turn ^= 1;
    renderDisplay();
  }
  function boardItems() {
    if (S.mode === 'related') { syncSlots(); return rel.slots.map(byId).filter(Boolean); }
    if (S.mode === 'live') {
      return questions.filter(q => !q.answered && !S.hidden.includes(q.id) && q.id !== S.hero)
        .sort((a, b) => b.voteCount - a.voteCount).slice(0, 6);
    }
    return S.featured.filter(id => id !== S.hero).map(byId).filter(Boolean);
  }
  // highest-voted unanswered question not already on screen (answered ones keep their old
  // totals, so they would otherwise sit here all night)
  function topItem() {
    const shown = new Set([S.hero, ...(S.mode === 'related' ? [] : boardItems().map(x => x.id))]);
    return questions.filter(q => !q.answered && !S.hidden.includes(q.id) && !shown.has(q.id))
      .sort((a, b) => b.voteCount - a.voteCount)[0] || null;
  }
  // newest audience question not already on screen and not hidden
  function latestItem() {
    const shown = new Set([S.hero, ...(S.mode === 'related' ? [] : boardItems().map(x => x.id))]);
    return questions.filter(q => !S.hidden.includes(q.id) && !shown.has(q.id))
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))[0] || null;
  }

  // ---------- helpers ----------
  const el = (doc, tag, attrs = {}, ...kids) => {
    const n = doc.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'style') n.style.cssText = v;
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) n.setAttribute(k, v);
    }
    for (const k of kids.flat()) if (k != null) n.append(k.nodeType ? k : doc.createTextNode(String(k)));
    return n;
  };
  const toggleIn = (arr, id) => arr.includes(id) ? arr.filter(x => x !== id) : [...arr, id];
  const move = (id, d) => {
    const i = S.featured.indexOf(id), j = i + d;
    if (i < 0 || j < 0 || j >= S.featured.length) return;
    [S.featured[i], S.featured[j]] = [S.featured[j], S.featured[i]];
  };
  const THUMB = 'M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3';
  const thumb = doc => {
    const ns = 'http://www.w3.org/2000/svg', svg = doc.createElementNS(ns, 'svg'), p = doc.createElementNS(ns, 'path');
    for (const [k, v] of Object.entries({ viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2.2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'thumb', 'aria-hidden': 'true' })) svg.setAttribute(k, v);
    p.setAttribute('d', THUMB); svg.append(p); return svg;
  };
  const act = fn => (e) => { e.stopPropagation(); fn(); save(); render(); };

  const FONT = "https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap";

  // ---------- tags ----------
  // Every question carries 1–3 tags; the first is its main tag. Seeded by hand for every question
  // on the board as of 2026-09-24 (Workflows/qa-board/tag-seed.json, keyed by the first 60
  // characters of the normalised text); newer questions get up to 3 tags from the keyword rules
  // below, and the moderator can re-tag any row. There is no catch-all: an unmatched question
  // shows as Untagged in the panel until someone tags it.
  const TAG_SEED = __TAG_SEED__;
  const TAGS = [   // listed in keyword-rule priority: the first match becomes the main tag
    { k: 'HG', n: 'Hearing God', re: /hear (from )?god|god.?s voice|voice of god|speak(ing|s)? to me|talking to me|inner voice/ },
    { k: 'SP', n: 'The Holy Spirit', re: /holy spirit|\bspirit\b|advocate|gifts of|presence/ },
    { k: 'DI', n: 'Discernment & decisions', re: /discern|decision|decide|direction|clarity|say .?no\b/ },
    { k: 'SU', n: 'Suffering & pain', re: /suffer|pain|traged|trauma|bad things|evil\b|cancer|grief|abuse/ },
    { k: 'CA', n: 'Does God care about me?', re: /care about (me|us)|n.?t care|does god care|abandon|alone|not enough|love me/ },
    { k: 'WO', n: 'Worry & anxiety', re: /worr|anxi|\bfear\b|afraid|peace|stress|panic/ },
    { k: 'SA', n: 'Salvation & the only way', re: /only way|other religion|never heard|plural|\bhell\b|heaven|saved|salvation|predestin|doomed/ },
    { k: 'DE', n: 'Death & the end times', re: /\bdie\b|death|dying|end times|rapture|afterlife/ },
    { k: 'SC', n: 'Science & faith', re: /scien|evolution|fossil|dinosaur|big bang|climate|energy|universe/ },
    { k: 'BI', n: 'The Bible', re: /bible|scripture|\bverse|genesis|psalm|matthew|\bluke\b|corinth|romans|parable|jonah|noah|adam|\beve\b|testament/ },
    { k: 'RE', n: 'Dating, sex & marriage', re: /dating|\bdate\b|marri|spouse|husband|wife|\bsex|intimate|boyfriend|girlfriend/ },
    { k: 'SI', n: 'Sin & forgiveness', re: /\bsin\b|sins\b|sinful|temptation|porn|addict|forgiv|repent|guilt|shame/ },
    { k: 'PU', n: 'Purpose & calling', re: /purpose|calling|called|meaning of (my )?life|urgen|career|vocation/ },
    { k: 'CO', n: "God's control & free will", re: /control|sovereign|free will|destiny|\bfate\b|passive|plan for/ },
    { k: 'DO', n: 'Faith & doubt', re: /doubt|losing faith|unbelie|paradox|answerable|skeptic/ },
    { k: 'GO', n: 'Who God is', re: /what god looks|nature of god|trinity|listen to everyone|god is like/ },
    { k: 'JE', n: 'Who Jesus is', re: /son of god|resurrect|crucif|was (jesus|christ)|jesus (was|is) /},
    { k: 'SH', n: 'Sharing your faith', re: /share|spread|gospel|evangel|influence|witness|tell (other|people)|follow jesus/ },
    { k: 'MO', n: 'Money & work', re: /money|financ|tith|debt|\bjob\b|salary|steward/ },
    { k: 'GR', n: 'Life at Grace', re: /at grace|grace (church|community)|small group|young professional|volunteer|ministr/ },
    { k: 'CH', n: 'Church & worship', re: /church|service|worship|communion|baptis|sunday|\bpray|praise|sabbath|attend/ },
    { k: 'SE', n: "Sunday's message", re: /sermon|message|last week|football|pastor said|you said/ },
    { k: 'WB', n: 'Words & names', re: /who (is|are|was) |what does .{0,25}mean|nephilim|jireh|\bamen\b|in jesus.? name/ },
    { k: 'CU', n: 'Faith & culture', re: /culture|mainstream|america|politic|documentary|society|secular/ },
    { k: 'LI', n: 'Everyday faith', re: /busy|friends|peers|teen|kids|parent|family|gentle|kind\b|everyday|handle/ },
    { k: 'FO', n: 'Formation & habits', re: /habit|shape|formation|\bgrow|disciplin|abide|prune|routine|daily|distract|rhythm|practice|\bseek|duty|motivation/ },
  ];
  const TAG_NAME = Object.fromEntries(TAGS.map(t => [t.k, t.n]));
  const normText = t => String(t).replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim()
    .replace(/^["']+|["']+$/g, '').trim().toLowerCase();   // some rows arrive wrapped in quotes
  function tagsOf(q) {
    if (!q || typeof q.id === 'string') return [];
    const o = S.tagOverride[q.id];
    if (Array.isArray(o)) return o.filter(k => TAG_NAME[k]);
    const t = normText(q.title), seeded = TAG_SEED[t.slice(0, 60)];
    if (seeded) return seeded;
    return TAGS.filter(x => x.re.test(t)).slice(0, 3).map(x => x.k);
  }
  const mainTag = q => tagsOf(q)[0] || null;
  function themeRanking() {
    const acc = {};
    for (const q of questions) {
      if (S.hidden.includes(q.id) || q.answered) continue;   // tags reflect only what's still waiting for an answer
      for (const k of tagsOf(q)) acc[k] = (acc[k] || 0) + (S.themeMetric === 'votes' ? q.voteCount : 1);
    }
    return Object.entries(acc).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([k, v]) => ({ k, v }));
  }

  // ---------- display (projector) ----------
  const DISPLAY_CSS = `
    *{box-sizing:border-box;margin:0;padding:0}
    html,body{height:100%;background:${C.stable};color:#fff;font-family:Lato,system-ui,sans-serif;overflow:hidden}
    .wrap{height:100%;display:flex;flex-direction:column;padding:5vh 5.5vw 4vh}
    .top{display:flex;justify-content:space-between;align-items:flex-start}
    .logo{width:13vw;min-width:144px;height:auto;display:block;margin-bottom:2.8vw}
    .meta{display:flex;flex-direction:column;align-items:flex-end;gap:1.2vh;padding-top:.6vw}
    .eyebrow{display:flex;align-items:center;gap:1vw;font-weight:900;font-size:1.05vw;letter-spacing:.16em;text-transform:uppercase;color:${C.cinder}}
    .livedot{display:inline-flex;align-items:center;gap:.5vw;color:#fff}
    .livedot i{width:.7vw;height:.7vw;border-radius:50%;background:${C.active};box-shadow:0 0 0 0 ${C.active};animation:ping 1.8s infinite}
    @keyframes ping{0%{box-shadow:0 0 0 0 ${C.active}}70%{box-shadow:0 0 0 .9vw transparent}100%{box-shadow:0 0 0 0 transparent}}
    .stats{display:flex;align-items:flex-end;gap:1.8vw}
    .stat{display:flex;flex-direction:column;align-items:flex-end;gap:.4vh}
    .lbl{font-weight:900;font-size:.8vw;letter-spacing:.16em;text-transform:uppercase;color:${C.cinder}}
    .num{font-weight:900;font-size:1.7vw;line-height:1;display:inline-block;transition:color .6s}
    .num.tick{animation:tick .7s ease-out;color:${C.active}}
    @keyframes tick{0%{transform:scale(1)}30%{transform:scale(1.45)}100%{transform:scale(1)}}
    .reacts{display:flex;gap:.5vw;font-size:1.6vw;line-height:1}
    .reacts span{display:inline-block;transition:transform .25s}
    .reacts span.pop{transform:scale(1.7) translateY(-.3vw)}
    .floater{position:fixed;bottom:-6vh;font-size:4vw;pointer-events:none;z-index:5;animation:rise 4.2s cubic-bezier(.3,.6,.4,1) forwards}
    @keyframes rise{0%{transform:translate(0,0) scale(.5);opacity:0}10%{opacity:1;transform:translate(0,-8vh) scale(1)}50%{transform:translate(var(--dx),-50vh) scale(1.05)}100%{transform:translate(calc(var(--dx) * -1),-100vh) scale(1.1);opacity:0}}
    .body{flex:1;min-height:0;display:flex;gap:3vw}
    .main{flex:1;min-width:0;display:flex;flex-direction:column}
    .hero{padding:.4vh 0 .4vh 2vw;border-left:.45vw solid ${C.active};animation:breathe 5s ease-in-out infinite}
    @keyframes breathe{0%,100%{border-left-color:${C.active}}50%{border-left-color:${C.cloud}}}
    .hero .q{font-weight:300;font-size:3.3vw;line-height:1.15;margin-top:1vh}
    .tag{font-weight:900;font-size:1.05vw;letter-spacing:.16em;text-transform:uppercase;color:${C.active}}
    .label{margin-top:3vh}
    .grid{position:relative;margin-top:1.6vh;display:grid;grid-template-columns:1fr 1fr;gap:1.6vh 1.4vw;align-content:start;align-items:start;flex:1;min-height:0;overflow:hidden}
    .card{border:2px solid ${C.cinder};border-radius:.5vw;padding:1.5vh 1.3vw;font-size:1.45vw;line-height:1.28;display:flex;gap:1vw;align-items:flex-start;justify-content:space-between}
    .card.host{background:${C.active};border-color:${C.active}}
    .card.enter{animation:enter .7s cubic-bezier(.2,.8,.2,1) both}
    @keyframes enter{0%{opacity:0;transform:translateY(3vh) scale(.97);border-color:${C.active}}60%{border-color:${C.active}}100%{opacity:1;transform:none}}
    /* rotation is a quiet crossfade, no motion and no teal: teal + movement means "new submission" */
    .slotcard{display:grid}
    .slotcard.in{animation:slotin 1.4s ease-in-out both}
    @keyframes slotin{from{opacity:0}to{opacity:1}}
    .layer{grid-area:1/1;display:flex;gap:1vw;align-items:flex-start;justify-content:space-between}
    .layer.long{font-size:1.2vw}
    /* old text leaves first, new text follows: the box stays put, the two never overlap */
    .layer.lout{animation:slotout ${Math.round(FADE_MS * .4)}ms ease-in both}
    .layer.lin{animation:slotin ${Math.round(FADE_MS * .6)}ms ease-out ${Math.round(FADE_MS * .4)}ms both}
    @keyframes slotout{from{opacity:1}to{opacity:0}}
    .fade{animation:fade .6s ease-out both}
    @keyframes fade{from{opacity:0;transform:translateY(1vh)}to{opacity:1;transform:none}}
    .votes,.slot .n{display:inline-flex;align-items:center;gap:.35em}
    .votes{flex:none;font-weight:700;color:${C.cloud};font-size:1.2vw}
    .thumb{width:1em;height:1em;flex:none;transform:translateY(-.06em)}
    .side{width:24vw;flex:none;display:flex;flex-direction:column;border-left:2px solid ${C.cinder};padding-left:2vw}
    .side .sub{font-weight:900;font-size:.8vw;letter-spacing:.16em;text-transform:uppercase;color:${C.cinder};margin-top:.6vh}
    .themes{list-style:none;margin-top:2.4vh;display:flex;flex-direction:column;gap:2.2vh;position:relative}
    .th{position:relative}
    .th .row{display:flex;align-items:baseline;gap:.8vw}
    .th .rk{font-weight:900;font-size:1vw;color:${C.cinder};width:1.4vw}
    .th .nm{flex:1;font-size:1.3vw;line-height:1.2}
    .th .v{font-weight:900;font-size:1.4vw;display:inline-block}
    .th .bar{height:.55vh;background:${C.cinder};border-radius:1vh;margin:1vh 0 0 2.2vw;overflow:hidden}
    .th .bar i{display:block;height:100%;background:${C.active};border-radius:1vh;transition:width 1s cubic-bezier(.2,.8,.2,1)}
    .th.bump .v{animation:tick .7s ease-out;color:${C.active}}
    .th.lead .nm{font-weight:900}
    .foot{display:flex;justify-content:space-between;align-items:flex-start;gap:2.6vw;border-top:2px solid ${C.cinder};padding-top:2vh;margin-top:2vh}
    .slot{min-width:0;flex:1;border-radius:.5vw;margin:-1vh -1vw;padding:1vh 1vw}
    .by{font-weight:900;font-size:.75vw;letter-spacing:.16em;text-transform:uppercase;color:${C.cinder};margin-top:.7vh}
    .hero .by{margin-top:1.2vh}
    .card.host .by,.toast .by{color:#fff}
    .slot .who{font-weight:900;font-size:.75vw;color:${C.cinder};letter-spacing:.16em;margin-left:.9vw}
    .slot .who::before{content:'· ';color:${C.cinder}}
    .slot.hit{animation:hit 3.2s ease-out}
    .slot.hit .tag{animation:hitTag 3.2s ease-out}
    .slot.hit .t{animation:hitText .8s cubic-bezier(.2,.8,.2,1) both}
    @keyframes hit{0%{background:${C.active};transform:scale(1.04)}15%{transform:scale(1)}70%{background:${C.active}}100%{background:transparent}}
    @keyframes hitTag{0%,70%{color:#fff}100%{color:${C.active}}}
    @keyframes hitText{from{opacity:0;transform:translateX(-2vw)}to{opacity:1;transform:none}}
    .slot .head{display:flex;align-items:center;white-space:nowrap;overflow:hidden}
    .slot .t{font-size:1.7vw;line-height:1.25;color:#fff;margin-top:.6vh;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
    .slot .n{font-weight:900;color:${C.cloud};letter-spacing:0;margin-left:.8vw}
    .slot.hit .n,.slot.hit .who,.slot.hit .who::before{color:#fff}
    .typing{display:none;align-items:center;justify-content:flex-end;gap:.8vw;font-weight:900;font-size:1.05vw;letter-spacing:.16em;text-transform:uppercase;color:${C.active};margin-bottom:.8vh}
    .typing.on{display:flex}
    .dots{display:inline-flex;gap:.35vw}
    .dots i{width:.55vw;height:.55vw;border-radius:50%;background:${C.active};animation:blink 1.2s infinite}
    .dots i:nth-child(2){animation-delay:.2s}.dots i:nth-child(3){animation-delay:.4s}
    @keyframes blink{0%,80%,100%{opacity:.25}40%{opacity:1}}
    .join{flex:none;text-align:right}
    .join .url{display:block;font-weight:900;font-size:2.4vw;letter-spacing:.04em;color:#fff;margin-top:.6vh}
    .toast{position:fixed;left:5.5vw;right:5.5vw;bottom:4vh;z-index:4;background:${C.active};border-radius:.5vw;padding:2.4vh 2vw;transform:translateY(160%);transition:transform .5s cubic-bezier(.2,.8,.2,1)}
    .toast.on{transform:translateY(0)}
    .toast .tag{color:#fff}
    .toast .t{font-size:2.8vw;line-height:1.25;margin-top:.8vh}
    .empty{color:${C.cinder};font-size:1.6vw;font-weight:300}
  `;

  // The display is built once, then each region updates in place with its own key, so a vote
  // ticking over animates one number instead of redrawing (and re-animating) the whole board.
  let D = null;   // { d, keys:{}, prevCards:Set }
  function openDisplay() {
    if (displayWin && !displayWin.closed) { displayWin.focus(); return; }
    displayWin = window.open('/robots.txt', 'graceQADisplay', 'width=1280,height=720');
    if (!displayWin) { alert('Pop-up blocked — allow pop-ups for presenter.ahaslides.com and try again.'); return; }
    const started = Date.now();
    const whenLoaded = () => {
      let ready = false;
      try { ready = displayWin.location.pathname === '/robots.txt' && displayWin.document.readyState === 'complete'; } catch {}
      if (ready) buildDisplay();
      else if (Date.now() - started < 10000) setTimeout(whenLoaded, 50);
      else alert('The display window did not load — close it and click Open display window again.');
    };
    whenLoaded();
  }

  function buildDisplay() {
    const d = displayWin.document;
    d.open();
    d.write(`<!doctype html><html><head><title>Grace · Sunday Night Q&A</title><link rel="stylesheet" href="${FONT}"><style>${DISPLAY_CSS}</style></head><body></body></html>`);
    d.close();
    try { displayWin.history.replaceState(null, '', '/grace-sunday-night-qa'); } catch {}
    d.body.append(
      el(d, 'div', { class: 'wrap' },
        el(d, 'div', { class: 'top' },
          el(d, 'img', { class: 'logo', src: LOGO, alt: 'Grace Community Church' }),
          el(d, 'div', { class: 'meta' },
            el(d, 'div', { class: 'eyebrow' }, el(d, 'span', { id: 'sub' }), el(d, 'span', { class: 'livedot' }, el(d, 'i'), 'Live')),
            el(d, 'div', { class: 'stats' },
              el(d, 'div', { class: 'stat' }, el(d, 'span', { class: 'lbl' }, 'Online'), el(d, 'span', { class: 'num', id: 'online' }, '–')),
              el(d, 'div', { class: 'stat' }, el(d, 'span', { class: 'lbl' }, 'Questions'), el(d, 'span', { class: 'num', id: 'qcount' }, '–')),
              el(d, 'div', { class: 'stat' }, el(d, 'span', { class: 'lbl' }, 'Votes'), el(d, 'span', { class: 'num', id: 'vcount' }, '–'))))),
        el(d, 'div', { class: 'body' },
          el(d, 'div', { class: 'main' }, el(d, 'div', { id: 'hero' }), el(d, 'div', { class: 'tag label', id: 'label' }), el(d, 'div', { class: 'grid', id: 'grid' })),
          el(d, 'aside', { class: 'side', id: 'side' },
            el(d, 'div', { class: 'tag' }, 'Top tags'),
            el(d, 'div', { class: 'sub', id: 'themeSub' }),
            el(d, 'ol', { class: 'themes', id: 'themes' }))),
        el(d, 'div', { class: 'foot', id: 'foot' })),
      el(d, 'div', { class: 'toast', id: 'toast' }, el(d, 'div', { class: 'tag' }, 'New question'), el(d, 'div', { class: 't', id: 'toast-t' }), el(d, 'div', { class: 'by', id: 'toast-by' })));
    d.addEventListener('dblclick', () => d.fullscreenElement ? d.exitFullscreen() : d.documentElement.requestFullscreen());
    displayWin.addEventListener('resize', () => D && fitCards());
    d.fonts && d.fonts.ready.then(() => D && fitCards());   // Lato arriving reflows the cards taller
    D = { d, keys: {}, prevCards: null };
    popping = false;
    render();
  }

  // run fn only when key changed since last time
  const changed = (name, key) => { if (D.keys[name] === key) return false; D.keys[name] = key; return true; };

  function renderDisplay() {
    if (!displayWin || displayWin.closed || !D) return;
    const d = D.d;
    d.getElementById('sub').textContent = S.sub;

    const hero = byId(S.hero);
    if (changed('hero', hero ? textOf(hero) : '')) {
      d.getElementById('hero').replaceChildren(...(hero ? [el(d, 'div', { class: 'hero fade' },
        el(d, 'div', { class: 'tag' }, 'Question of the night'), el(d, 'div', { class: 'q' }, textOf(hero)), whoOf(hero) ? el(d, 'div', { class: 'by' }, whoOf(hero)) : null)] : []));
    }

    const items = boardItems();
    const hero0 = S.mode === 'related' ? byId(S.hero) : null;
    d.getElementById('label').textContent = !items.length ? '' :
      hero0 && mainTag(hero0) ? `${S.heading} · ${TAG_NAME[mainTag(hero0)]}` : S.heading;
    const grid = d.getElementById('grid');
    if (changed('gridMode', S.mode)) { grid.replaceChildren(); D.keys.cards = null; D.prevCards = null; }
    if (S.mode === 'related') renderSlots(items);
    const cardKey = JSON.stringify(items.map(it => [it.id, textOf(it), S.showVotes ? it.voteCount : null]));
    if (S.mode !== 'related' && changed('cards', cardKey)) {
      const prev = D.prevCards;
      let entering = 0;
      d.getElementById('grid').replaceChildren(...(items.length ? items.map(it => {
        const isNew = !prev || !prev.has(it.id);
        const c = el(d, 'div', { class: 'card' + (it.text ? ' host' : '') + (isNew ? ' enter' : ''), style: isNew ? `animation-delay:${entering++ * 110}ms` : '' },
          el(d, 'div', {}, el(d, 'div', {}, textOf(it)), whoOf(it) ? el(d, 'div', { class: 'by' }, whoOf(it)) : null),
          S.showVotes && it.voteCount != null ? el(d, 'span', { class: 'votes' }, String(it.voteCount), thumb(d)) : null);
        return c;
      }) : [hero ? null : el(d, 'div', { class: 'empty' }, 'Questions will appear here.')].filter(Boolean)));
      D.prevCards = new Set(items.map(it => it.id));
    }
    fitCards();

    renderThemes();

    const latest = S.latestMode === 'always' ? latestItem() : null;
    const top = S.showTop ? topItem() : null;
    const footKey = JSON.stringify([top && top.id, top && textOf(top), latest && latest.id, S.showVotes && top ? top.voteCount : null, S.showVotes && latest ? latest.voteCount : null, joinMatch]);
    if (changed('foot', footKey)) {
      const typing = el(d, 'div', { class: 'typing', id: 'typing' }, el(d, 'span', { class: 'dots' }, el(d, 'i'), el(d, 'i'), el(d, 'i')), el(d, 'span', { class: 'tl' }, 'Typing'));
      const hit = latest && latest.id === lastArrival && D.keys.latestShown !== latest.id;
      if (latest) D.keys.latestShown = latest.id;
      // "Just in" stays up while the question is fresh, then settles back to "Latest question"
      if (hit) setTimeout(() => { if (D && D.keys.latestShown === latest.id) { lastArrival = null; D.keys.foot = null; renderDisplay(); } }, 20000);
      const slot = (label, q, withTyping, loud) => el(d, 'div', { class: 'slot' + (loud ? ' hit' : '') },
        el(d, 'div', { class: 'head' }, el(d, 'div', { class: 'tag' }, loud ? 'Just in' : label,
          S.showVotes && q && q.voteCount != null ? el(d, 'span', { class: 'n' }, String(q.voteCount), thumb(d)) : null,
          whoOf(q) ? el(d, 'span', { class: 'who' }, whoOf(q)) : null), withTyping ? typing : null),
        el(d, 'div', { class: 't fade' }, q ? textOf(q) : ''));
      d.getElementById('foot').replaceChildren(...[
        top ? slot('Top voted', top, false) : null,
        latest ? slot('Latest question', latest, false, hit) : null,
        !top && !latest ? el(d, 'div', { class: 'slot' }) : null,
        el(d, 'div', { class: 'join' }, typing,
          el(d, 'div', { class: 'tag' }, joinMatch ? 'Ask yours at' : 'Ask yours anytime'),
          joinMatch ? el(d, 'span', { class: 'url' }, joinMatch) : null)].filter(Boolean));
    }
    renderStats();
    if (S.latestMode === 'popup') showNextPop();
  }

  // two fixed card slots; a slot whose question changes fades out, swaps text, fades back in
  // a card holds one content layer; a swap stacks the next layer on top of the old one and
  // crossfades them, so the card's box never empties out mid-rotation
  const makeLayer = (d, it) => el(d, 'div', { class: 'layer' + (textOf(it).length > 140 ? ' long' : '') },
    el(d, 'div', {}, el(d, 'div', {}, textOf(it)), whoOf(it) ? el(d, 'div', { class: 'by' }, whoOf(it)) : null),
    S.showVotes && it.voteCount != null ? el(d, 'span', { class: 'votes' }, String(it.voteCount), thumb(d)) : null);
  function fillCard(d, c, it) { c.dataset.id = it.id; c.replaceChildren(makeLayer(d, it)); }
  function crossfade(d, c, it, done) {
    const old = [...c.children];
    c.dataset.id = it.id;
    const layer = makeLayer(d, it);
    layer.classList.add('lin');
    old.forEach(o => { o.classList.remove('lin'); o.classList.add('lout'); });
    c.append(layer);
    setTimeout(() => { old.forEach(o => o.remove()); layer.classList.remove('lin'); done(); }, FADE_MS);
  }
  const cardFits = c => c.offsetTop + c.offsetHeight <= c.parentElement.clientHeight + 1;
  // a rotating card that won't fit above the footer is swapped for the next question that does,
  // instead of sitting hidden until its next turn (which read as the two cards syncing up)
  function fitOrSkip(c, slot) {
    if (cardFits(c)) return true;
    const pool = relatedPool(), other = rel.slots[slot ^ 1];
    for (let tries = 0; tries < pool.length; tries++) {
      const q = pool[rel.next % pool.length];
      rel.next = (rel.next + 1) % pool.length;
      if (q.id === other || String(q.id) === c.dataset.id) continue;
      rel.slots[slot] = q.id;
      fillCard(D.d, c, q);
      if (cardFits(c)) return true;
    }
    return false;   // nothing in the category fits: fitCards hides it
  }
  function renderSlots(items) {
    const d = D.d, grid = d.getElementById('grid');
    if (!items.length) { grid.replaceChildren(); return; }
    while (grid.children.length < items.length) grid.append(el(d, 'div', { class: 'card slotcard' }));
    while (grid.children.length > items.length) grid.lastChild.remove();
    items.forEach((it, i) => {
      const c = grid.children[i];
      if (c.dataset.swapping) { c.dataset.pending = it.id; return; }
      if (!c.dataset.id) { fillCard(d, c, it); fitOrSkip(c, i); c.classList.add('in'); c.style.animationDelay = i * 300 + 'ms'; return; }
      if (c.dataset.id === String(it.id)) {   // same question: refresh the vote count quietly
        const v = c.lastElementChild && c.lastElementChild.querySelector('.votes');
        if (S.showVotes && v && v.firstChild && v.firstChild.nodeValue !== String(it.voteCount)) v.firstChild.nodeValue = String(it.voteCount);
        return;
      }
      c.dataset.swapping = '1';
      crossfade(d, c, it, () => {
        delete c.dataset.swapping;
        const pend = c.dataset.pending && byId(+c.dataset.pending);
        delete c.dataset.pending;
        if (pend && String(pend.id) !== c.dataset.id) fillCard(d, c, pend);
        fitOrSkip(c, i);
        fitCards();
      });
    });
  }

  // a card that would be cut off by the footer is left out entirely rather than shown half-clipped
  function fitCards() {
    // layout boxes (offsetTop/Height), not getBoundingClientRect: the entrance animation's
    // translateY would otherwise make a card look like it overflows and hide it for good
    const grid = D.d.getElementById('grid'), h = grid.clientHeight;
    // fonts loading or a resize can push a rotating card over the edge: re-pick rather than hide
    if (S.mode === 'related') [...grid.children].forEach((c, i) => { if (!c.dataset.swapping && c.dataset.id) fitOrSkip(c, i); });
    let shown = 0;
    for (const c of grid.children) {
      const fits = c.dataset.swapping || c.offsetTop + c.offsetHeight <= h + 1;
      c.style.visibility = fits ? '' : 'hidden';
      if (fits) shown++;
    }
    D.shown = shown;   // the next rotation starts right after the last card that actually fit
  }


  // ranked theme list; rows are keyed by theme so a reorder slides (FLIP) instead of jumping
  function renderThemes() {
    const d = D.d, side = d.getElementById('side'), list = d.getElementById('themes');
    side.style.display = S.showThemes ? '' : 'none';
    if (!S.showThemes) return;
    d.getElementById('themeSub').textContent = `By ${S.themeMetric === 'votes' ? 'votes' : 'number of questions'}`;
    const rank = themeRanking(), max = Math.max(1, ...rank.map(r => r.v));
    if (!changed('themes', JSON.stringify([rank, S.themeMetric]))) return;   // cards rotating must not touch this
    const rows = new Map([...list.children].map(li => [li.dataset.k, li]));
    const before = new Map([...rows].map(([k, li]) => [k, li.getBoundingClientRect().top]));
    const next = rank.map((r, i) => {
      let li = rows.get(r.k);
      if (!li) {
        li = el(d, 'li', { class: 'th fade', 'data-k': r.k, onanimationend: e => e.target === li && li.classList.remove('fade') },
          el(d, 'div', { class: 'row' }, el(d, 'span', { class: 'rk' }), el(d, 'span', { class: 'nm' }, TAG_NAME[r.k]), el(d, 'span', { class: 'v' })),
          el(d, 'div', { class: 'bar' }, el(d, 'i', { style: 'width:0' })));
      }
      const old = +li.dataset.v || 0;
      if (li.dataset.v && r.v > old) { li.classList.remove('bump'); void li.offsetWidth; li.classList.add('bump'); }
      li.dataset.v = r.v;
      li.classList.toggle('lead', i === 0);
      li.querySelector('.rk').textContent = i + 1;
      li.querySelector('.v').textContent = r.v;
      return li;
    });
    // only re-insert rows when the order actually changed (re-inserting restarts CSS animations)
    if (next.some((li, i) => list.children[i] !== li) || list.children.length !== next.length) list.replaceChildren(...next);
    // bars grow on the next frame so the width transition runs
    displayWin.requestAnimationFrame(() => next.forEach((li, i) => { li.querySelector('.bar i').style.width = (rank[i].v / max * 100) + '%'; }));
    for (const li of next) {
      const was = before.get(li.dataset.k);
      if (was == null) continue;
      const dy = was - li.getBoundingClientRect().top;
      if (dy) li.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }], { duration: 700, easing: 'cubic-bezier(.2,.8,.2,1)' });
    }
  }

  // new questions slide in one at a time, then get out of the way
  function showNextPop() {
    if (popping || !displayWin || displayWin.closed || !D) return;
    if (S.latestMode !== 'popup') { popQueue.length = 0; return; }
    const q = popQueue.shift();
    if (!q) return;
    const d = D.d, t = d.getElementById('toast');
    popping = true;
    d.getElementById('toast-t').textContent = textOf(q);
    d.getElementById('toast-by').textContent = whoOf(q);
    t.classList.add('on');
    setTimeout(() => { t.classList.remove('on'); setTimeout(() => { popping = false; showNextPop(); }, 600); }, POP_MS);
  }

  // cheap in-place update every STATS_MS; numbers pulse when they move
  function renderStats() {
    const st = panel && panel.querySelector('.live');
    if (st) st.textContent = [live.online != null ? (live.online === 1 ? '1 person' : live.online + ' people') + ' online' : null, live.typing ? (live.typing > 1 ? live.typing + ' typing…' : 'someone typing…') : null, typingSock ? null : 'typing signal: present mode only'].filter(Boolean).join(' · ');
    if (!displayWin || displayWin.closed || !D) return;
    const d = D.d;
    const set = (id, n) => {
      const x = d.getElementById(id); if (!x) return;
      const v = n == null ? '–' : String(n);
      if (x.textContent === v) return;
      const wasNum = /^\d+$/.test(x.textContent);
      x.textContent = v;
      if (wasNum) { x.classList.remove('tick'); void x.offsetWidth; x.classList.add('tick'); }
    };
    set('online', live.online);
    set('qcount', questions.length);
    set('vcount', questions.reduce((n, q) => n + (q.voteCount || 0), 0));   // every up-vote on the board, answered included
    fitCards();
    const ty = d.getElementById('typing');
    if (ty) {
      ty.classList.toggle('on', live.typing > 0);
      const lbl = ty.querySelector('.tl'), txt = live.typing > 1 ? `${live.typing} typing` : 'Typing';
      if (lbl && lbl.textContent !== txt) lbl.textContent = txt;
    }
  }

  function floatReaction(k) {
    if (!displayWin || displayWin.closed || !D || !EMOJI[k]) return;
    const d = D.d;
    const icon = d.querySelector(`#reacts [data-r="${k}"]`);
    if (icon) { icon.classList.add('pop'); setTimeout(() => icon.classList.remove('pop'), 300); }
    const f = el(d, 'div', { class: 'floater', style: `right:${3 + Math.random() * 26}vw;--dx:${(Math.random() * 6 - 3).toFixed(1)}vw` }, EMOJI[k]);
    d.body.append(f);
    setTimeout(() => f.remove(), 4300);
  }

  // ---------- moderator panel ----------
  const MOD_CSS = `
    #gqa{position:fixed;inset:0;z-index:2147483647;background:${C.cloud};color:${C.ink};font:14px/1.4 Lato,system-ui,sans-serif;display:flex;flex-direction:column}
    #gqa *{box-sizing:border-box}
    #gqa header{display:flex;align-items:center;gap:12px;padding:10px 16px;background:${C.stable};color:#fff}
    #gqa header b{font-weight:300;font-size:20px;margin-right:auto}
    #gqa .st{font-size:12px;color:${C.cloud}}
    #gqa .st.err{color:#fff;font-weight:900}
    #gqa button{font:inherit;cursor:pointer;border:1px solid ${C.cinder};background:#fff;color:${C.ink};border-radius:6px;padding:4px 10px}
    #gqa button.pri{background:${C.active};border-color:${C.active};color:#fff;font-weight:700}
    #gqa button.on{background:${C.stable};border-color:${C.stable};color:#fff}
    #gqa header button{background:transparent;color:#fff;border-color:${C.cloud}}
    #gqa header button.pri{background:${C.active};border-color:${C.active}}
    #gqa main{flex:1;display:grid;grid-template-columns:1.2fr 1fr;gap:16px;padding:16px;min-height:0}
    #gqa section{background:#fff;border-radius:10px;display:flex;flex-direction:column;min-height:0}
    #gqa h2{font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:900;color:${C.stable};margin:0;padding:12px 14px 8px}
    #gqa .bar{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px;align-items:center}
    #gqa input[type=text]{font:inherit;border:1px solid ${C.cinder};border-radius:6px;padding:5px 8px;flex:1;min-width:120px}
    #gqa .list{overflow:auto;flex:1;padding:0 8px 8px}
    #gqa .row{display:flex;gap:8px;align-items:flex-start;padding:8px 6px;border-top:1px solid ${C.cloud}}
    #gqa .row .t{flex:1}
    #gqa .row .meta{font-size:11px;color:${C.stable};opacity:1;margin-top:2px}
    #gqa .row .acts{display:flex;gap:4px;flex:none}
    #gqa .row .acts button{padding:2px 8px;font-size:12px}
    #gqa .pill{display:inline-block;font-size:10px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;border-radius:4px;padding:1px 5px;margin-right:4px}
    #gqa .p-ans{background:${C.cloud};color:${C.stable}}
    #gqa .p-new{background:${C.active};color:#fff}
    #gqa .p-host{background:${C.stable};color:#fff}
    #gqa .p-hid{background:${C.cinder};color:#fff}
    #gqa .row.dim .t{opacity:.5}
    #gqa .hero{margin:0 14px 10px;padding:10px 12px;border-left:4px solid ${C.active};background:${C.cloud};border-radius:6px}
    #gqa select.catsel{font:inherit;border:1px solid ${C.cinder};border-radius:6px;padding:4px 6px;background:#fff;color:${C.stable};max-width:60%}
    #gqa .bulk{font-size:12px;color:${C.stable};margin-left:auto}
    #gqa button[disabled]{opacity:.4;cursor:default}
    #gqa .chips{display:inline-flex;flex-wrap:wrap;gap:4px;vertical-align:middle}
    #gqa .chip{font-size:11px;border:1px solid ${C.active};color:${C.stable};border-radius:10px;padding:0 4px 0 7px;cursor:pointer;white-space:nowrap}
    #gqa .chip.main{background:${C.active};color:#fff;cursor:default}
    #gqa .chip b{font-weight:900;margin-left:4px;cursor:pointer;opacity:.7}
    #gqa .chip b:hover{opacity:1}
    #gqa select.thsel{font:inherit;font-size:11px;color:${C.stable};border:1px solid ${C.cloud};border-radius:4px;background:#fff;padding:0 2px}
    #gqa .note{font-size:12px;color:${C.stable};padding:0 14px 12px}
  `;

  let panel;
  function buildPanel() {
    if (!document.getElementById('gqa-font')) document.head.append(el(document, 'link', { id: 'gqa-font', rel: 'stylesheet', href: FONT }));
    document.head.append(el(document, 'style', { id: 'gqa-css' }, MOD_CSS));
    panel = el(document, 'div', { id: 'gqa' });
    document.body.append(panel);
    // keep AhaSlides' keyboard shortcuts (slide nav etc.) from firing while the panel is up
    panel.addEventListener('keydown', e => { e.stopPropagation(); if (e.key === 'Escape') toggle(); }, true);
    panel.addEventListener('pointerdown', () => { pointerDown = true; }, true);
    const flush = () => { if (!pointerDown && renderPending) { renderPending = false; setTimeout(render, 0); } };
    window.addEventListener('pointerup', () => { pointerDown = false; setTimeout(flush, 0); }, true);
    // focus leaves a field on the same mousedown that starts a click: flush only once the press is over
    panel.addEventListener('focusout', () => setTimeout(flush, 0), true);
  }

  function row(q, opts = {}) {
    const d = document, id = q.id, isHost = typeof id === 'string';
    const feat = S.featured.includes(id), hero = S.hero === id, hid = S.hidden.includes(id);
    return el(d, 'div', { class: 'row' + (hid ? ' dim' : '') },
      el(d, 'div', { class: 't' },
        el(d, 'div', {},
          isHost ? el(d, 'span', { class: 'pill p-host' }, 'Host') : null,
          q.answered ? el(d, 'span', { class: 'pill p-ans' }, 'Answered') : null,
          !isHost && !seenAtOpen.has(id) ? el(d, 'span', { class: 'pill p-new' }, 'New') : null,
          hid ? el(d, 'span', { class: 'pill p-hid' }, 'Hidden') : null,
          textOf(q)),
        !isHost ? el(d, 'div', { class: 'meta' }, `${q.voteCount} vote${q.voteCount === 1 ? '' : 's'} · ${whoOf(q)} · ${new Date(q.createdAt).toLocaleDateString()} · `, tagEditor(q)) : null),
      el(d, 'div', { class: 'acts' },
        opts.order ? [
          el(d, 'button', { title: 'Move up', onclick: act(() => move(id, -1)) }, '↑'),
          el(d, 'button', { title: 'Move down', onclick: act(() => move(id, 1)) }, '↓'),
        ] : null,
        el(d, 'button', { class: hero ? 'on' : '', title: 'Question of the night', onclick: act(() => { S.hero = hero ? null : id; }) }, hero ? 'QOTN ✓' : 'QOTN'),
        el(d, 'button', { class: feat ? 'on' : '', onclick: act(() => { S.featured = toggleIn(S.featured, id); }) }, feat ? 'On board' : 'Feature'),
        !isHost && !opts.order ? el(d, 'button', { class: hid ? 'on' : '', title: 'Keep off the display (rotation, top voted, latest, categories)', onclick: act(() => { S.hidden = toggleIn(S.hidden, id); }) }, hid ? 'Unhide' : 'Hide') : null,
        isHost && opts.order ? el(d, 'button', { title: 'Delete host card', onclick: act(() => {
          S.custom = S.custom.filter(c => c.id !== id); S.featured = S.featured.filter(x => x !== id); if (S.hero === id) S.hero = null;
        }) }, '✕') : null));
  }

  // tag chips: click a chip to make it the main tag, × to remove, the + menu to add one
  function tagEditor(q) {
    const d = document, cur = tagsOf(q);
    const setTags = next => { S.tagOverride[q.id] = next; save(); render(); };
    const chips = cur.map((k, i) => el(d, 'span', { class: 'chip' + (i === 0 ? ' main' : ''), title: i === 0 ? 'Main tag' : 'Click to make this the main tag',
        onclick: e => { e.stopPropagation(); if (i) setTags([k, ...cur.filter(x => x !== k)]); } },
      TAG_NAME[k], el(d, 'b', { title: 'Remove tag', onclick: e => { e.stopPropagation(); setTags(cur.filter(x => x !== k)); } }, '×')));
    const add = el(d, 'select', { class: 'thsel', title: 'Add a tag' },
      el(d, 'option', { value: '' }, cur.length ? '+ tag' : '+ tag (untagged)'),
      TAGS.filter(t => !cur.includes(t.k)).map(t => el(d, 'option', { value: t.k }, t.n)));
    add.addEventListener('change', () => { if (add.value) { add.blur(); setTags([...cur, add.value]); } });
    return el(d, 'span', { class: 'chips' }, chips, add);
  }

  function renderPanel() {
    if (!panel || panel.style.display === 'none') return;
    const d = document;
    const q = search.toLowerCase();
    const pool = questions
      .filter(x => filter === 'all' || (filter === 'open' && !x.answered) || (filter === 'answered' && x.answered) || (filter === 'featured' && S.featured.includes(x.id)) || (filter === 'hidden' && S.hidden.includes(x.id)))
      .filter(x => !catFilter || (catFilter === 'none' ? !tagsOf(x).length : tagsOf(x).includes(catFilter)))
      .filter(x => !q || x.title.toLowerCase().includes(q))
      .sort((a, b) => b.voteCount - a.voteCount);
    const counts = { all: questions.length, open: questions.filter(x => !x.answered).length, answered: questions.filter(x => x.answered).length, featured: S.featured.length, hidden: S.hidden.length };
    const catCounts = {}; let untagged = 0;
    for (const x of questions) { const ts = tagsOf(x); if (!ts.length) untagged++; for (const k of ts) catCounts[k] = (catCounts[k] || 0) + 1; }
    const opt = (v, label) => { const o = el(d, 'option', { value: v }, label); if (v === catFilter) o.selected = true; return o; };
    const catSel = el(d, 'select', { class: 'catsel', title: 'Filter by tag' },
      opt('', `All tags (${questions.length})`),
      untagged ? opt('none', `Untagged (${untagged})`) : null,
      TAGS.filter(t => catCounts[t.k]).sort((a, b) => catCounts[b.k] - catCounts[a.k]).map(t => opt(t.k, `${t.n} (${catCounts[t.k]})`)));
    catSel.addEventListener('change', () => { catFilter = catSel.value; catSel.blur(); renderPanel(); });
    const poolIds = pool.map(x => x.id);
    const nHid = poolIds.filter(id => S.hidden.includes(id)).length, nHideable = poolIds.filter(id => id !== S.hero && !S.hidden.includes(id)).length;
    // bulk hide never takes the question of the night with it
    const bulk = hide => act(() => { S.hidden = hide ? [...new Set([...S.hidden, ...poolIds.filter(id => id !== S.hero)])] : S.hidden.filter(id => !poolIds.includes(id)); });
    const hero = byId(S.hero);
    const dispOpen = displayWin && !displayWin.closed;

    // preserve focus/scroll across re-renders
    const active = d.activeElement && d.activeElement.dataset ? d.activeElement.dataset.k : null;
    const selStart = active ? d.activeElement.selectionStart : null;
    const scrolls = [...panel.querySelectorAll('.list')].map(n => n.scrollTop);

    const customIn = el(d, 'input', { type: 'text', 'data-k': 'custom', placeholder: 'Add a host card (e.g. a framing line or scripture)…' });
    const addCustom = () => { const t = customIn.value.trim(); if (!t) return; const id = 'c' + Date.now(); S.custom.push({ id, text: t }); S.featured.push(id); customIn.value = ''; save(); render(); };
    customIn.addEventListener('keydown', e => { if (e.key === 'Enter') addCustom(); });

    const headIn = el(d, 'input', { type: 'text', 'data-k': 'heading', value: S.heading });
    headIn.addEventListener('input', () => { S.heading = headIn.value; save(); renderDisplay(); });
    const subIn = el(d, 'input', { type: 'text', 'data-k': 'sub', value: S.sub });
    subIn.addEventListener('input', () => { S.sub = subIn.value; save(); renderDisplay(); });
    const searchIn = el(d, 'input', { type: 'text', 'data-k': 'search', placeholder: 'Search questions…', value: search });
    searchIn.addEventListener('input', () => { search = searchIn.value; renderPanel(); });

    panel.replaceChildren(
      el(d, 'header', {},
        el(d, 'b', {}, 'Grace Q&A Board'),
        el(d, 'span', { class: 'st live' }),
        el(d, 'span', { class: 'st' + (lastErr ? ' err' : '') }, statusText()),
        el(d, 'button', { class: 'pri', onclick: openDisplay }, dispOpen ? 'Focus display window' : 'Open display window'),
        el(d, 'button', { onclick: () => toggle() }, 'Hide panel (Esc)')),
      el(d, 'main', {},
        el(d, 'section', {},
          el(d, 'h2', {}, 'All questions from AhaSlides'),
          el(d, 'div', { class: 'bar' },
            ['all', 'open', 'answered', 'featured', 'hidden'].map(f => el(d, 'button', { class: filter === f ? 'on' : '', onclick: () => { filter = f; renderPanel(); } },
              `${{ all: 'All', open: 'Unanswered', answered: 'Answered', featured: 'On board', hidden: 'Hidden' }[f]} (${counts[f]})`)),
            searchIn),
          el(d, 'div', { class: 'bar' },
            catSel,
            el(d, 'span', { class: 'bulk' }, `${pool.length} shown`),
            el(d, 'button', { disabled: !nHideable || null, onclick: bulk(true) }, `Hide all ${nHideable || ''}`.trim()),
            el(d, 'button', { disabled: !nHid || null, onclick: bulk(false) }, `Unhide all ${nHid || ''}`.trim())),
          el(d, 'div', { class: 'list' }, pool.map(x => row(x)))),
        el(d, 'section', {},
          el(d, 'h2', {}, 'On the board'),
          el(d, 'div', { class: 'bar' },
            el(d, 'button', { class: S.mode === 'related' ? 'on' : '', title: "Cycle through the QOTN's category", onclick: act(() => { S.mode = 'related'; }) }, 'Same category'),
            el(d, 'button', { class: S.mode === 'featured' ? 'on' : '', onclick: act(() => { S.mode = 'featured'; }) }, 'Curated'),
            el(d, 'button', { class: S.mode === 'live' ? 'on' : '', onclick: act(() => { S.mode = 'live'; }) }, 'Live top 6'),
            el(d, 'button', { class: S.showVotes ? 'on' : '', onclick: act(() => { S.showVotes = !S.showVotes; }) }, S.showVotes ? 'Votes shown' : 'Votes hidden'),
            el(d, 'button', { class: S.showTop ? 'on' : '', onclick: act(() => { S.showTop = !S.showTop; }) }, S.showTop ? 'Top voted shown' : 'Top voted hidden'),
            el(d, 'button', { class: S.latestMode !== 'off' ? 'on' : '', title: 'Pop-up: new questions slide in for 8s. Always: pinned in the footer.',
              onclick: act(() => { S.latestMode = { popup: 'always', always: 'off', off: 'popup' }[S.latestMode] || 'popup'; }) },
              'Latest: ' + ({ popup: 'pop-up', always: 'always', off: 'off' }[S.latestMode] || 'pop-up'))),
          el(d, 'div', { class: 'bar' },
            el(d, 'button', { class: S.showThemes ? 'on' : '', onclick: act(() => { S.showThemes = !S.showThemes; }) }, S.showThemes ? 'Tags shown' : 'Tags hidden'),
            el(d, 'button', { onclick: act(() => { S.themeMetric = S.themeMetric === 'votes' ? 'count' : 'votes'; }) }, 'Rank by: ' + (S.themeMetric === 'votes' ? 'votes' : 'questions'))),
          el(d, 'div', { class: 'bar' }, el(d, 'span', {}, 'Eyebrow'), subIn),
          el(d, 'div', { class: 'bar' }, el(d, 'span', {}, 'Heading'), headIn),
          hero ? el(d, 'div', { class: 'hero' }, el(d, 'b', {}, 'QOTN: '), textOf(hero)) : el(d, 'div', { class: 'note' }, 'No question of the night set — click QOTN on any question or host card.'),
          el(d, 'div', { class: 'bar' }, customIn, el(d, 'button', { class: 'pri', onclick: addCustom }, 'Add')),
          S.mode === 'related' ? el(d, 'div', { class: 'note' }, hero && mainTag(hero)
            ? `Rotating ${relatedPool().length} questions tagged "${TAG_NAME[mainTag(hero)] || '—'}" (the QOTN's main tag): two on screen, one swaps every ${SWAP_MS / 1000}s. Tag a question at left to pull it in or out.`
            : 'Set a question of the night that has a tag (an audience question, not a host card) to rotate its main tag.') : null,
          S.mode === 'live' ? el(d, 'div', { class: 'note' }, 'Live mode shows the top 6 unanswered questions by votes (minus hidden ones). Switch to Curated to use your order below.') : null,
          el(d, 'div', { class: 'list' },
            S.mode === 'featured'
              ? (S.featured.length ? S.featured.map(byId).filter(Boolean).map(x => row(x, { order: true })) : el(d, 'div', { class: 'note' }, 'Nothing featured yet — click Feature on questions at left.'))
              : (S.mode === 'related' ? relatedPool() : boardItems()).map(x => row(x))),
          el(d, 'div', { class: 'note' }, 'Read-only: nothing here changes the AhaSlides deck. Double-click the display window to go fullscreen.')))
    );

    renderStats();
    panel.querySelectorAll('.list').forEach((n, i) => { n.scrollTop = scrolls[i] || 0; });
    if (active) { const n = panel.querySelector(`[data-k="${active}"]`); if (n) { n.focus(); try { n.setSelectionRange(selStart, selStart); } catch {} } }
  }

  let pointerDown = false, renderPending = false;
  function render() {
    const a = document.activeElement;
    if (pointerDown || (a && a.tagName === 'SELECT' && panel && panel.contains(a))) { renderPending = true; renderDisplay(); return; }
    renderPanel(); renderDisplay();
  }

  function toggle() {
    if (!panel) return;
    panel.style.display = panel.style.display === 'none' ? 'flex' : 'none';
    renderPanel();
  }

  buildPanel();
  const timer = setInterval(poll, POLL_MS);
  const statsTimer = setInterval(pollStats, STATS_MS);
  const cycleTimer = setInterval(swapOne, SWAP_MS);
  window.__graceQA = { version: VERSION, toggle, destroy: () => { clearInterval(timer); clearInterval(statsTimer); clearInterval(cycleTimer); try { typingSock && typingSock.off('user-is-typing', onTyping); } catch {} panel.remove(); } };
  poll();
  pollStats();
})();
