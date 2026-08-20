# Research directions — scan 2026-08-19-21-50

Six directions argued from **172 eligible** papers, citing 32 of them.

A standing filter (`tools/topic_filter.py`) removed **63 of 235** papers before analysis: security (45), privacy (16), fraud (9), governance (4).

---

## 01. Agentic code migration has no empirical baseline

**Empirical software engineering** · _Highest novelty_ · Effort: 8&ndash;12 weeks with data in hand

> The literature measures LLM coding on isolated benchmark tasks. No published study follows a multi-agent system through a real framework-version migration across a production service estate.

**The gap.** This journal publishes agentic AI as position and opportunity work — Redefining Elderly Care With Agentic AI is a challenges-and-opportunities piece — and applies LLMs to single bounded tasks in LLM-Driven Adaptive Cloud Resource Scheduling and Integrating AI and LLMs for Automated Data Quality Enhancement. Its empirical software-engineering work is thinner: An Empirical Study on the Classification of Bug Reports is a classifier study, Applicability of Process Mining in Usability Tests a single case study. The wider SE literature is dominated by SWE-bench-style isolated tasks. Nowhere is there an estate-scale migration measured against the human baseline it replaced.

**What to build.** An empirical study plus a method contribution. The method is catalog accretion: each migrated service deposits reusable transformation knowledge, so service n+1 costs less than service n — in contrast to rule-based transformation tooling, whose per-service cost is flat because a recipe is authored once and applied unchanged. The falsifiable claim is a negative slope on the accretion curve after adjusting for service complexity.

**First experiment.** Instrument a migration programme covering twenty or more services on a common framework-version ladder. Record human-touch hours and catalog reuse rate per service against migration ordinal, with pre-migration complexity covariates captured at each starting commit. Reuse rate is the key measure: migration ordering confounds cost, but it cannot explain why later services draw more heavily on knowledge that already existed.

**Why it is under-attempted.** Estate-scale migration data sits inside organisations that do not publish, and the instrumentation must be in place before the migration runs — retrospective reconstruction of human-touch hours is where most attempts die. The result is a literature that measures what is easy to measure: isolated tasks on public repositories.

**Venue read.** Applied systems work fits the venue; the accretion curve is the figure that sells it.

**Built on:**

- [An Empirical Study on the Classification of Bug Reports With Machine Learning](https://doi.org/10.1109/ojcs.2026.3692087) — 2026, 0 citations, _Software Engineering & AIOps_
- [Redefining Elderly Care With Agentic AI: Challenges and Opportunities](https://doi.org/10.1109/ojcs.2026.3650842) — 2026, 14 citations, _Agentic AI & LLM Systems_
- [LLM-Driven Adaptive Cloud Resource Scheduling: Bridging Reasoning Intelligence With Optimization Guarantees](https://doi.org/10.1109/ojcs.2026.3667549) — 2026, 3 citations, _Agentic AI & LLM Systems_
- [Integrating AI and Large Language Models for Automated Data Quality Enhancement in Data Integration Systems](https://doi.org/10.1109/ojcs.2026.3666345) — 2026, 2 citations, _Software Engineering & AIOps_
- [Applicability of Process Mining in Usability Tests: A Case Study for Identifying User Mental Models in Geospatial Search Engines](https://doi.org/10.1109/ojcs.2026.3682070) — 2026, 1 citations, _Software Engineering & AIOps_

---

## 02. Metric indexing and vector search are the same problem, published in different rooms

**Retrieval systems** · _Two literatures, no overlap_ · Effort: 10&ndash;14 weeks

> A decades-old literature with provable recall guarantees sits beside a new one with none, and the venue is publishing both without either citing the other.

**The gap.** Three papers here work classical similarity search with real rigour: Gaussian Kernel-Based LSH for High-Dimensional Similarity Search, Include-Slim: Supporting Similarity Retrieval Variants With a Metric Access Method, and A Framework for Predictive Similarity Queries Over Heterogeneous Metric Spaces. Separately, H2-Cache accelerates generative diffusion through hierarchical caching, and SINdex proposes a semantic inconsistency index for detecting hallucination in LLMs. Nobody joins them. The metric-access-method community has spent decades establishing what an index guarantees about recall; the retrieval-augmented generation community ships approximate indexes with tuned-by-vibes parameters and then measures hallucination downstream as if it were purely a model property. Same mathematical object, two vocabularies, no shared evaluation.

**What to build.** Establish the missing chain: index recall → retrieval quality → generation faithfulness. Define retrieval-induced hallucination — the share of unfaithful output attributable to the index failing to return a relevant document, rather than to the generator ignoring one it received. That distinction is currently unmeasurable, so every RAG hallucination is blamed on the model. Then bring the metric-access-method guarantees to bear on the operating point: what recall does a deployment actually need, and what does it cost?

**First experiment.** Fix a corpus and a question set. Sweep an approximate index across its accuracy knob — HNSW efSearch, IVF nprobe — to trace measured recall@k from roughly 0.5 to 1.0, and at each point measure generation faithfulness. The interesting outcome is the shape: if faithfulness collapses sharply within a narrow recall band, that band is an operating-point finding every RAG deployment needs and nobody has published.

**Why it is under-attempted.** The two communities publish in different venues, use different names for the same structure, and neither owns the whole pipeline — database researchers do not run generators, and NLP researchers treat the index as a black box they did not build. Faithfulness evaluation is also expensive and contested, so the end-to-end experiment is nobody’s natural next paper.

**Venue read.** The venue already publishes both halves, which makes it an unusually receptive home for the bridge.

**Built on:**

- [Gaussian Kernel-Based LSH for High-Dimensional Similarity Search](https://doi.org/10.1109/ojcs.2025.3602355) — 2025, 1 citations, _Learning Theory & Optimization_
- [Include-Slim: Supporting Similarity Retrieval Variants With a Metric Access Method](https://doi.org/10.1109/ojcs.2026.3687006) — 2026, 0 citations, _Applied ML & Forecasting_
- [A Framework for Predictive Similarity Queries Over Heterogeneous Metric Spaces](https://doi.org/10.1109/ojcs.2026.3676153) — 2026, 0 citations, _Applied ML & Forecasting_
- [H2-Cache: A Novel Hierarchical Dual-Stage Cache for High-Performance Acceleration of Generative Diffusion Models](https://doi.org/10.1109/ojcs.2025.3639606) — 2025, 0 citations, _Multimodal & Vision_
- [SINdex: S emantic IN consistency Index for Hallucination Detection in LLMs](https://doi.org/10.1109/ojcs.2026.3697236) — 2026, 0 citations, _Software Engineering & AIOps_

---

## 03. Sales forecasting papers treat promotions as weather. They are decisions.

**Causal inference meets retail** · _Strongest methodological claim_ · Effort: 10&ndash;14 weeks

> A forecast that sets the promotion, trained on demand shaped by past promotions, is a feedback loop this entire cluster steps around.

**The gap.** A Hybrid Temporal Convolutional Network and Transformer Model for Sales Forecasting — the cluster's most-cited paper — conditions on holidays, promotions and oil prices as exogenous features and reports MAE, RMSE and wMAPE. Comprehensive Electricity Demand Forecasting, BOL-LPP for day-ahead load price, CryptoMamba-SSM for volatility and Potential Purchaser Prediction with AutoGluon Ensembles all follow the same protocol. But a promotion is chosen in response to the forecast. Train on promo-conditioned history, then deploy the model to set promotions, and the feature is downstream of the prediction — textbook policy confounding. ECommVis, which visualises advertising outcomes, gets closest without naming the loop.

**What to build.** Two contributions that reinforce each other. A policy-aware evaluation protocol that holds out on promotion regimes rather than on time, exposing models that have merely memorised the historical promo policy. And an asymmetric decision-cost metric replacing RMSE, since a stockout and an equal-magnitude markdown are not the same loss — squared error asserts they are.

**First experiment.** On a public grocery dataset with promotion flags, compare naive conditioning against a policy-aware estimator under a simulated promo-policy shift, reporting both RMSE and realised decision cost. The expected finding — that the two rankings disagree — would invalidate how the cluster currently selects models.

**Why it is under-attempted.** The forecasting and causal-inference communities barely read each other. Forecasting reviewers want accuracy tables; causal reviewers want identification assumptions. A paper that needs both is harder to place than one that needs either, which is why the loop stays unaddressed despite being obvious to practitioners.

**Venue read.** Rebuts the cluster's most-cited paper on methodology rather than accuracy — a durable contribution.

**Built on:**

- [A Hybrid Temporal Convolutional Network and Transformer Model for Accurate and Scalable Sales Forecasting](https://doi.org/10.1109/ojcs.2025.3538579) — 2025, 17 citations, _Fraud & Financial Analytics_
- [An Enhanced Deep Learning Approach to Potential Purchaser Prediction: AutoGluon Ensembles for Cross-Industry Profit Maximization](https://doi.org/10.1109/ojcs.2025.3552376) — 2025, 9 citations, _Fraud & Financial Analytics_
- [Comprehensive Electricity Demand Forecasting With a Custom Multi-Dimensional Dataset With Model Analysis and Mobile Visualization](https://doi.org/10.1109/ojcs.2026.3693025) — 2026, 0 citations, _Multimodal & Vision_
- [BOL-LPP: A Bayesian-Optimized LSTM Model for Day-Ahead Load Price Forecasting in the ERCOT Market](https://doi.org/10.1109/ojcs.2025.3580107) — 2025, 6 citations, _Fraud & Financial Analytics_
- [CryptoMamba-SSM: Linear Complexity State Space Models for Cryptocurrency Volatility Prediction](https://doi.org/10.1109/ojcs.2026.3651226) — 2026, 2 citations, _Fraud & Financial Analytics_
- [LaplaceSalesNet: A Neural Laplace-Transformer Framework for Continuous-Time Sales Forecasting](https://doi.org/10.1109/ojcs.2025.3617489) — 2025, 1 citations, _Fraud & Financial Analytics_
- [ECommVis: Supporting E-Commerce Marketplace Advertising Outcomes Through a Visual Analytics System](https://doi.org/10.1109/ojcs.2026.3660917) — 2026, 0 citations, _Multimodal & Vision_

---

## 04. Incident prediction is scored on F1. On-call is scored on whether anyone could act in time.

**Reliability engineering** · _Needs human subjects_ · Effort: 14&ndash;20 weeks (consent and ethics add time)

> A perfectly accurate prediction that arrives too late, or too vague to act on, is worth nothing — and no reported metric can reveal that this happened.

**The gap.** A Multi-Task Neural Framework for Unified Alert Processing and Incident Prediction in Enterprise IT and Cross-Modal Attention Networks for Multi-Modal Anomaly Detection in System Software both predict operational failure from logs and metrics, and both report classification metrics. DRL-Adapt optimises routing convergence on network measures. Only A Physics-Guided Bayesian Neural Network for Sensor Fault Detection in Wind Turbines carries uncertainty at all, and never connects it to an operator decision. Meanwhile Benchmarking Explainable AI Methods for Vision Transformers and Human-in-the-Loop Feature Selection with a Kolmogorov-Arnold Network evaluate interpretability by fidelity proxies rather than by whether a human acted differently. One shared blind spot: no measured decision, no measured clock.

**What to build.** A decision-utility benchmark for AIOps built on a quantity the literature has no name for — actionable lead time: the window in which a prediction is both early enough to intervene and specific enough to indicate what to do. Report it alongside page precision, time-to-mitigate and an explicit alert-fatigue cost, so a model that doubles paging for marginal recall is correctly scored as worse.

**First experiment.** Replay real incident timelines through published detectors and measure what fraction of correct predictions fall inside the actionable window. Then a small controlled study with practising on-call engineers: identical incidents with and without the prediction, measuring time-to-mitigate rather than diagnostic accuracy.

**Why it is under-attempted.** It needs three things that rarely co-occur: real incident timelines, consenting on-call engineers, and ethics approval. Classification metrics need none of those, which is precisely why the literature reports them.

**Venue read.** Benchmarks accrue citations from everything they judge — high ceiling.

**Built on:**

- [A Multi-Task Neural Framework for Unified Alert Processing and Incident Prediction in Enterprise IT Systems](https://doi.org/10.1109/ojcs.2026.3651756) — 2026, 0 citations, _Software Engineering & AIOps_
- [Cross-Modal Attention Networks for Multi-Modal Anomaly Detection in System Software](https://doi.org/10.1109/ojcs.2025.3607975) — 2025, 12 citations, _Software Engineering & AIOps_
- [A Physics-Guided Bayesian Neural Network for Sensor Fault Detection in Wind Turbines](https://doi.org/10.1109/ojcs.2025.3577588) — 2025, 6 citations, _Networks, Cloud & Edge_
- [DRL-Adapt: Deep Reinforcement Learning for Adaptive Routing Convergence Optimization in Large-Scale Networks](https://doi.org/10.1109/ojcs.2026.3687441) — 2026, 4 citations, _Networks, Cloud & Edge_
- [Human-in-the-Loop Feature Selection Using Interpretable Kolmogorov-Arnold Network-Based Double Deep Q-Network](https://doi.org/10.1109/ojcs.2026.3652986) — 2026, 0 citations, _Networks, Cloud & Edge_
- [Benchmarking Explainable AI Methods for Vision Transformer-Based Diabetic Retinopathy Analysis](https://doi.org/10.1109/ojcs.2026.3688710) — 2026, 1 citations, _Health & Biomedical AI_

---

## 05. Joules per adapter: energy attribution across fine-tune, serve, and schedule

**Systems and efficiency** · _Fastest to a result_ · Effort: 6&ndash;10 weeks

> Four papers each optimise one layer of the GPU stack. Operators pay for all four at once, and nobody measures that.

**The gap.** LLMs on a Budget profiles power and memory for single-GPU fine-tuning and notes fine-tuning is understudied next to training and inference. Idle Fragmentation-Aware Resource Scheduling for Hyperscale Data Centres attacks stranded capacity, DeCLIP works the Pareto frontier of collaborative inference, and LLM-Driven Adaptive Cloud Resource Scheduling puts a reasoning model in the scheduler. Each optimises in isolation and treats the other layers as fixed. Real deployments run fine-tuning and inference on one contended pool where the binding constraint is an inference SLO — a regime none of them evaluates. The efficiency cluster reaches for new substrates instead: An Efficient Neural Cell Architecture for Spiking Neural Networks and the NA-STM Spiking U-Net Denoiser chase energy through architecture rather than scheduling.

**What to build.** Treat adapter fine-tuning as preemptible background load scheduled against inference SLO headroom, and report one attributable figure end to end: joules per unit of adapter quality. Then chart the frontier — how much SLO headroom must be surrendered per joule recovered — which is the curve a platform owner needs in order to price the decision.

**First experiment.** Co-locate LoRA fine-tuning with a served model across a QPS sweep. Measure SLO violation, energy and adapter quality against naive time-slicing and against dedicated hardware. Small, cheap, and it publishes either way.

**Why it is under-attempted.** Cross-layer measurement requires owning the whole stack — scheduler, serving tier and training job. Academic groups typically rent one slice, and industry teams that own all three rarely publish energy numbers that could be read as a cost disclosure.

**Venue read.** Lowest-risk on this list. A sensible first paper out of the pipeline.

**Built on:**

- [LLMs on a Budget: System-Level Approaches to Power-Efficient and Scalable Fine-Tuning](https://doi.org/10.1109/ojcs.2025.3580498) — 2025, 10 citations, _Agentic AI & LLM Systems_
- [Idle Fragmentation-Aware Resource Scheduling for Hyperscale Energy-Efficient Cloud Data Centers](https://doi.org/10.1109/ojcs.2026.3699545) — 2026, 0 citations, _Networks, Cloud & Edge_
- [DeCLIP: Pareto-Efficient Collaborative Inference in Decentralized Physical Infrastructure Networks](https://doi.org/10.1109/ojcs.2026.3690486) — 2026, 0 citations, _Networks, Cloud & Edge_
- [LLM-Driven Adaptive Cloud Resource Scheduling: Bridging Reasoning Intelligence With Optimization Guarantees](https://doi.org/10.1109/ojcs.2026.3667549) — 2026, 3 citations, _Agentic AI & LLM Systems_
- [An Efficient Neural Cell Architecture for Spiking Neural Networks](https://doi.org/10.1109/ojcs.2025.3563423) — 2025, 7 citations, _Networks, Cloud & Edge_
- [NA-STM Enhanced Energy-Efficient Custom Spiking U-Net Denoiser for Noise-Robust CIFAR-10 Classification](https://doi.org/10.1109/ojcs.2026.3681673) — 2026, 0 citations, _Learning Theory & Optimization_

---

## 06. Multimodal fusion breaks quietly when a sensor dies

**Robustness and calibration** · _Broadest applicability_ · Effort: 8&ndash;12 weeks

> Every fusion paper here assumes all modalities arrive clean. Deployments lose inputs constantly, and attention-based fusion stays confident as it degrades.

**The gap.** The fusion cluster is thick and uniformly optimistic. Cross-Modal Attention Networks fuses logs with performance metrics, Near-Miss Detection with Multimodal LLMs pairs video segmentation with a language model, A Multimodal Self-Supervised Learning Framework for Scene Understanding in Autonomous Driving and An Emotion Aware Driving Assistant fuse vehicle sensor streams, and Advancing Autism Spectrum Disorder Diagnosis With Multimodal Data surveys the clinical case. All are evaluated with every modality present and uncorrupted. Deployments do not work that way — a microphone fails, a shipper drops, a camera degrades in rain. Only A Physics-Guided Bayesian Neural Network for Sensor Fault Detection in Wind Turbines treats sensor failure as first-class, and it is a single-modality detector rather than a fusion model.

**What to build.** A modality-degradation benchmark — dropout, lag, partial corruption, and the hardest case, a modality present but wrong — plus a fusion head reporting calibrated uncertainty under missing inputs. The headline measure is deliberately not accuracy under degradation but whether confidence falls when evidence is removed, reported as calibration error drift.

**First experiment.** Take a published tri-modal setup, ablate each modality at inference, and report accuracy alongside expected calibration error. The likely finding — graceful accuracy degradation alongside calibration collapse — changes a subfield's evaluation protocol rather than its leaderboard.

**Why it is under-attempted.** Degradation has no standard corruption suite for multimodal input, unlike the well-established image-corruption benchmarks. Every author would have to build their own, so nobody does, and papers default to the clean-input protocol they inherited.

**Venue read.** Retrofits onto a dozen papers in this corpus — wide citation surface.

**Built on:**

- [Cross-Modal Attention Networks for Multi-Modal Anomaly Detection in System Software](https://doi.org/10.1109/ojcs.2025.3607975) — 2025, 12 citations, _Software Engineering & AIOps_
- [Leveraging Deep Learning and Multimodal Large Language Models for Near-Miss Detection Using Crowdsourced Videos](https://doi.org/10.1109/ojcs.2025.3525560) — 2025, 16 citations, _Agentic AI & LLM Systems_
- [A Multimodal Self-Supervised Learning Framework for Scene Understanding in Autonomous Driving Systems](https://doi.org/10.1109/ojcs.2026.3707444) — 2026, 0 citations, _Multimodal & Vision_
- [An Emotion Aware Driving Assistant Using Multimodal Recognition and Regulation](https://doi.org/10.1109/ojcs.2026.3701945) — 2026, 0 citations, _Multimodal & Vision_
- [Advancing Autism Spectrum Disorder Diagnosis With Multimodal Data: A Survey](https://doi.org/10.1109/ojcs.2026.3666102) — 2026, 4 citations, _Health & Biomedical AI_
- [A Physics-Guided Bayesian Neural Network for Sensor Fault Detection in Wind Turbines](https://doi.org/10.1109/ojcs.2025.3577588) — 2025, 6 citations, _Networks, Cloud & Edge_

---

