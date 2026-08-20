# Open Journal Radar

A standing scan of an open-access journal that produces **research directions**, not a
mirror of the journal.

Each run fetches bibliographic metadata, dedups against a ledger so previously seen
papers are discarded, clusters what is left, and writes a dated snapshot. The analysis —
which gaps the corpus leaves open, and why they have persisted — is the output that
matters. Papers are cited and linked; no article text is reproduced.

Currently pointed at **IEEE Open Journal of the Computer Society** (ISSN 2644-1268).

## Latest scan

`scans/2026-08-19-21-50/` — 235 papers scanned, 63 removed by the standing filter, 172 eligible, 32 cited across 6 directions.

| File | What it is |
|---|---|
| `directions.md` | The six research directions, each with its cited papers |
| `direction-01-paper-skeleton.md` | Full study design for the strongest direction |
| `scan-summary.md` | Cluster breakdown and every paper scanned, linked |
| `papers.json` | Bibliographic records for the run |
| `radar.html` | Standalone interactive page — open it in a browser |

## Standing topic filter

`tools/topic_filter.py` holds a persistent exclusion list applied on **every** scan, so
unwanted themes never reach the candidate pool and the preference does not have to be
restated each run. Current exclusions: **security, privacy, fraud, governance**.

Filtered papers are not deleted. They stay in `papers.json` and the ledger tagged with
`excluded_by`, and appear greyed in the scan summary — so the corpus record stays
complete and the filter stays auditable.

Matching is on **titles only**, deliberately. OpenAlex `topics` and `concepts` are
auto-assigned and noisy: an AIOps paper on log and metric anomalies picks up "Advanced
Malware Detection Techniques", and a cryptocurrency forecasting paper picks up security
topics from the word "crypto". Matching those fields cut reliability and forecasting work
that was not excluded work at all. The trade-off is that a paper with a neutral title can
slip through — the better failure mode, and title matching keeps the reason a paper was
cut visible in its own name.

Edit `EXCLUSIONS` to change it; each entry is a case-insensitive regex.

## Running a scan

Standard library only. No dependencies to install.

```bash
python3 tools/fetch_scan.py --out "scans/$(date +%Y-%m-%d-%H-%M)"
```

Point it at a different journal by ISSN:

```bash
python3 tools/fetch_scan.py --issn 2644-1268 --since 2025-01-01 --out scans/my-run
```

Each run writes `papers.json`, `new-since-last-scan.json` and `scan-summary.md`, and
updates `data/scan_ledger.db`.

## The scan ledger

`data/scan_ledger.db` is a SQLite ledger of every paper ever scanned, so repeat runs
surface only new work.

Dedup is a three-key probe — OpenAlex ID, then DOI, then a normalised title hash — and
every one resolves as `SEARCH ... USING COVERING INDEX`, never a table scan, so lookups
stay flat as the ledger grows toward a million rows. Ingest batches into a single
transaction under WAL. The row payload deliberately excludes abstracts and author blobs,
which keeps roughly 200 MB at 1M rows with the hot indexes resident in page cache.

```
run 1: fetched=235  new=234  skipped=1     (1 intra-batch title duplicate)
run 2: fetched=235  new=0    skipped=235   dedup working
```

## Cadence

The workflow in `.github/workflows/weekly-scan.yml` runs **weekly**, not daily.

This journal published 142 papers in 2025 and 93 so far in 2026 — roughly six a month,
about 0.2 a day. With dedup working, a daily run would return zero new papers on roughly
four days in five. Weekly produces a batch worth reading; monthly also works.

The workflow performs the deterministic half — fetch, dedup, cluster, commit the
snapshot. It does **not** write research directions, which require a model. Treat the
committed `new-since-last-scan.json` as the input to that step.

## On rights

This repository reproduces no abstracts and no article text. It stores bibliographic
fact — title, authors, year, citation count, DOI — plus original analysis. `fetch_scan.py`
never reads the abstract field OpenAlex returns. Every paper links to the publisher of
record, where the journal's open-access licence terms apply.

## Method and limits

- Records come from [OpenAlex](https://openalex.org); IEEE Xplore refuses automated requests.
- Clusters use title-first keyword rules with a topic-weighted fallback. Useful for
  orientation, not authoritative.
- Citation counts favour papers with several months of exposure, so recent work is
  under-ranked by construction. The cluster breakdown is the better guide to what is
  being published now.

## Layout

```
scans/<YYYY-MM-DD-HH-MM>/   dated snapshots
tools/fetch_scan.py         fetch → cluster → dedup → emit
tools/scan_db.py            the ledger: schema, ingest, dedup
tools/gen.py                renders the interactive page
tools/ideas.py refs.py      the directions and their citations
data/scan_ledger.db         dedup ledger
```
