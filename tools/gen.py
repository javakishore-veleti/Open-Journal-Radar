import json, html, datetime, sqlite3, collections
from ideas import IDEAS
from refs import IDEA_REFS
from topic_filter import partition, EXCLUSIONS

all_rows = json.load(open('../ojcs_all.json'))
rows, filtered = partition(all_rows)   # standing exclusions applied on every build
NOW = datetime.datetime.now(); STAMP = NOW.strftime('%d %B %Y')
by_title = {r['title']: r for r in rows}
def find(frag): return next(r for r in rows if frag.lower() in r['title'].lower())

db = sqlite3.connect('scan_ledger.db')
ledger_n = db.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
runs = db.execute("SELECT run_id,n_fetched,n_new,n_skipped FROM runs ORDER BY run_id").fetchall()

def esc(s): return html.escape(str(s))
def byline(p):
    a = p['authors']
    if not a: return '&mdash;'
    if len(a) == 1: return esc(a[0])
    if p['n_authors'] == 2: return esc(a[0]) + ' &amp; ' + esc(a[1])
    return esc(a[0]) + ' <i>et al.</i>'

clusters = collections.Counter(r['cluster'] for r in rows)
filt_str = ', '.join(f"<b>{k}</b> ({v})" for k,v in collections.Counter(n for p in filtered for n in p['excluded_by']).most_common())
maxn = max(clusters.values())
cited = {r['title'] for v in IDEA_REFS.values() for r in [find(f) for f in v]}
filt_counts = collections.Counter(n for p in filtered for n in p['excluded_by'])

# ---------- idea cards ----------
cards = []
for n, it in enumerate(IDEAS, 1):
    ev = []
    for frag in IDEA_REFS[it['id']]:
        p = find(frag)
        ev.append(f'''<li><a href="https://doi.org/{esc(p['doi'])}" target="_blank" rel="noopener">
   <span class="ev-t">{esc(p['title'])}</span>
   <span class="ev-m">{byline(p)} <span class="dot">&middot;</span> {p['year']} <span class="dot">&middot;</span> <span class="ev-c">{p['cites']} citations</span> <span class="dot">&middot;</span> {esc(p['cluster'])}</span></a></li>''')
    cards.append(f'''<article class="idea" id="{it['id']}">
 <div class="idea-num">{n:02d}</div>
 <div class="idea-inner">
  <header class="idea-head"><span class="idea-kicker">{it['kicker']}</span><span class="idea-tag">{it['tag']}</span></header>
  <h3 class="idea-title">{it['title']}</h3>
  <p class="idea-thesis">{it['thesis']}</p>
  <div class="idea-grid">
   <section><h4>The gap in this month&rsquo;s output</h4><p>{it['gap']}</p></section>
   <section><h4>What to build</h4><p>{it['proposal']}</p></section>
   <section><h4>First experiment</h4><p>{it['experiment']}</p></section>
   <section class="edge"><h4>Why it is under-attempted</h4><p>{it['barrier']}</p></section>
  </div>
  <div class="evidence">
   <h4>Built on {len(ev)} papers from this scan <span class="ev-note">&mdash; titles and links only; open each at the publisher</span></h4>
   <ol class="ev-list">{''.join(ev)}</ol>
  </div>
  <footer class="idea-foot"><span class="st"><b>Effort</b> {it['effort']}</span><span class="st"><b>Venue read</b> {it['venue']}</span></footer>
 </div>
</article>''')

# ---------- cluster bars ----------
bars = []
for name, n in clusters.most_common():
    c = sum(1 for t in cited if by_title[t]['cluster'] == name)
    bars.append(f'''<div class="fm-row" tabindex="0" data-tip="{esc(name)}: {n} papers scanned, {c} cited by a research direction">
 <span class="fm-label">{esc(name)}</span>
 <span class="fm-track"><span class="fm-all" style="width:{n/maxn*100:.1f}%"><span class="fm-sub" style="width:{(c/n*100) if n else 0:.1f}%"></span></span></span>
 <span class="fm-n">{n}</span></div>''')

# ---------- full index ----------
idx = []
for p in sorted(all_rows, key=lambda r: (-r['cites'], r['title'])):
    star = ' <span class="star" title="Cited by a research direction above">&#9679;</span>' if p['title'] in cited else ''
    ex = p.get('excluded_by') or []
    idx.append(f'''<li class="ix{' ix-out' if ex else ''}" data-cluster="{esc(p['cluster'])}" data-cited="{'1' if p['title'] in cited else '0'}" data-filtered="{'1' if ex else '0'}" data-text="{esc((p['title']+' '+' '.join(p['authors'])+' '+p['cluster']).lower())}">
 <a href="https://doi.org/{esc(p['doi'])}" target="_blank" rel="noopener" class="ix-t">{esc(p['title'])}</a>{star}
 <span class="ix-m">{byline(p)} <span class="dot">&middot;</span> {p['year']} <span class="dot">&middot;</span> {esc(p['cluster'])} <span class="dot">&middot;</span> <span class="ix-c">{p['cites']} cit.</span>{f' <span class="flt">filtered: {esc(", ".join(ex))}</span>' if ex else ''}</span></li>''')

chipbar = ' '.join(f'<button class="chip" data-cluster="{esc(c)}">{esc(c)} <span class="chip-n">{n}</span></button>' for c, n in clusters.most_common())

HTML = f'''<title>Open Journal Radar</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
:root{{
 --bg:#EDEFEC;--surface:#FBFCFA;--sunken:#E7EAE7;
 --ink:#101614;--ink-2:#48544F;--ink-3:#78837E;
 --rule:#D2D8D3;--rule-2:#BFC7C1;
 --accent:#14675C;--accent-soft:#CFE2DC;--accent-ghost:#DEEBE6;--heat:#8A6206;
 --shadow:0 1px 2px rgba(16,22,20,.05),0 10px 30px -14px rgba(16,22,20,.16);
 --sans:'Archivo',ui-sans-serif,system-ui,sans-serif;
 --serif:'Source Serif 4',Georgia,'Times New Roman',serif;
 --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
 --measure:66ch;--pad:clamp(1.15rem,4vw,2.75rem);
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
 --bg:#0B100E;--surface:#131A17;--sunken:#0F1513;
 --ink:#E9EEEB;--ink-2:#9DAAA4;--ink-3:#6E7A75;
 --rule:#242E29;--rule-2:#33403A;
 --accent:#5BC6B0;--accent-soft:#183A34;--accent-ghost:#14231F;--heat:#DDAE45;
 --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 34px -16px rgba(0,0,0,.75);
}}}}
:root[data-theme="dark"]{{
 --bg:#0B100E;--surface:#131A17;--sunken:#0F1513;
 --ink:#E9EEEB;--ink-2:#9DAAA4;--ink-3:#6E7A75;
 --rule:#242E29;--rule-2:#33403A;
 --accent:#5BC6B0;--accent-soft:#183A34;--accent-ghost:#14231F;--heat:#DDAE45;
 --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 34px -16px rgba(0,0,0,.75);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--serif);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1080px;margin:0 auto;padding-left:var(--pad);padding-right:var(--pad)}}
h1,h2,h3,h4{{font-family:var(--sans);text-wrap:balance;margin:0}}
a{{color:var(--accent)}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}}
.lab{{font-family:var(--sans);font-size:.66rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);margin:0}}
.dot{{opacity:.45;margin:0 .18rem}}

.mast{{border-bottom:1px solid var(--rule);background:var(--surface)}}
.mast-in{{display:flex;flex-wrap:wrap;gap:1.5rem 2rem;align-items:flex-end;justify-content:space-between;padding-top:clamp(2rem,5vw,3.4rem);padding-bottom:1.6rem}}
.mast h1{{font-size:clamp(2.1rem,5.2vw,3.35rem);font-weight:700;line-height:1.02;letter-spacing:-.032em;max-width:15ch;margin-top:.5rem}}
.mast h1 em{{font-style:normal;color:var(--accent);display:block}}
.mast-sub{{font-family:var(--sans);font-size:.95rem;color:var(--ink-2);margin:.9rem 0 0;max-width:54ch;line-height:1.55}}
.stamp{{font-family:var(--mono);font-size:.74rem;color:var(--ink-3);text-align:right;line-height:1.9;flex-shrink:0}}
.stamp b{{color:var(--ink);font-weight:500;display:block;font-size:.82rem}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--rule);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}}
.stat{{background:var(--surface);padding:1.05rem var(--pad) 1.15rem}}
.stat .n{{font-family:var(--sans);font-size:1.9rem;font-weight:700;letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:1.1;display:block}}
.stat .k{{font-family:var(--sans);font-size:.68rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-top:.3rem;display:block}}
.stats .stat:first-child .n{{color:var(--accent)}}

section.band{{padding-top:clamp(2.6rem,6vw,4.4rem)}}
.sec-head{{display:flex;flex-wrap:wrap;align-items:baseline;gap:.5rem 1.2rem;border-bottom:2px solid var(--ink);padding-bottom:.55rem;margin-bottom:1.6rem}}
.sec-head h2{{font-size:clamp(1.35rem,3vw,1.9rem);font-weight:700;letter-spacing:-.024em}}
.sec-head p{{margin:0;font-family:var(--sans);font-size:.87rem;color:var(--ink-2);flex:1 1 22ch;min-width:0}}

.ideas{{display:flex;flex-direction:column;gap:1.3rem}}
.idea{{background:var(--surface);border:1px solid var(--rule);border-radius:10px;box-shadow:var(--shadow);display:grid;grid-template-columns:auto 1fr;overflow:hidden}}
.idea-num{{font-family:var(--mono);font-size:.8rem;color:var(--accent);background:var(--accent-ghost);border-right:1px solid var(--rule);padding:1.4rem .85rem;font-variant-numeric:tabular-nums}}
.idea-inner{{padding:clamp(1.2rem,3vw,1.9rem);min-width:0}}
.idea-head{{display:flex;flex-wrap:wrap;gap:.6rem 1rem;align-items:center;justify-content:space-between;margin-bottom:.7rem}}
.idea-kicker{{font-family:var(--sans);font-size:.67rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--accent)}}
.idea-tag{{font-family:var(--sans);font-size:.68rem;font-weight:600;color:var(--ink-3);border:1px solid var(--rule-2);border-radius:99px;padding:.16rem .6rem}}
.idea-title{{font-size:clamp(1.18rem,2.6vw,1.55rem);font-weight:700;letter-spacing:-.024em;line-height:1.18}}
.idea-thesis{{font-size:1.06rem;line-height:1.5;color:var(--ink-2);margin:.6rem 0 1.5rem;max-width:60ch;font-style:italic}}
.idea-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));gap:1.35rem 2.2rem}}
.idea-grid h4,.evidence h4{{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.45rem}}
.idea-grid p{{margin:0;font-size:.94rem;line-height:1.58;color:var(--ink-2)}}
.idea-grid b{{color:var(--ink);font-weight:600}}
.idea-grid .edge h4{{color:var(--accent)}}
.idea-grid .edge{{border-left:2px solid var(--accent-soft);padding-left:1.05rem}}
.evidence{{margin-top:1.6rem;padding-top:1.1rem;border-top:1px solid var(--rule)}}
.ev-note{{font-weight:500;letter-spacing:0;text-transform:none;color:var(--ink-3);font-size:.72rem}}
.ev-list{{list-style:none;margin:0;padding:0;display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:6px;overflow:hidden}}
.ev-list li{{background:var(--surface)}}
.ev-list a{{display:block;padding:.6rem .75rem;text-decoration:none;color:inherit}}
.ev-list a:hover{{background:var(--accent-ghost)}}
.ev-t{{display:block;font-family:var(--sans);font-size:.87rem;font-weight:600;line-height:1.32;color:var(--accent)}}
.ev-m{{display:block;font-family:var(--sans);font-size:.74rem;color:var(--ink-3);margin-top:.2rem}}
.ev-c{{font-family:var(--mono);font-size:.71rem}}
.idea-foot{{display:flex;flex-wrap:wrap;gap:.4rem 1.6rem;margin-top:1.2rem;padding-top:.9rem;border-top:1px solid var(--rule)}}
.st{{font-family:var(--sans);font-size:.76rem;color:var(--ink-3)}}
.st b{{color:var(--ink-2);font-weight:600}}

.fm{{display:flex;flex-direction:column;gap:.42rem;margin-bottom:.6rem}}
.fm-row{{display:grid;grid-template-columns:minmax(0,15rem) 1fr 2.4rem;gap:.9rem;align-items:center;border-radius:4px}}
.fm-label{{font-family:var(--sans);font-size:.83rem;color:var(--ink-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.fm-track{{height:15px;border-radius:2px;overflow:hidden;box-shadow:inset 0 0 0 1px var(--rule)}}
.fm-all{{display:block;height:100%;background:var(--accent-soft);border-radius:2px;position:relative}}
.fm-sub{{position:absolute;inset:0 auto 0 0;background:var(--accent);border-radius:2px 0 0 2px}}
.fm-n{{font-family:var(--mono);font-size:.78rem;color:var(--ink-2);text-align:right;font-variant-numeric:tabular-nums}}
.excl{{font-family:var(--sans);font-size:.86rem;line-height:1.55;color:var(--ink-2);background:var(--accent-ghost);border-left:2px solid var(--accent);border-radius:0 6px 6px 0;padding:.85rem 1.1rem;margin:0 0 1.4rem;max-width:74ch}}
.excl b{{color:var(--ink)}}
.fm-legend{{display:flex;flex-wrap:wrap;gap:1.25rem;font-family:var(--sans);font-size:.75rem;color:var(--ink-2);margin-bottom:1.1rem}}
.fm-legend span{{display:inline-flex;align-items:center;gap:.42rem}}
.sw{{width:11px;height:11px;border-radius:2px;display:inline-block}}
.sw.a{{background:var(--accent)}}.sw.b{{background:var(--accent-soft)}}

.controls{{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--rule);padding:.8rem 0;display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}}
.search{{flex:1 1 15rem;min-width:0;font-family:var(--sans);font-size:.87rem;padding:.5rem .75rem;border:1px solid var(--rule-2);border-radius:5px;background:var(--surface);color:var(--ink)}}
.search::placeholder{{color:var(--ink-3)}}
.sortbtn{{font-family:var(--sans);font-size:.78rem;font-weight:600;padding:.5rem .8rem;border:1px solid var(--rule-2);border-radius:5px;background:var(--surface);color:var(--ink-2);cursor:pointer}}
.sortbtn[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:var(--surface)}}
.chips{{display:flex;flex-wrap:wrap;gap:.4rem;width:100%}}
.chip{{font-family:var(--sans);font-size:.75rem;font-weight:500;padding:.32rem .6rem;border:1px solid var(--rule-2);border-radius:99px;background:transparent;color:var(--ink-2);cursor:pointer;display:inline-flex;gap:.4rem;align-items:center}}
.chip:hover{{border-color:var(--ink-3);color:var(--ink)}}
.chip[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:var(--surface)}}
.chip-n{{font-family:var(--mono);font-size:.68rem;opacity:.7}}
.index{{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}}
.ix{{border-bottom:1px solid var(--rule);padding:.62rem .25rem}}
.ix.hidden{{display:none}}
.ix-t{{font-family:var(--sans);font-size:.9rem;font-weight:600;line-height:1.33;text-decoration:none;color:var(--ink)}}
.ix-t:hover{{color:var(--accent);text-decoration:underline}}
.ix-m{{display:block;font-family:var(--sans);font-size:.74rem;color:var(--ink-3);margin-top:.2rem}}
.ix-c{{font-family:var(--mono);font-size:.71rem}}
.star{{color:var(--accent);font-size:.6rem;vertical-align:middle}}
.ix-out .ix-t{{color:var(--ink-3);font-weight:500}}
.ix-out{{opacity:.72}}
.flt{{font-family:var(--mono);font-size:.68rem;color:var(--heat);border:1px solid var(--heat-soft);border-radius:3px;padding:0 .3rem;margin-left:.35rem;white-space:nowrap}}
.empty{{padding:2rem .25rem;font-family:var(--sans);font-size:.9rem;color:var(--ink-3)}}

footer.note{{margin-top:clamp(3rem,7vw,5rem);border-top:1px solid var(--rule);background:var(--surface)}}
footer.note .wrap{{padding-top:2rem;padding-bottom:2.8rem}}
footer.note p{{max-width:var(--measure);font-size:.88rem;color:var(--ink-2);margin:.55rem 0 0}}
footer.note h3{{font-size:.95rem;margin-top:1.7rem}}
code{{font-family:var(--mono);font-size:.82em;background:var(--sunken);padding:.1rem .35rem;border-radius:3px}}
.rights{{border-left:2px solid var(--accent);padding-left:1.1rem;margin-top:1.4rem}}
.tip{{position:fixed;z-index:60;pointer-events:none;background:var(--ink);color:var(--bg);font-family:var(--sans);font-size:.75rem;padding:.35rem .55rem;border-radius:4px;opacity:0;transition:opacity .12s;max-width:22rem}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important;scroll-behavior:auto!important}}}}
@media (max-width:640px){{
 .idea{{grid-template-columns:1fr}}
 .idea-num{{border-right:0;border-bottom:1px solid var(--rule);padding:.5rem .9rem}}
 .fm-row{{grid-template-columns:minmax(0,9rem) 1fr 2rem;gap:.6rem}}
 .stamp{{text-align:left}}
}}
html{{scroll-behavior:smooth}}
</style>

<header class="mast">
 <div class="wrap mast-in">
  <div>
   <p class="lab">Research directions from IEEE Open Journal of the Computer Society &middot; ISSN 2644-1268</p>
   <h1>Open Journal <em>Radar</em></h1>
   <p class="mast-sub">Six research directions argued from {len(rows)} eligible open-access papers. A standing filter removes security, privacy, fraud and governance work before anything is read &mdash; {len(filtered)} papers this run. Each direction names a gap the corpus leaves open, cites the papers that establish it, and says why the gap has persisted.</p>
  </div>
  <p class="stamp"><b>{STAMP}</b>{len(all_rows)} scanned &middot; {len(filtered)} filtered<br>{len(rows)} eligible &middot; {len(cited)} cited<br>Volumes 6&ndash;7 &middot; 2025&ndash;2026</p>
 </div>
 <div class="stats">
  <div class="stat"><span class="n">{len(IDEAS)}</span><span class="k">Research directions</span></div>
  <div class="stat"><span class="n">{len(rows)}</span><span class="k">Eligible papers</span></div>
  <div class="stat"><span class="n">{len(cited)}</span><span class="k">Papers cited</span></div>
  <div class="stat"><span class="n">{len(filtered)}</span><span class="k">Filtered out</span></div>
  <div class="stat"><span class="n">{ledger_n}</span><span class="k">In scan ledger</span></div>
 </div>
</header>

<main class="wrap">

<section class="band">
 <div class="sec-head"><h2>Six directions</h2><p>Each gap below is a real absence across the papers cited beneath it, not a generic call for future work.</p></div>
 <div class="ideas">{''.join(cards)}</div>
</section>

<section class="band">
 <div class="sec-head"><h2>Where the volume is</h2><p>All {len(rows)} scanned papers by cluster. The solid segment marks how many a direction above cites.</p></div>
 <p class="excl"><b>A standing filter runs before the corpus is read.</b> {filt_str} &mdash; {len(filtered)} of {len(all_rows)} papers this run &mdash; are removed from the candidate pool, so no direction can be built on them. Matching is on titles only: auto-assigned topic tags are too noisy, and would have cut reliability and forecasting work that is not excluded work at all. Filtered papers still appear in the index below, marked, so the filter stays auditable.</p>
 <div class="fm-legend"><span><i class="sw a"></i> Cited by a direction</span><span><i class="sw b"></i> Scanned, not cited</span></div>
 <div class="fm">{''.join(bars)}</div>
</section>

<section class="band" id="index">
 <div class="sec-head"><h2>Every paper scanned</h2><p>All {len(all_rows)} papers this run, each linking to the publisher. {'&#9679;'} marks a paper cited by a direction; greyed rows were removed by the standing filter.</p></div>
 <div class="controls">
  <input class="search" id="q" type="search" placeholder="Search titles, authors, clusters&hellip;" aria-label="Search scanned papers">
  <button class="sortbtn" id="onlycited" aria-pressed="false">Only cited</button>
  <button class="sortbtn" id="hidefiltered" aria-pressed="false">Hide filtered</button>
  <div class="chips" id="chips">{chipbar}</div>
 </div>
 <ol class="index" id="ix-list">{''.join(idx)}</ol>
 <p class="empty" id="empty" hidden>No papers match that filter.</p>
</section>

</main>

<footer class="note">
 <div class="wrap">
  <p class="lab">Method</p>
  <p>The standing filter lives in <code>tools/topic_filter.py</code> and runs on every scan, so exclusions persist across runs rather than being reapplied by hand. Clusters use title-first keyword rules with a topic-weighted fallback; an earlier revision over-matched security terms and has been corrected. IEEE Xplore refuses automated requests, so bibliographic records come from <b>OpenAlex</b> filtered to ISSN <code>2644-1268</code>, covering {len(rows)} research articles published from January 2025 onward. Front matter and reviewer lists are excluded. Clusters are assigned by keyword matching over titles and indexed topics &mdash; useful for orientation, not authoritative.</p>

  <div class="rights">
   <p><b>On rights.</b> This page reproduces no abstracts and no article text. What it contains is bibliographic fact &mdash; title, authors, year, citation count, DOI &mdash; plus original analysis written for this brief. Every paper links to the publisher of record, where IEEE&rsquo;s open-access licence terms apply. The research directions are argued from the corpus, not extracted from it; the citations exist so each claim can be checked at the source.</p>
  </div>

  <h3>Scan ledger</h3>
  <p>A local SQLite ledger (<code>scan_ledger.db</code>) records every paper ever scanned, so repeat runs surface only new work. Dedup is a three-key index probe &mdash; OpenAlex ID, then DOI, then a normalised title hash &mdash; and never a table scan, which keeps lookups flat as the ledger grows toward a million rows. Ingest batches into a single transaction under WAL, and the row payload deliberately excludes abstracts and author blobs so the hot indexes stay in page cache.</p>
  <p>Runs so far: {' &middot; '.join(f'run {r[0]} &rarr; {r[1]} fetched, <b>{r[2]} new</b>, {r[3]} already seen' for r in runs)}.</p>

  <h3>On ranking</h3>
  <p>Xplore&rsquo;s own popular-papers list is download-driven and exposed through no open API, so citation count stands in. It is a slower signal that favours papers with several months of exposure, which under-ranks 2026 work by construction &mdash; the cluster chart covers the full corpus and is the better guide to what is being published right now.</p>
 </div>
</footer>

<div class="tip" id="tip" role="status"></div>
<script>
(function(){{
 var items=[].slice.call(document.querySelectorAll('.ix'));
 var q=document.getElementById('q'),empty=document.getElementById('empty');
 var chips=[].slice.call(document.querySelectorAll('.chip')),only=document.getElementById('onlycited');
 var hidef=document.getElementById('hidefiltered');
 var active=null,citedOnly=false,hideFiltered=false;
 function apply(){{
  var t=q.value.trim().toLowerCase(),shown=0;
  items.forEach(function(el){{
   var ok=(!active||el.dataset.cluster===active)&&(!t||el.dataset.text.indexOf(t)>-1)&&(!citedOnly||el.dataset.cited==='1')&&(!hideFiltered||el.dataset.filtered==='0');
   el.classList.toggle('hidden',!ok); if(ok)shown++;
  }});
  empty.hidden=shown>0;
 }}
 q.addEventListener('input',apply);
 only.addEventListener('click',function(){{citedOnly=!citedOnly;only.setAttribute('aria-pressed',citedOnly?'true':'false');apply();}});
 hidef.addEventListener('click',function(){{hideFiltered=!hideFiltered;hidef.setAttribute('aria-pressed',hideFiltered?'true':'false');apply();}});
 chips.forEach(function(c){{
  c.setAttribute('aria-pressed','false');
  c.addEventListener('click',function(){{
   var on=active===c.dataset.cluster;
   chips.forEach(function(x){{x.setAttribute('aria-pressed','false')}});
   active=on?null:c.dataset.cluster; if(!on)c.setAttribute('aria-pressed','true'); apply();
  }});
 }});
 var tip=document.getElementById('tip');
 document.querySelectorAll('.fm-row').forEach(function(r){{
  r.addEventListener('mousemove',function(e){{tip.textContent=r.dataset.tip;tip.style.opacity='1';
   tip.style.left=Math.min(e.clientX+14,innerWidth-tip.offsetWidth-10)+'px';tip.style.top=(e.clientY+16)+'px';}});
  r.addEventListener('mouseleave',function(){{tip.style.opacity='0'}});
  r.addEventListener('focus',function(){{var b=r.getBoundingClientRect();tip.textContent=r.dataset.tip;
   tip.style.opacity='1';tip.style.left=b.left+'px';tip.style.top=(b.bottom+8)+'px';}});
  r.addEventListener('blur',function(){{tip.style.opacity='0'}});
 }});
}})();
</script>'''
open('radar.html','w').write(HTML)
print('wrote radar.html', len(HTML), 'bytes | cited papers:', len(cited))
