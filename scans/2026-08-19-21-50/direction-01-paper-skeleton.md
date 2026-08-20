# Direction 01 — Study Design Template

**Working title:** *Catalog Accretion: Measuring Compounding Reuse in Multi-Agent
Framework Migration Across a Production Microservice Estate*

**Alternate framing:** *An Empirical Study of Agent-Assisted Framework Migration at
Enterprise Scale*

A design template for the empirical study Direction 01 describes. It states the claim,
the measures, and the threat that decides acceptance.

---

## 1. The claim, stated so it can be attacked

> A multi-agent migration system whose agents deposit reusable transformation knowledge
> into a shared catalog exhibits **decreasing marginal cost per service**, whereas
> rule-based transformation tooling exhibits approximately **flat marginal cost**.

Everything below exists to make that sentence falsifiable. If the accretion curve is
flat, or is explained entirely by migration ordering, the study reports that instead —
and remains worth publishing, because nobody has measured it either way.

---

## 2. Why it is publishable

Three literatures are adjacent and none covers this:

1. **LLM code-generation benchmarks** (SWE-bench, HumanEval, Defects4J-style harnesses).
   Isolated tasks, single repositories, no estate-level economics and no cross-task
   knowledge transfer. They measure whether a model can do *one* thing.
2. **Rule-based transformation tooling** (OpenRewrite, Rector, codemods). Real migrations
   at real scale, but with an explicitly per-service cost model: a recipe is authored
   once and applied N times, with no mechanism by which service N+1 becomes cheaper
   because service N was completed.
3. **Empirical software engineering on modernisation.** Case studies of monolith
   decomposition and cloud migration, but predating agentic tooling — the unit of
   analysis is the architecture, not the automation.

**The gap:** no published study of a multi-agent system performing a real
framework-version migration across a production service estate, measured against the
human baseline it replaced.

In the venue scanned here, the corpus contains agentic AI as *position* work
(`Redefining Elderly Care With Agentic AI`), LLMs applied to single bounded tasks
(`LLM-Driven Adaptive Cloud Resource Scheduling`, `Integrating AI and LLMs for Automated
Data Quality Enhancement`), and thin empirical SE (`An Empirical Study on the
Classification of Bug Reports`, `Applicability of Process Mining in Usability Tests`).
An estate-scale empirical study is a clear differentiator rather than an incremental one.

---

## 3. Research questions

| RQ | Question | Primary measure |
|----|----------|-----------------|
| **RQ1** | Does per-service migration cost fall as the catalog accretes? | Human-touch hours vs. migration ordinal |
| **RQ2** | How does agent-assisted migration compare to the pre-agent baseline? | Cycle time, human-touch hours, rework rate |
| **RQ3** | Where does human intervention remain necessary, and does that set shrink? | Intervention taxonomy, frequency per service |
| **RQ4** | Does migration quality hold? | Defect escape rate, post-migration incidents |

RQ1 is the contribution. RQ2 is the credibility. RQ3 is what practitioners cite.
RQ4 is what stops a reviewer rejecting it.

---

## 4. THE CRITICAL THREAT — settle this before collecting anything

**The ordering confound decides acceptance or rejection.**

If services are migrated in roughly easy-to-hard order — which is what any sensible team
does — then a falling cost curve is *fully explained by ordering* and says nothing about
catalog accretion. A competent reviewer raises this immediately, and if the data cannot
answer it, the paper is dead.

Three defences, strongest first:

1. **Complexity-adjusted regression.** Model human-touch hours as a function of migration
   ordinal *and* per-service complexity covariates measured **pre-migration**: lines
   touched, dependency count, transitive framework-module surface, test coverage,
   cyclomatic complexity, deprecated API call sites. If the ordinal coefficient remains
   negative and significant after adjustment, accretion is real.
2. **Catalog reuse rate as a direct mechanism measure.** Ordering confounds *cost*, but
   it does not explain *reuse*. If the fraction of transformations for service *n* that
   already existed in the catalog rises with *n*, that is evidence of accretion
   independent of difficulty. **This is the cleanest available signal — instrument it
   first.**
3. **Natural experiment.** Any service migrated out of difficulty order — a late easy
   one, or an early hard one forced by a release dependency — carries the most
   information. Identify these and report them individually.

> **Practical consequence:** if pre-migration complexity covariates were never captured,
> reconstruct them retrospectively from each pre-migration commit SHA. That is
> recoverable, but do it before writing anything else.

---

## 5. Measures, defined precisely

Ambiguous metrics are a common rejection cause. Define these exactly:

| Measure | Definition | Source |
|---|---|---|
| **Cycle time** | Wall-clock, migration branch first commit → merge to trunk | Version control / CI |
| **Human-touch hours** | Engineer hours actually spent, excluding waiting on CI, review queues and release windows | Time records, or commit-session estimation |
| **Rework rate** | Commits after first "ready for review" ÷ total commits on branch | Version control |
| **Review rounds** | Distinct review request cycles before approval | PR metadata |
| **Catalog reuse rate** | Transformations applied to service *n* already in the catalog before *n* began ÷ total transformations for *n* | Catalog + shared schema |
| **Intervention events** | Each point where an agent halted or produced output requiring human correction | Agent execution logs |
| **Defect escape rate** | Production incidents attributable to the migration within 30 days of deploy | Incident tracker |

**Report cycle time and human-touch hours separately and defend the distinction.**
Wall-clock improvement is partly organisational — fewer handoffs, less queueing — and
will be attacked as such. Human-touch hours isolates the automation and is the number
reviewers trust.

---

## 6. Baseline construction — the honest weak point

A programme with some services migrated before the agent fleet and some after is a
**quasi-experiment, not a randomised trial**. Say so plainly rather than letting a
reviewer discover it.

State explicitly:
- Assignment to condition was by calendar, not randomisation.
- The team learned the migration domain over time, independent of tooling. Some
  improvement is human learning, and **the design cannot fully separate the two.**
- Framework-version targets may differ between groups.

Then mitigate:
- Report the pre-agent group's own ordinal trend. **If it already shows a falling curve,
  that is human learning, and the accretion claim must be restricted to the increment
  above it.** This comparison is the most honest thing in the paper and reviewers respect
  it.
- Use complexity-adjusted comparison, not raw means.
- Consider an interrupted time-series framing rather than two-group comparison.

Do not overclaim causality. "Associated with" survives review; "causes" does not.

---

## 7. The system section — what makes it a method paper

Describe a reusable architecture, not a war story:

- **Agent roles** — responsibilities, boundaries, handoff contract.
- **Tool-mediated access** (e.g. MCP) — why tool mediation rather than direct file
  manipulation, and what it buys in reproducibility and auditability.
- **The shared snapshot schema** — the transferable artefact. Publish it; it is what
  lets others replicate the mechanism on a different stack.
- **Catalog accretion mechanism** — precisely how a completed migration deposits reusable
  knowledge, how the next planner retrieves it, and the match criteria.
- **Explicit contrast with rule-based tooling** — why recipe authoring has flat marginal
  cost and catalog accretion does not. Be fair to the alternative; reviewers use it.

---

## 8. Figures — build these first, they carry the paper

1. **The accretion curve.** Human-touch hours vs. migration ordinal, raw and
   complexity-adjusted, with confidence band. *Headline figure.*
2. **Catalog reuse rate vs. ordinal.** The mechanism figure — cleanest evidence.
3. **Baseline vs. agent-assisted**, complexity-adjusted, with the pre-agent trend shown
   so the reader can see how much is human learning.
4. **Intervention taxonomy over time.** Stacked area — which intervention classes
   disappeared and which never did. Most practitioner-useful figure.
5. **Defect escape rate**, both conditions, with confidence intervals. The
   "speed did not cost quality" figure.

---

## 9. Section plan and target lengths

| § | Section | Words | Notes |
|---|---------|-------|-------|
| 1 | Introduction | 800 | Lead with the estate, not the model. Contributions as a numbered list. |
| 2 | Background & Related Work | 1200 | The three literatures; end on an explicit gap statement. |
| 3 | System Description | 1500 | Architecture, agent roles, shared schema, accretion mechanism. |
| 4 | Study Design | 1200 | RQs, measures, baseline construction, analysis plan. |
| 5 | Results | 1800 | Five figures, RQ by RQ. |
| 6 | Discussion | 900 | What transfers to other stacks; where it will not. |
| 7 | Threats to Validity | 700 | Ordering confound first and prominently. Do not bury it. |
| 8 | Conclusion & Replication | 400 | Link the package. |

~8,500 words — normal length for this venue.

---

## 10. Data extraction checklist

- [ ] Per-service migration ordinal, start and merge timestamps
- [ ] Per-service **pre-migration** complexity covariates at the pre-migration commit SHA
- [ ] Human-touch hours per service, plus the derivation method (state it explicitly)
- [ ] Commit history per migration branch: total, post-review, review rounds
- [ ] Catalog state snapshots: entries present before each service began
- [ ] Per-service transformation list, tagged reused vs. newly authored
- [ ] Agent execution logs: halts, errors, human corrections, with classification context
- [ ] 30-day post-deploy incidents per service, with migration-attribution judgement
- [ ] The same fields, as far as recoverable, for pre-agent baseline services

---

## 11. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| Ordering confound unresolvable | **Critical** | Catalog reuse rate as mechanism evidence (§4.2) |
| Human-touch hours not recorded | **High** | Reconstruct from commit sessions; state method and its error |
| Too few baseline services for power | Medium | Report effect sizes and CIs, not p-values alone |
| Single-organisation study | Medium | Frame as a within-estate longitudinal study; claim no generality |
| Catalog cannot be open-sourced | Medium | Publish schema and synthetic exemplars instead |
| Reads as a tool advertisement | Medium | Report failures and residual interventions prominently |

---

## 12. Immediate next actions

1. **Instrument catalog reuse rate.** It is the mechanism evidence and the strongest
   defence against the ordering confound. Nothing else matters as much.
2. **Recover pre-migration complexity covariates** at each pre-migration commit SHA.
3. **Fix the human-touch-hours derivation method** and apply it uniformly across both
   groups. Inconsistency here invalidates RQ2.
4. **Plot the raw accretion curve.** If it is flat, the study pivots to a negative
   result — still publishable, and far better discovered now than in month three.
