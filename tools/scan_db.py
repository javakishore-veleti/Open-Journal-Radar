#!/usr/bin/env python3
"""
Journal scan ledger — dedup store for IEEE Open Journal of the Computer Society.

Purpose: remember every paper already scanned so subsequent runs surface ONLY new
work. Designed to stay fast at ~1M rows.

Scale notes:
  * Dedup is an index probe, not a table scan: UNIQUE(openalex_id), UNIQUE(doi),
    and INDEX(title_hash) as a fallback for records with neither.
  * Ingest runs in ONE transaction with executemany + INSERT..ON CONFLICT, so a
    batch is O(n log n) on index maintenance, not O(n) round trips.
  * WAL journal + NORMAL sync: concurrent readers never block the writer.
  * Payload stays narrow (no abstracts, no author blobs) so 1M rows is ~200MB and
    the hot indexes stay resident in page cache.
"""
import sqlite3, hashlib, re, json, datetime, os, sys

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS runs (
  run_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  started_utc TEXT NOT NULL,
  source_issn TEXT NOT NULL,
  n_fetched   INTEGER DEFAULT 0,
  n_new       INTEGER DEFAULT 0,
  n_skipped   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS papers (
  paper_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  openalex_id    TEXT NOT NULL,
  doi            TEXT,
  title          TEXT NOT NULL,
  title_hash     TEXT NOT NULL,
  source_issn    TEXT NOT NULL,
  pub_year       INTEGER,
  pub_date       TEXT,
  cited_by       INTEGER NOT NULL DEFAULT 0,
  cluster        TEXT,
  link           TEXT,
  first_seen_utc TEXT NOT NULL,
  last_seen_utc  TEXT NOT NULL,
  first_run_id   INTEGER NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_oaid  ON papers(openalex_id);
CREATE UNIQUE INDEX IF NOT EXISTS ux_papers_doi   ON papers(doi) WHERE doi IS NOT NULL;
CREATE        INDEX IF NOT EXISTS ix_papers_thash ON papers(title_hash);
CREATE        INDEX IF NOT EXISTS ix_papers_run   ON papers(first_run_id);
CREATE        INDEX IF NOT EXISTS ix_papers_cited ON papers(source_issn, cited_by DESC);
"""

def norm_title(t):
    return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()

def title_hash(t):
    return hashlib.sha1(norm_title(t).encode()).hexdigest()

def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db

def ingest(db, records, issn):
    """Insert only unseen papers. Returns (new_records, skipped_count, run_id)."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    cur = db.execute("INSERT INTO runs(started_utc, source_issn) VALUES(?,?)", (now, issn))
    run_id = cur.lastrowid

    # One probe per key type, batched — index lookups, never a scan.
    oaids  = {r['id'] for r in records}
    dois   = {r['doi'] for r in records if r.get('doi')}
    thashes= {title_hash(r['title']) for r in records}

    def seen(col, vals):
        out = set()
        vals = list(vals)
        for i in range(0, len(vals), 900):           # stay under SQLITE_MAX_VARIABLE_NUMBER
            chunk = vals[i:i+900]
            q = f"SELECT {col} FROM papers WHERE {col} IN ({','.join('?'*len(chunk))})"
            out |= {row[0] for row in db.execute(q, chunk)}
        return out

    seen_oa, seen_doi, seen_th = seen('openalex_id', oaids), seen('doi', dois), seen('title_hash', thashes)

    new, skipped = [], 0
    batch_th = set()
    for r in records:
        th = title_hash(r['title'])
        if (r['id'] in seen_oa) or (r.get('doi') and r['doi'] in seen_doi) or (th in seen_th) or (th in batch_th):
            skipped += 1
            continue
        batch_th.add(th)
        new.append(r)

    db.executemany("""
      INSERT INTO papers(openalex_id,doi,title,title_hash,source_issn,pub_year,pub_date,
                         cited_by,cluster,link,first_seen_utc,last_seen_utc,first_run_id)
      VALUES(:id,:doi,:title,:th,:issn,:year,:date,:cites,:cluster,:link,:now,:now,:run)
      ON CONFLICT(openalex_id) DO UPDATE SET
        cited_by=excluded.cited_by, last_seen_utc=excluded.last_seen_utc
    """, [dict(r, th=title_hash(r['title']), issn=issn, now=now, run=run_id,
               link=f"https://doi.org/{r['doi']}" if r.get('doi') else None) for r in new])

    # Refresh citation counts + last_seen for papers we already had.
    db.executemany("UPDATE papers SET cited_by=?, last_seen_utc=? WHERE openalex_id=?",
                   [(r['cites'], now, r['id']) for r in records if r['id'] in seen_oa])

    db.execute("UPDATE runs SET n_fetched=?, n_new=?, n_skipped=? WHERE run_id=?",
               (len(records), len(new), skipped, run_id))
    db.commit()
    return new, skipped, run_id

def stats(db):
    r = db.execute("SELECT COUNT(*) n, MIN(first_seen_utc) f, MAX(last_seen_utc) l FROM papers").fetchone()
    runs = db.execute("SELECT run_id,started_utc,n_fetched,n_new,n_skipped FROM runs ORDER BY run_id").fetchall()
    return dict(r), [dict(x) for x in runs]

if __name__ == '__main__':
    DB = sys.argv[1] if len(sys.argv) > 1 else 'scan_ledger.db'
    rows = json.load(open('../ojcs_all.json'))
    recs = [{'id': r['id'], 'doi': r['doi'] or None, 'title': r['title'], 'year': r['year'],
             'date': r['date'], 'cites': r['cites'], 'cluster': r.get('cluster')} for r in rows]
    db = connect(DB)
    new, skipped, run = ingest(db, recs, '2644-1268')
    print(f"run {run}: fetched={len(recs)} new={len(new)} skipped={skipped}")
    new2, skipped2, run2 = ingest(db, recs, '2644-1268')
    print(f"run {run2}: fetched={len(recs)} new={len(new2)} skipped={skipped2}   <- dedup proof")
    s, runs = stats(db)
    print("ledger:", s)
