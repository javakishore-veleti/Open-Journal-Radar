#!/usr/bin/env python3
"""
Fetch → cluster → dedup → emit. One reproducible pass over a journal's recent output.

  python3 tools/fetch_scan.py --since 2025-01-01 --out scans/$(date +%Y-%m-%d-%H-%M)

Deliberately stdlib-only (urllib, sqlite3, json, re) so CI needs no dependency install.

IMPORTANT — rights: this fetches BIBLIOGRAPHIC METADATA ONLY. OpenAlex returns an
inverted abstract index; we never reconstruct or persist it. Titles, authors, DOIs and
citation counts are facts about the literature and are stored; article text is not.
"""
import argparse, json, os, re, sqlite3, ssl, sys, urllib.parse, urllib.request, datetime

def _ssl_ctx():
    """Some Python installs ship without a usable CA bundle; prefer certifi when present."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()

SSL_CTX  = _ssl_ctx()
OPENALEX = "https://api.openalex.org/works"
ISSN     = "2644-1268"                      # IEEE Open Journal of the Computer Society

CLUSTERS = [
 ("Software Engineering & AIOps",
  r"bug report|process mining|system software|software defect|code review|refactor|technical debt|"
  r"alert processing|incident prediction|enterprise it|data quality|data integration|log integrity|"
  r"software update|usability test|devops|microservice"),
 ("Agentic AI & LLM Systems",
  r"agentic|internet of agents|large language model|\bllm\b|multi-agent|generative ai|prompt engineering|fine-tuning"),
 ("Privacy & Federated Learning",
  r"federated|homomorphic|unlearning|zero-knowledge|\bzk-|differential privacy|privacy-preserving"),
 ("Security & Threat Detection",
  r"intrusion|malware|ransomware|cyber threat|cybersecurity|attack|adversar|deception|"
  r"authentication|\bpuf\b|threat|penetration|botnet|phishing|forensic"),
 ("Fraud & Financial Analytics",
  r"fraud|money laundering|cbdc|card-not-present|churn|purchaser|sales forecast|cryptocurrency|load price|volatility"),
 ("Health & Biomedical AI",
  r"health|clinical|medical|tumou?r|\becg\b|\beeg\b|patient|disease|diagnos|pneumonia|retinopathy|"
  r"autism|parkinson|maternal|elderly|rehabilit|alaryngeal|\bcpr\b|arrhythmia|neurological"),
 ("Multimodal & Vision",
  r"multimodal|multi-modal|vision transformer|\bclip\b|segmentation|image|video|colorization|\bocr\b|"
  r"iris|deepfake|watermark|visual|scene understanding"),
 ("Networks, Cloud & Edge",
  r"\b5g\b|routing|cloud|data cent|scheduling|edge comput|spectrum|\bmimo\b|\bris\b|swipt|\biot\b|"
  r"\buav\b|smart home|orchestration|network|resource allocation"),
 ("Learning Theory & Optimization",
  r"optimiz|quantum|spiking|kolmogorov|kernel|representer|pruning|self-supervised|open-set|"
  r"incremental learning|pseudo label|hyperparameter|ensemble|contrastive|representation learning"),
]
SKIP_TITLE = re.compile(r"reviewers list|^editorial|^front cover|^table of contents|^guest editorial", re.I)


def cluster_of(title, topics, concepts):
    t = title.lower()
    for name, pat in CLUSTERS:
        if re.search(pat, t): return name
    hay = (title + ' ' + ' '.join(topics) + ' ' + ' '.join(concepts)).lower()
    best, bn = "Applied ML & Forecasting", 0
    for name, pat in CLUSTERS:
        n = len(re.findall(pat, hay))
        if n > bn: best, bn = name, n
    return best


def fetch(issn, since, mailto):
    """Page through OpenAlex. Metadata only — the abstract index is discarded on read."""
    out, cursor = [], "*"
    while cursor:
        q = urllib.parse.urlencode({
            "filter": f"primary_location.source.issn:{issn},from_publication_date:{since}",
            "per-page": "200", "cursor": cursor, "mailto": mailto})
        req = urllib.request.Request(f"{OPENALEX}?{q}", headers={"User-Agent": f"open-journal-radar ({mailto})"})
        with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as r:
            d = json.load(r)
        for w in d.get("results", []):
            title = (w.get("title") or "").strip()
            if not title or SKIP_TITLE.search(title): continue
            topics   = [t["display_name"] for t in (w.get("topics") or [])[:3]]
            concepts = [c["display_name"] for c in (w.get("concepts") or []) if c.get("score", 0) > .4][:6]
            auths    = w.get("authorships") or []
            out.append({
                "id": w["id"].split("/")[-1],
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "title": title,
                "year": w.get("publication_year"),
                "date": w.get("publication_date"),
                "cites": w.get("cited_by_count", 0),
                "authors": [a["author"]["display_name"] for a in auths][:6],
                "n_authors": len(auths),
                "institutions": sorted({i["display_name"] for a in auths for i in (a.get("institutions") or [])})[:4],
                "countries": sorted({c for a in auths for c in (a.get("countries") or [])}),
                "topics": topics,
                "concepts": concepts,
                "cluster": cluster_of(title, topics, concepts),
                # NOTE: w["abstract_inverted_index"] deliberately not read, not stored.
            })
        cursor = (d.get("meta") or {}).get("next_cursor")
        if not d.get("results"): break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issn", default=ISSN)
    ap.add_argument("--since", default="2025-01-01")
    ap.add_argument("--db", default="data/scan_ledger.db")
    ap.add_argument("--out", required=True, help="snapshot directory, e.g. scans/2026-08-19-21-50")
    ap.add_argument("--mailto", default=os.environ.get("OPENALEX_MAILTO", "research@example.com"))
    a = ap.parse_args()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from scan_db import connect, ingest
    from topic_filter import partition, EXCLUSIONS

    print(f"fetching {a.issn} since {a.since} …")
    papers = fetch(a.issn, a.since, a.mailto)
    print(f"  {len(papers)} papers returned")
    eligible, filtered = partition(papers)      # standing exclusions, tagged in place
    print(f"  {len(eligible)} eligible, {len(filtered)} filtered "
          f"({', '.join(sorted(EXCLUSIONS))})")

    os.makedirs(os.path.dirname(a.db) or ".", exist_ok=True)
    db = connect(a.db)
    new, skipped, run_id = ingest(db, papers, a.issn)
    print(f"  run {run_id}: {len(new)} new, {skipped} already in ledger")

    os.makedirs(a.out, exist_ok=True)
    json.dump(papers, open(f"{a.out}/papers.json", "w"), indent=1)
    json.dump(new,    open(f"{a.out}/new-since-last-scan.json", "w"), indent=1)
    json.dump([p for p in new if not p["excluded_by"]],
              open(f"{a.out}/new-eligible.json", "w"), indent=1)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    by_cluster = {}
    for p in eligible: by_cluster[p["cluster"]] = by_cluster.get(p["cluster"], 0) + 1

    with open(f"{a.out}/scan-summary.md", "w") as f:
        f.write(f"# Scan summary\n\n")
        f.write(f"- **Run:** {run_id} · {now}\n- **Source:** ISSN {a.issn}, published since {a.since}\n")
        f.write(f"- **Returned:** {len(papers)} · **New this run:** {len(new)} · **Already seen:** {skipped}\n")
        f.write(f"- **Eligible:** {len(eligible)} · **Filtered by standing exclusions:** {len(filtered)}\n")
        f.write(f"- **Ledger total:** {db.execute('SELECT COUNT(*) FROM papers').fetchone()[0]}\n\n")
        f.write("## By cluster (eligible only)\n\n| Cluster | Papers |\n|---|---:|\n")
        for k, v in sorted(by_cluster.items(), key=lambda x: -x[1]): f.write(f"| {k} | {v} |\n")
        fc = {}
        for p in filtered:
            for n in p["excluded_by"]: fc[n] = fc.get(n, 0) + 1
        f.write("\n## Removed by standing filter\n\n| Exclusion | Papers |\n|---|---:|\n")
        for k, v in sorted(fc.items(), key=lambda x: -x[1]): f.write(f"| {k} | {v} |\n")
        if new:
            f.write(f"\n## New since last scan ({len(new)})\n\n")
            for p in sorted(new, key=lambda x: -x["cites"]):
                link = f"https://doi.org/{p['doi']}" if p["doi"] else ""
                tag = f" — **filtered: {', '.join(p['excluded_by'])}**" if p["excluded_by"] else ""
                f.write(f"- [{p['title']}]({link}) — {p['year']}, {p['cites']} citations, _{p['cluster']}_{tag}\n")
        else:
            f.write("\n## New since last scan\n\nNone. Every paper returned was already in the ledger.\n")
    print(f"  wrote {a.out}/")

if __name__ == "__main__":
    main()
