#!/usr/bin/env python3
"""
Standing topic exclusions, applied on every scan.

Excluded papers are NOT deleted — they stay in papers.json and the ledger, tagged with
which filter caught them, so the corpus record remains complete and the filter itself
stays auditable. What they are excluded from is the *candidate pool for research
directions* and the "eligible" counts in the summary.

Edit EXCLUSIONS to change the standing filter. One entry per themed exclusion; each is a
case-insensitive regex matched against title + topics + concepts.
"""
import re

EXCLUSIONS = {
    "security": (
        r"\bsecurit\w*|\bsecure\w*|cyber\w*|\bthreat\w*|\battack\w*|adversar\w*|intrusion|malware|ransomware|"
        r"botnet|phishing|exploit|vulnerab\w*|penetration test|\bsoc\b|forensic|deception|"
        r"authentic\w*|\bpuf\b|encrypt\w*|cryptograph\w*|steganograph\w*|tamper|watermark\w*|"
        r"trust\w* comput|access control|\bzero.trust\b|hardening|antivirus"
    ),
    "privacy": (
        r"\bprivacy\b|privacy-preserving|differential privacy|anonymi[sz]|de-identif|"
        r"homomorphic|zero-knowledge|\bzk-|federated learning|unlearning|\bgdpr\b|\bhipaa\b|consent"
    ),
    "fraud": (
        r"\bfraud\w*|money laundering|\baml\b|\bcbdc\b|card-not-present|chargeback|"
        r"financial crime|counterfeit|sybil|deepfake|forgery"
    ),
    "governance": (
        r"governance|compliance|regulatory|audit\w*|policy-compliant|data steward\w*|"
        r"\bcatalog\w* (quality|decay|governance)|records management|\bsox\b|\bsoc ?2\b|"
        r"ethical and legal|digital rights"
    ),
}

_COMPILED = {k: re.compile(v, re.I) for k, v in EXCLUSIONS.items()}


def excluded_by(paper):
    """Return the sorted list of exclusion names matching this paper (empty if eligible)."""
    # TITLE ONLY, deliberately.
    #
    # OpenAlex `concepts` and `topics` are auto-assigned and noisy: an AIOps paper on log
    # and metric anomalies picks up "Advanced Malware Detection Techniques", and a
    # cryptocurrency forecasting paper picks up security topics from the word "crypto".
    # Matching those fields filtered out reliability and forecasting work that is not
    # security work at all.
    #
    # The trade-off is explicit: a security paper with a neutral title can slip through.
    # That is the better failure mode — and title-only is auditable, since the reason a
    # paper was cut is visible in the paper's own name.
    hay = re.sub(r"<[^>]+>", " ", paper.get("title", ""))
    return sorted(name for name, rx in _COMPILED.items() if rx.search(hay))


def partition(papers):
    """Split into (eligible, filtered); tags each paper in place with `excluded_by`."""
    eligible, filtered = [], []
    for p in papers:
        hits = excluded_by(p)
        p["excluded_by"] = hits
        (filtered if hits else eligible).append(p)
    return eligible, filtered
