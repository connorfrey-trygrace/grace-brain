(() => {
  const VERSION = '2affdac2df';
  if (window.__graceQA) {
    if (window.__graceQA.version === VERSION) { window.__graceQA.toggle(); return; }
    try { window.__graceQA.destroy ? window.__graceQA.destroy() : document.getElementById('gqa')?.remove(); } catch {}
    document.getElementById('gqa-css')?.remove();
  }

  const m = location.pathname.match(/presentation\/(\d+)/);
  if (location.host !== 'presenter.ahaslides.com' || !m) {
    alert('Open your AhaSlides presentation (presenter.ahaslides.com/presentation/\u2026) first, then click the bookmarklet.');
    return;
  }
  const PID = m[1];
  const KEY = 'graceQA:' + PID;
  const POLL_MS = 4000;

  const C = { stable: '#1C3B6B', active: '#2F97A0', cinder: '#ABABAB', cloud: '#E3E3E3', ink: '#1C3B6B' };

  const LOGO = 'data:image/png;base64,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';
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

  const STATS_MS = 2000;
  const REACTION_SLIDE = 1;   // reaction counters are kept per slide; the Q&A slide is slide 1 in this deck
  const EMOJI = { heart: '\u2764\ufe0f', like: '\ud83d\udc4d', laugh: '\ud83d\ude02', wow: '\ud83d\ude2e', sad: '\ud83d\ude22' };
  const live = { online: null, typing: 0, reactions: null };

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
  const statusText = () => lastErr ? `Can't reach AhaSlides (${lastErr}) \u2014 retrying` : lastOk ? `Live \u00b7 updated ${lastOk.toLocaleTimeString()}` : 'Connecting\u2026';
  function renderStatus() {
    const n = panel && panel.querySelector('.st:not(.live)');
    if (n) { n.textContent = statusText(); n.className = 'st' + (lastErr ? ' err' : ''); }
  }

  const byId = id => typeof id === 'string'
    ? S.custom.find(c => c.id === id)
    : questions.find(q => q.id === id);
  const textOf = item => item ? (item.title ?? item.text) : '';
  const whoOf = item => !item || typeof item.id === 'string' ? '' : (item.audienceName || '').trim() || 'Anon';

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
  function topItem() {
    const shown = new Set([S.hero, ...(S.mode === 'related' ? [] : boardItems().map(x => x.id))]);
    return questions.filter(q => !q.answered && !S.hidden.includes(q.id) && !shown.has(q.id))
      .sort((a, b) => b.voteCount - a.voteCount)[0] || null;
  }
  function latestItem() {
    const shown = new Set([S.hero, ...(S.mode === 'related' ? [] : boardItems().map(x => x.id))]);
    return questions.filter(q => !S.hidden.includes(q.id) && !shown.has(q.id))
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))[0] || null;
  }

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

  const TAG_SEED = {"if god is always with us and loves us, why do many people go":["SU","CA"],"what do you do if you are losing faith that god cares about ":["CA","DO"],"my greatest question always goes back to pain. if there is a":["SU"],"i think back on my life and if tragedy befell me before i ca":["SA","SU"],"gos never gives us more than we can handle. what's our praye":["SU"],"why does god let our loved ones suffer or die tragically at ":["SU","DE"],"what do you do when you believe god does not care about you ":["CA","DO"],"if god is all-powerful and perfectly good, why do innocent a":["SU"],"why do bad things happen to good people?":["SU"],"how does adam and eve fit in with evolution?":["SC","BI"],"how do we know what's real in the bible and what is a parabl":["BI"],"if adam and eve had just two sons, cain and abel, and no dau":["BI","SC"],"did jonah and the fish really happen?":["BI"],"how to handle sin when trying to build a relationship with g":["SI","FO"],"how should dc washingtonians practice sabbath?":["CH","LI"],"can actions/ thoughts hinder a deep meaningful relationship ":["SI","FO"],"is it okay that i don't attend service every week? am i any ":["CH"],"if jesus created a new covenant with his crucifixion and res":["BI","CH"],"how do we control what we put into our minds without isolati":["FO","LI"],"how do i handle a busy season?":["LI","FO"],"does 1 corinthians 11:30 mean that some people should not pa":["CH","BI"],"how do we test our true motivations?":["FO"],"how do i be gentle and kind and forgiving without becoming a":["LI","FO"],"how to endure when you're doing \"all of the things\" and stil":["WO","FO"],"how do we differentiate the origin of objects of our desire ":["SI","SC"],"i would like to hear more about how to fully accept that god":["CO","PU"],"how do i know my real purpose in life? i dont work and feel ":["PU"],"hwo to gain power over oneself":["FO","SI"],"is the desire to find a grand purpose in life itself somethi":["PU"],"can a person become addicted to urgency because it temporari":["PU","WO"],"does christianity encourage us to live urgently, or does it ":["PU","FO"],"i like to learn about to the some situation in the past affe":["LI"],"the young professionals group at grace has had only one even":["GR"],"what does grace really mean?":["WB"],"does grace ofer bible?":["GR","BI"],"i have noticed that some people end their prayers without sa":["CH","WB"],"can psalm 1&2 really be a summary of the entire bible?":["BI"],"do you have small groups for women in the 50ish age backet?":["GR"],"who is jireh?":["WB","BI"],"who are the nephilim?":["WB","BI"],"if i don't like church ( because i can't sit still) does tha":["CH"],"how can we discern the difference between god calling us to ":["DI"],"how does christian discernment work when god hasn't provided":["DI"],"how to have discernment? especially with things i've prayed ":["DI","HG"],"what if you don't hear the advocate or the holy spirit? does":["SP","HG"],"can you speak on the gifts of the holy spirit?":["SP"],"how can i influence a loved one to follow jesus?":["SH"],"how should christian evangelism evolve in an age where peopl":["SH","CU"],"believing in god makes so much sense \u2014 why isn't it more mai":["CU","SH"],"what is the next big thing god is going to do in arlington? ":["CU"],"what to do when teens don't believe in jesus. ie just like s":["SH","LI"],"how do i handle situations where i'm around friends or even ":["LI","SH"],"how to spread hope to so many around me who are hopeless?":["SH"],"what if someone is not christian, wants to learn more about ":["SA","SH"],"why/how is it considered that jesus \"saved\" humanity/us when":["SA","JE"],"how does someone who used to be godless learn to forgive the":["SI","SA"],"what happens when you die?":["DE"],"what are some of the most common things christians do, say, ":["BI","CU"],"can you lose your salvation?":["SA"],"if fear of death can motivate an animal toward survival, wha":["BI","WB"],"how does god listen to everyone at once ?":["GO"],"what's the deal with all these paradoxes in christianity?":["DO"],"what to do when multiple people are saying the end times are":["DE"],"how did you come up with the metaphors and examples with foo":["SE"],"how do we beat praise god for blessings?":["CH"],"i saw te documentary christspiracy... was christ a vegan? ho":["JE","CU"],"how can i learn to hear from god?":["HG"],"how can i learn the difference between god speaking to me an":["HG","DI"],"how can identify when god is talking to me?":["HG"],"how do we know w're hearing from god, and not just our own p":["HG","DI"],"what does god's presence feel like? how do you access his pr":["SP","HG"],"how can you differentiate your own inner voice from gods?":["HG","DI"],"how can i hear god when i don't know what his voice sounds l":["HG"],"how can i be more sensitive to the voice of god? what else c":["HG","FO"],"how can i know if the holy spirit is with me?":["SP"],"how do i identify god and how can i get to him if i need it\u2026":["HG","CA"],"how do we actually know what god looks like?":["GO","HG"],"how do i not worry when everything is actually falling apart":["WO","SU"],"how do i not worrybout the future? and specially in a relati":["WO","RE"],"how do i not worry so much?":["WO"],"is jesus really the only way to god? what about people who n":["SA"],"on sunday's sermon: if \"the way\" is an approach to life, the":["SA","SE"],"what are the 'greater works' he's talking about in verse 12?":["BI","SE"],"how can i spread the gospel to the people in my life and str":["SH"],"do i have to go church on sunday?":["CH"],"how many time per week should a good church going gentleman ":["RE"],"are all these questions answerable?":["DO"],"how can we be a better steward of our financial blessing and":["MO","DI"],"almost every time in my life that i felt \"called\" to somethi":["PU","SU","DO"],"how can god love us equally if he predestined some to go to ":["CO","SA"],"if duty is doing things even when you don't feel like it, wh":["FO"],"how do we keep god in the middle? in between the highs and t":["FO"],"is it wrong to date an have physical relations with someone ":["RE","SI"],"why did god give us fossil fuels? why not skip straight to c":["SC","CO"],"regarding matthew 6:33 (\"seek first the kingdom of god\") and":["BI","FO"]};
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
  const normText = t => String(t).replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"').replace(/\s+/g, ' ').trim()
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
    .slot .who::before{content:'\u00b7 ';color:${C.cinder}}
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

  let D = null;   // { d, keys:{}, prevCards:Set }
  function openDisplay() {
    if (displayWin && !displayWin.closed) { displayWin.focus(); return; }
    displayWin = window.open('/robots.txt', 'graceQADisplay', 'width=1280,height=720');
    if (!displayWin) { alert('Pop-up blocked \u2014 allow pop-ups for presenter.ahaslides.com and try again.'); return; }
    const started = Date.now();
    const whenLoaded = () => {
      let ready = false;
      try { ready = displayWin.location.pathname === '/robots.txt' && displayWin.document.readyState === 'complete'; } catch {}
      if (ready) buildDisplay();
      else if (Date.now() - started < 10000) setTimeout(whenLoaded, 50);
      else alert('The display window did not load \u2014 close it and click Open display window again.');
    };
    whenLoaded();
  }

  function buildDisplay() {
    const d = displayWin.document;
    d.open();
    d.write(`<!doctype html><html><head><title>Grace \u00b7 Sunday Night Q&A</title><link rel="stylesheet" href="${FONT}"><style>${DISPLAY_CSS}</style></head><body></body></html>`);
    d.close();
    try { displayWin.history.replaceState(null, '', '/grace-sunday-night-qa'); } catch {}
    d.body.append(
      el(d, 'div', { class: 'wrap' },
        el(d, 'div', { class: 'top' },
          el(d, 'img', { class: 'logo', src: LOGO, alt: 'Grace Community Church' }),
          el(d, 'div', { class: 'meta' },
            el(d, 'div', { class: 'eyebrow' }, el(d, 'span', { id: 'sub' }), el(d, 'span', { class: 'livedot' }, el(d, 'i'), 'Live')),
            el(d, 'div', { class: 'stats' },
              el(d, 'div', { class: 'stat' }, el(d, 'span', { class: 'lbl' }, 'Online'), el(d, 'span', { class: 'num', id: 'online' }, '\u2013')),
              el(d, 'div', { class: 'stat' }, el(d, 'span', { class: 'lbl' }, 'Questions'), el(d, 'span', { class: 'num', id: 'qcount' }, '\u2013')),
              el(d, 'div', { class: 'stat' }, el(d, 'span', { class: 'lbl' }, 'Votes'), el(d, 'span', { class: 'num', id: 'vcount' }, '\u2013'))))),
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
      hero0 && mainTag(hero0) ? `${S.heading} \u00b7 ${TAG_NAME[mainTag(hero0)]}` : S.heading;
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

  function fitCards() {
    const grid = D.d.getElementById('grid'), h = grid.clientHeight;
    if (S.mode === 'related') [...grid.children].forEach((c, i) => { if (!c.dataset.swapping && c.dataset.id) fitOrSkip(c, i); });
    let shown = 0;
    for (const c of grid.children) {
      const fits = c.dataset.swapping || c.offsetTop + c.offsetHeight <= h + 1;
      c.style.visibility = fits ? '' : 'hidden';
      if (fits) shown++;
    }
    D.shown = shown;   // the next rotation starts right after the last card that actually fit
  }


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
    if (next.some((li, i) => list.children[i] !== li) || list.children.length !== next.length) list.replaceChildren(...next);
    displayWin.requestAnimationFrame(() => next.forEach((li, i) => { li.querySelector('.bar i').style.width = (rank[i].v / max * 100) + '%'; }));
    for (const li of next) {
      const was = before.get(li.dataset.k);
      if (was == null) continue;
      const dy = was - li.getBoundingClientRect().top;
      if (dy) li.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }], { duration: 700, easing: 'cubic-bezier(.2,.8,.2,1)' });
    }
  }

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

  function renderStats() {
    const st = panel && panel.querySelector('.live');
    if (st) st.textContent = [live.online != null ? (live.online === 1 ? '1 person' : live.online + ' people') + ' online' : null, live.typing ? (live.typing > 1 ? live.typing + ' typing\u2026' : 'someone typing\u2026') : null, typingSock ? null : 'typing signal: present mode only'].filter(Boolean).join(' \u00b7 ');
    if (!displayWin || displayWin.closed || !D) return;
    const d = D.d;
    const set = (id, n) => {
      const x = d.getElementById(id); if (!x) return;
      const v = n == null ? '\u2013' : String(n);
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
    panel.addEventListener('keydown', e => { e.stopPropagation(); if (e.key === 'Escape') toggle(); }, true);
    panel.addEventListener('pointerdown', () => { pointerDown = true; }, true);
    const flush = () => { if (!pointerDown && renderPending) { renderPending = false; setTimeout(render, 0); } };
    window.addEventListener('pointerup', () => { pointerDown = false; setTimeout(flush, 0); }, true);
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
        !isHost ? el(d, 'div', { class: 'meta' }, `${q.voteCount} vote${q.voteCount === 1 ? '' : 's'} \u00b7 ${whoOf(q)} \u00b7 ${new Date(q.createdAt).toLocaleDateString()} \u00b7 `, tagEditor(q)) : null),
      el(d, 'div', { class: 'acts' },
        opts.order ? [
          el(d, 'button', { title: 'Move up', onclick: act(() => move(id, -1)) }, '\u2191'),
          el(d, 'button', { title: 'Move down', onclick: act(() => move(id, 1)) }, '\u2193'),
        ] : null,
        el(d, 'button', { class: hero ? 'on' : '', title: 'Question of the night', onclick: act(() => { S.hero = hero ? null : id; }) }, hero ? 'QOTN \u2713' : 'QOTN'),
        el(d, 'button', { class: feat ? 'on' : '', onclick: act(() => { S.featured = toggleIn(S.featured, id); }) }, feat ? 'On board' : 'Feature'),
        !isHost && !opts.order ? el(d, 'button', { class: hid ? 'on' : '', title: 'Keep off the display (rotation, top voted, latest, categories)', onclick: act(() => { S.hidden = toggleIn(S.hidden, id); }) }, hid ? 'Unhide' : 'Hide') : null,
        isHost && opts.order ? el(d, 'button', { title: 'Delete host card', onclick: act(() => {
          S.custom = S.custom.filter(c => c.id !== id); S.featured = S.featured.filter(x => x !== id); if (S.hero === id) S.hero = null;
        }) }, '\u2715') : null));
  }

  function tagEditor(q) {
    const d = document, cur = tagsOf(q);
    const setTags = next => { S.tagOverride[q.id] = next; save(); render(); };
    const chips = cur.map((k, i) => el(d, 'span', { class: 'chip' + (i === 0 ? ' main' : ''), title: i === 0 ? 'Main tag' : 'Click to make this the main tag',
        onclick: e => { e.stopPropagation(); if (i) setTags([k, ...cur.filter(x => x !== k)]); } },
      TAG_NAME[k], el(d, 'b', { title: 'Remove tag', onclick: e => { e.stopPropagation(); setTags(cur.filter(x => x !== k)); } }, '\u00d7')));
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
    const bulk = hide => act(() => { S.hidden = hide ? [...new Set([...S.hidden, ...poolIds.filter(id => id !== S.hero)])] : S.hidden.filter(id => !poolIds.includes(id)); });
    const hero = byId(S.hero);
    const dispOpen = displayWin && !displayWin.closed;

    const active = d.activeElement && d.activeElement.dataset ? d.activeElement.dataset.k : null;
    const selStart = active ? d.activeElement.selectionStart : null;
    const scrolls = [...panel.querySelectorAll('.list')].map(n => n.scrollTop);

    const customIn = el(d, 'input', { type: 'text', 'data-k': 'custom', placeholder: 'Add a host card (e.g. a framing line or scripture)\u2026' });
    const addCustom = () => { const t = customIn.value.trim(); if (!t) return; const id = 'c' + Date.now(); S.custom.push({ id, text: t }); S.featured.push(id); customIn.value = ''; save(); render(); };
    customIn.addEventListener('keydown', e => { if (e.key === 'Enter') addCustom(); });

    const headIn = el(d, 'input', { type: 'text', 'data-k': 'heading', value: S.heading });
    headIn.addEventListener('input', () => { S.heading = headIn.value; save(); renderDisplay(); });
    const subIn = el(d, 'input', { type: 'text', 'data-k': 'sub', value: S.sub });
    subIn.addEventListener('input', () => { S.sub = subIn.value; save(); renderDisplay(); });
    const searchIn = el(d, 'input', { type: 'text', 'data-k': 'search', placeholder: 'Search questions\u2026', value: search });
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
          hero ? el(d, 'div', { class: 'hero' }, el(d, 'b', {}, 'QOTN: '), textOf(hero)) : el(d, 'div', { class: 'note' }, 'No question of the night set \u2014 click QOTN on any question or host card.'),
          el(d, 'div', { class: 'bar' }, customIn, el(d, 'button', { class: 'pri', onclick: addCustom }, 'Add')),
          S.mode === 'related' ? el(d, 'div', { class: 'note' }, hero && mainTag(hero)
            ? `Rotating ${relatedPool().length} questions tagged "${TAG_NAME[mainTag(hero)] || '\u2014'}" (the QOTN's main tag): two on screen, one swaps every ${SWAP_MS / 1000}s. Tag a question at left to pull it in or out.`
            : 'Set a question of the night that has a tag (an audience question, not a host card) to rotate its main tag.') : null,
          S.mode === 'live' ? el(d, 'div', { class: 'note' }, 'Live mode shows the top 6 unanswered questions by votes (minus hidden ones). Switch to Curated to use your order below.') : null,
          el(d, 'div', { class: 'list' },
            S.mode === 'featured'
              ? (S.featured.length ? S.featured.map(byId).filter(Boolean).map(x => row(x, { order: true })) : el(d, 'div', { class: 'note' }, 'Nothing featured yet \u2014 click Feature on questions at left.'))
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