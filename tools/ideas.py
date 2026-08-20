# Each direction stands on the corpus alone. The fourth panel is "Why it is under-attempted"
# — the structural barrier that explains why the gap has persisted.
IDEAS = [
{
 "id":"migrate",
 "tag":"Highest novelty",
 "kicker":"Empirical software engineering",
 "title":"Agentic code migration has no empirical baseline",
 "thesis":"The literature measures LLM coding on isolated benchmark tasks. No published study follows a multi-agent system through a real framework-version migration across a production service estate.",
 "gap":"This journal publishes agentic AI as <em>position and opportunity</em> work &mdash; <b>Redefining Elderly Care With Agentic AI</b> is a challenges-and-opportunities piece &mdash; and applies LLMs to single bounded tasks in <b>LLM-Driven Adaptive Cloud Resource Scheduling</b> and <b>Integrating AI and LLMs for Automated Data Quality Enhancement</b>. Its empirical software-engineering work is thinner: <b>An Empirical Study on the Classification of Bug Reports</b> is a classifier study, <b>Applicability of Process Mining in Usability Tests</b> a single case study. The wider SE literature is dominated by SWE-bench-style isolated tasks. Nowhere is there an estate-scale migration measured against the human baseline it replaced.",
 "proposal":"An empirical study plus a method contribution. The method is <b>catalog accretion</b>: each migrated service deposits reusable transformation knowledge, so service <i>n</i>&plus;1 costs less than service <i>n</i> &mdash; in contrast to rule-based transformation tooling, whose per-service cost is flat because a recipe is authored once and applied unchanged. The falsifiable claim is a <b>negative slope on the accretion curve</b> after adjusting for service complexity.",
 "experiment":"Instrument a migration programme covering twenty or more services on a common framework-version ladder. Record human-touch hours and catalog reuse rate per service against migration ordinal, with pre-migration complexity covariates captured at each starting commit. Reuse rate is the key measure: migration ordering confounds cost, but it cannot explain why later services draw more heavily on knowledge that already existed.",
 "barrier":"Estate-scale migration data sits inside organisations that do not publish, and the instrumentation must be in place <em>before</em> the migration runs &mdash; retrospective reconstruction of human-touch hours is where most attempts die. The result is a literature that measures what is easy to measure: isolated tasks on public repositories.",
 "effort":"8&ndash;12 weeks with data in hand",
 "venue":"Applied systems work fits the venue; the accretion curve is the figure that sells it."
},
{
 "id":"retrieval",
 "tag":"Two literatures, no overlap",
 "kicker":"Retrieval systems",
 "title":"Metric indexing and vector search are the same problem, published in different rooms",
 "thesis":"A decades-old literature with provable recall guarantees sits beside a new one with none, and the venue is publishing both without either citing the other.",
 "gap":"Three papers here work classical similarity search with real rigour: <b>Gaussian Kernel-Based LSH for High-Dimensional Similarity Search</b>, <b>Include-Slim: Supporting Similarity Retrieval Variants With a Metric Access Method</b>, and <b>A Framework for Predictive Similarity Queries Over Heterogeneous Metric Spaces</b>. Separately, <b>H2-Cache</b> accelerates generative diffusion through hierarchical caching, and <b>SINdex</b> proposes a semantic inconsistency index for detecting hallucination in LLMs. Nobody joins them. The metric-access-method community has spent decades establishing what an index guarantees about recall; the retrieval-augmented generation community ships approximate indexes with tuned-by-vibes parameters and then measures hallucination downstream as if it were purely a model property. Same mathematical object, two vocabularies, no shared evaluation.",
 "proposal":"Establish the missing chain: <b>index recall &rarr; retrieval quality &rarr; generation faithfulness</b>. Define <b>retrieval-induced hallucination</b> &mdash; the share of unfaithful output attributable to the index failing to return a relevant document, rather than to the generator ignoring one it received. That distinction is currently unmeasurable, so every RAG hallucination is blamed on the model. Then bring the metric-access-method guarantees to bear on the operating point: what recall does a deployment actually need, and what does it cost?",
 "experiment":"Fix a corpus and a question set. Sweep an approximate index across its accuracy knob &mdash; HNSW <code>efSearch</code>, IVF <code>nprobe</code> &mdash; to trace measured recall@k from roughly 0.5 to 1.0, and at each point measure generation faithfulness. The interesting outcome is the shape: if faithfulness collapses sharply within a narrow recall band, that band is an operating-point finding every RAG deployment needs and nobody has published.",
 "barrier":"The two communities publish in different venues, use different names for the same structure, and neither owns the whole pipeline &mdash; database researchers do not run generators, and NLP researchers treat the index as a black box they did not build. Faithfulness evaluation is also expensive and contested, so the end-to-end experiment is nobody\u2019s natural next paper.",
 "effort":"10&ndash;14 weeks",
 "venue":"The venue already publishes both halves, which makes it an unusually receptive home for the bridge."
},
{
 "id":"forecast",
 "tag":"Strongest methodological claim",
 "kicker":"Causal inference meets retail",
 "title":"Sales forecasting papers treat promotions as weather. They are decisions.",
 "thesis":"A forecast that sets the promotion, trained on demand shaped by past promotions, is a feedback loop this entire cluster steps around.",
 "gap":"<b>A Hybrid Temporal Convolutional Network and Transformer Model for Sales Forecasting</b> &mdash; the cluster's most-cited paper &mdash; conditions on holidays, promotions and oil prices as exogenous features and reports MAE, RMSE and wMAPE. <b>Comprehensive Electricity Demand Forecasting</b>, <b>BOL-LPP</b> for day-ahead load price, <b>CryptoMamba-SSM</b> for volatility and <b>Potential Purchaser Prediction with AutoGluon Ensembles</b> all follow the same protocol. But a promotion is <em>chosen in response to the forecast</em>. Train on promo-conditioned history, then deploy the model to set promotions, and the feature is downstream of the prediction &mdash; textbook policy confounding. <b>ECommVis</b>, which visualises advertising outcomes, gets closest without naming the loop.",
 "proposal":"Two contributions that reinforce each other. A <b>policy-aware evaluation protocol</b> that holds out on promotion regimes rather than on time, exposing models that have merely memorised the historical promo policy. And an <b>asymmetric decision-cost metric</b> replacing RMSE, since a stockout and an equal-magnitude markdown are not the same loss &mdash; squared error asserts they are.",
 "experiment":"On a public grocery dataset with promotion flags, compare naive conditioning against a policy-aware estimator under a simulated promo-policy shift, reporting both RMSE and realised decision cost. The expected finding &mdash; that the two rankings disagree &mdash; would invalidate how the cluster currently selects models.",
 "barrier":"The forecasting and causal-inference communities barely read each other. Forecasting reviewers want accuracy tables; causal reviewers want identification assumptions. A paper that needs both is harder to place than one that needs either, which is why the loop stays unaddressed despite being obvious to practitioners.",
 "effort":"10&ndash;14 weeks",
 "venue":"Rebuts the cluster's most-cited paper on methodology rather than accuracy &mdash; a durable contribution."
},
{
 "id":"aiops",
 "tag":"Needs human subjects",
 "kicker":"Reliability engineering",
 "title":"Incident prediction is scored on F1. On-call is scored on whether anyone could act in time.",
 "thesis":"A perfectly accurate prediction that arrives too late, or too vague to act on, is worth nothing &mdash; and no reported metric can reveal that this happened.",
 "gap":"<b>A Multi-Task Neural Framework for Unified Alert Processing and Incident Prediction in Enterprise IT</b> and <b>Cross-Modal Attention Networks for Multi-Modal Anomaly Detection in System Software</b> both predict operational failure from logs and metrics, and both report classification metrics. <b>DRL-Adapt</b> optimises routing convergence on network measures. Only <b>A Physics-Guided Bayesian Neural Network for Sensor Fault Detection in Wind Turbines</b> carries uncertainty at all, and never connects it to an operator decision. Meanwhile <b>Benchmarking Explainable AI Methods for Vision Transformers</b> and <b>Human-in-the-Loop Feature Selection with a Kolmogorov-Arnold Network</b> evaluate interpretability by fidelity proxies rather than by whether a human acted differently. One shared blind spot: no measured decision, no measured clock.",
 "proposal":"A decision-utility benchmark for AIOps built on a quantity the literature has no name for &mdash; <b>actionable lead time</b>: the window in which a prediction is both early enough to intervene and specific enough to indicate what to do. Report it alongside page precision, time-to-mitigate and an explicit alert-fatigue cost, so a model that doubles paging for marginal recall is correctly scored as worse.",
 "experiment":"Replay real incident timelines through published detectors and measure what fraction of correct predictions fall inside the actionable window. Then a small controlled study with practising on-call engineers: identical incidents with and without the prediction, measuring time-to-mitigate rather than diagnostic accuracy.",
 "barrier":"It needs three things that rarely co-occur: real incident timelines, consenting on-call engineers, and ethics approval. Classification metrics need none of those, which is precisely why the literature reports them.",
 "effort":"14&ndash;20 weeks (consent and ethics add time)",
 "venue":"Benchmarks accrue citations from everything they judge &mdash; high ceiling."
},
{
 "id":"energy",
 "tag":"Fastest to a result",
 "kicker":"Systems and efficiency",
 "title":"Joules per adapter: energy attribution across fine-tune, serve, and schedule",
 "thesis":"Four papers each optimise one layer of the GPU stack. Operators pay for all four at once, and nobody measures that.",
 "gap":"<b>LLMs on a Budget</b> profiles power and memory for single-GPU fine-tuning and notes fine-tuning is understudied next to training and inference. <b>Idle Fragmentation-Aware Resource Scheduling for Hyperscale Data Centres</b> attacks stranded capacity, <b>DeCLIP</b> works the Pareto frontier of collaborative inference, and <b>LLM-Driven Adaptive Cloud Resource Scheduling</b> puts a reasoning model in the scheduler. Each optimises in isolation and treats the other layers as fixed. Real deployments run fine-tuning and inference on one contended pool where the binding constraint is an inference SLO &mdash; a regime none of them evaluates. The efficiency cluster reaches for new substrates instead: <b>An Efficient Neural Cell Architecture for Spiking Neural Networks</b> and the <b>NA-STM Spiking U-Net Denoiser</b> chase energy through architecture rather than scheduling.",
 "proposal":"Treat adapter fine-tuning as preemptible background load scheduled against inference SLO headroom, and report one attributable figure end to end: <b>joules per unit of adapter quality</b>. Then chart the frontier &mdash; how much SLO headroom must be surrendered per joule recovered &mdash; which is the curve a platform owner needs in order to price the decision.",
 "experiment":"Co-locate LoRA fine-tuning with a served model across a QPS sweep. Measure SLO violation, energy and adapter quality against naive time-slicing and against dedicated hardware. Small, cheap, and it publishes either way.",
 "barrier":"Cross-layer measurement requires owning the whole stack &mdash; scheduler, serving tier and training job. Academic groups typically rent one slice, and industry teams that own all three rarely publish energy numbers that could be read as a cost disclosure.",
 "effort":"6&ndash;10 weeks",
 "venue":"Lowest-risk on this list. A sensible first paper out of the pipeline."
},
{
 "id":"degrade",
 "tag":"Broadest applicability",
 "kicker":"Robustness and calibration",
 "title":"Multimodal fusion breaks quietly when a sensor dies",
 "thesis":"Every fusion paper here assumes all modalities arrive clean. Deployments lose inputs constantly, and attention-based fusion stays confident as it degrades.",
 "gap":"The fusion cluster is thick and uniformly optimistic. <b>Cross-Modal Attention Networks</b> fuses logs with performance metrics, <b>Near-Miss Detection with Multimodal LLMs</b> pairs video segmentation with a language model, <b>A Multimodal Self-Supervised Learning Framework for Scene Understanding in Autonomous Driving</b> and <b>An Emotion Aware Driving Assistant</b> fuse vehicle sensor streams, and <b>Advancing Autism Spectrum Disorder Diagnosis With Multimodal Data</b> surveys the clinical case. All are evaluated with every modality present and uncorrupted. Deployments do not work that way &mdash; a microphone fails, a shipper drops, a camera degrades in rain. Only <b>A Physics-Guided Bayesian Neural Network for Sensor Fault Detection in Wind Turbines</b> treats sensor failure as first-class, and it is a single-modality detector rather than a fusion model.",
 "proposal":"A modality-degradation benchmark &mdash; dropout, lag, partial corruption, and the hardest case, a modality present but wrong &mdash; plus a fusion head reporting calibrated uncertainty under missing inputs. The headline measure is deliberately not accuracy under degradation but whether <b>confidence falls when evidence is removed</b>, reported as calibration error drift.",
 "experiment":"Take a published tri-modal setup, ablate each modality at inference, and report accuracy alongside expected calibration error. The likely finding &mdash; graceful accuracy degradation alongside calibration collapse &mdash; changes a subfield's evaluation protocol rather than its leaderboard.",
 "barrier":"Degradation has no standard corruption suite for multimodal input, unlike the well-established image-corruption benchmarks. Every author would have to build their own, so nobody does, and papers default to the clean-input protocol they inherited.",
 "effort":"8&ndash;12 weeks",
 "venue":"Retrofits onto a dozen papers in this corpus &mdash; wide citation surface."
},
]
