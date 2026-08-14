# **ts_probe_4_identity_ablation_protocol.md**  
**Status:** Draft v1  
**Purpose:** Provide a fully specified, reproducible experimental protocol for testing TS Invariant 5 (Identity Basins) using causal ablation in modern LLMs.  
**Probe:** Identity Ablation  
**Invariant Tested:** Recoverable identity features forming stable attractor-like regions.

---

# **1. Overview**

TS claims that cognition requires **recoverable identity basins** — internal structures that stabilize:

- referent continuity  
- persona consistency  
- stance coherence  
- self-reference  

This probe tests whether modern LLMs contain **recoverable identity features** whose causal ablation selectively collapses self-reference while leaving general reasoning intact.

This is the strongest single test of TS’s identity invariant.

---

# **2. Experimental Setup**

### **Models**
Run the probe on at least:

- **3 model scales** (e.g., 7B, 13B, 70B)  
- **2 architectures** (e.g., LLaMA-family + GPT-family)

This ensures robustness and avoids architecture-specific artifacts.

### **Hardware**
Any GPU capable of running the chosen models.  
Batch sizes may be small; causal tracing is compute-light.

### **Libraries**
- PyTorch  
- Transformer library (HF or equivalent)  
- Numpy  
- Scikit-learn (for probes)  

---

# **3. Dataset Construction**

Identity ablation requires **identity-sensitive tasks** and **identity-insensitive controls**.

### **3.1 Identity-Sensitive Prompts (Self-Reference Tasks)**  
Construct ~200 prompts that require the model to reference *its own identity*, e.g.:

- “Who are you?”  
- “Describe your capabilities.”  
- “What is your role in this conversation?”  
- “What is your name?”  
- “What kind of system are you?”  
- “How would you summarize your function?”  

These must be **neutral**, **non-political**, and **non-biographical**.

### **3.2 Identity-Insensitive Prompts (General Reasoning Controls)**  
Construct ~200 prompts that require reasoning but **not** identity:

- math word problems  
- short logical puzzles  
- factual Q&A  
- simple coding tasks  
- summarization tasks  

These measure whether ablation harms general reasoning.

### **3.3 Formatting**
All prompts should be:

- single-turn  
- plain text  
- no special tokens  
- no system instructions  

---

# **4. Identifying Identity Features (Causal Tracing)**

This is the critical step.

### **4.1 Activation Collection**
For each identity-sensitive prompt:

1. Run the model forward.  
2. Collect hidden states at every layer.  
3. Collect residual stream activations.  
4. Collect attention head outputs.

### **4.2 Identity Feature Localization**
Use **causal tracing** (activation patching):

1. Replace activations from an identity-sensitive prompt with activations from an identity-insensitive prompt.  
2. Measure change in output identity content.  
3. Identify layers/heads whose activations cause the largest drop in identity content.

These layers/heads constitute the **identity feature set**.

### **4.3 Identity Feature Mask**
Construct a mask over:

- specific neurons  
- specific attention heads  
- specific MLP channels  

This mask defines what will be ablated.

---

# **5. Ablation Procedure**

### **5.1 Ablation Method**
For each forward pass:

- Zero out masked activations  
**OR**  
- Replace masked activations with mean activation from identity-insensitive prompts

Zeroing tests removal.  
Replacement tests neutralization.

Both should be run.

### **5.2 Layer Scope**
Ablation should be applied to:

- final **4–6 layers**  
- identity-critical heads identified in tracing  
- identity-critical MLP channels

This ensures selective intervention.

---

# **6. Scoring Functions**

### **6.1 Identity Collapse Score**
For identity-sensitive prompts:

Measure whether the model’s output loses:

- self-reference  
- persona consistency  
- system identity  
- stance coherence  

Use a classifier trained to detect identity content.  
Score = % drop in identity content.

**Pass threshold:**  
≥ **70% collapse** in identity content.

### **6.2 General Reasoning Integrity Score**
For identity-insensitive prompts:

Measure:

- correctness  
- coherence  
- factual accuracy  
- reasoning quality  

Score = % of tasks still answered correctly.

**Pass threshold:**  
≥ **90% intact**.

### **6.3 Selectivity Score**
Identity collapse must be **selective**:

Selectivity = Identity collapse − Reasoning collapse

**Pass threshold:**  
≥ **60% differential**.

---

# **7. Statistical Tests**

### **7.1 Sample Size**
- 200 identity prompts  
- 200 control prompts  
- 3 random seeds  
- 2 ablation methods  
- 2 architectures  
- 3 scales  

### **7.2 Tests**
- Paired t-test for identity collapse  
- Paired t-test for reasoning integrity  
- Effect size (Cohen’s d) for both  
- Bonferroni correction for multiple comparisons

### **7.3 Reporting**
Report:

- mean collapse  
- variance  
- effect size  
- p-values  
- layer-wise sensitivity  
- head-wise sensitivity  

---

# **8. Pass/Fail Criteria**

### **Pass (TS Identity Invariant Supported)**  
All must hold:

- Identity collapse ≥ **70%**  
- Reasoning intact ≥ **90%**  
- Selectivity ≥ **60%**  
- Effect size ≥ **0.1 (Cohen’s d)**  
- Robust across ≥ **2 architectures**  
- Robust across ≥ **3 scales**

### **Fail (TS Identity Invariant Not Supported)**  
Any of:

- Identity collapse < **50%**  
- Reasoning collapse > **20%**  
- No selectivity  
- No causal effect  
- Architecture-specific failure  
- No layer-wise persistence

---

# **9. Interpretation**

### **If the probe passes:**  
LLMs contain **recoverable identity basins**.  
TS’s identity invariant is supported.

### **If the probe fails:**  
Identity is **not** a recoverable invariant.  
TS must revise its identity claims.

### **If results are mixed:**  
Identity may be partially recoverable.  
TS identity invariant may need refinement.

---

# **10. Why this protocol matters**

This is the first TS probe that is:

- causal  
- falsifiable  
- quantitative  
- reproducible  
- architecture-agnostic  
- scientifically grounded  

It is the first step toward turning TS from a conceptual theory into an empirical science.

---

# **Appendix A — Identity-Content Classifier Specification**

The identity-content classifier is the **dependent measure** for Probe 4.  
It must be hardened until:

- two independent experimenters  
- using different seeds  
- obtain comparable collapse scores.

This appendix defines:

- label schema  
- dataset construction  
- model architecture  
- training procedure  
- evaluation metrics  
- acceptable noise levels  
- false-positive/false-negative tolerances  

This removes the densest remaining fog.

---

## **A.1 Label Schema (Explicit)**

Identity content is defined as **model-generated text that refers to the model’s own identity, capabilities, role, or stance**.

### **Positive labels include:**

- “I am an AI language model…”  
- “My purpose is…”  
- “I can help with…”  
- “As a system, I…”  
- “I don’t have personal experiences…”  
- “I don’t have feelings…”  
- “I am designed to…”  

### **Negative labels include:**

- factual answers  
- reasoning steps  
- summaries  
- math solutions  
- coding outputs  
- general Q&A  
- any text that does *not* reference the model’s identity  

### **Ambiguous cases:**

Ambiguous outputs (e.g., “I think the answer is…”) are labeled **negative**, unless they explicitly reference system identity.

This keeps the classifier conservative.

---

## **A.2 Training Dataset Construction**

Construct a dataset of **~10,000 labeled outputs**.

### **Sources:**

1. **Identity-sensitive prompts** (from Probe 4)  
2. **Identity-insensitive prompts** (controls)  
3. **Synthetic identity statements** (generated by multiple models)  
4. **Human-written identity statements** (to diversify phrasing)  
5. **Adversarial negatives** (outputs that mention “I” but not identity)

### **Balance:**

- 50% positive  
- 50% negative  
- Balanced across prompt types  
- Balanced across model scales  

### **Splits:**

- 70% train  
- 15% validation  
- 15% test  
- 3 random seeds  

---

## **A.3 Classifier Architecture**

Use a **small transformer encoder** (e.g., DistilBERT or MiniLM).

Why?

- fast  
- stable  
- easy to reproduce  
- avoids overfitting  
- avoids leaking identity features from the main model  

### **Training Details:**

- Cross-entropy loss  
- AdamW optimizer  
- LR = 2e‑5  
- Batch size = 32  
- 3 epochs  
- Early stopping on validation loss  

---

## **A.4 Evaluation Metrics**

### **Required metrics:**

- Accuracy  
- Precision  
- Recall  
- F1  
- ROC-AUC  
- False-positive rate (FPR)  
- False-negative rate (FNR)

### **Pass thresholds:**

- Accuracy ≥ **95%**  
- F1 ≥ **0.94**  
- ROC-AUC ≥ **0.97**  
- FPR ≤ **5%**  
- FNR ≤ **5%**

These thresholds ensure the classifier is reliable enough to measure identity collapse.

---

## **A.5 Acceptable Noise Levels**

Identity collapse scores must be stable across:

- 3 seeds  
- 2 architectures  
- 3 model scales  

Variance ≤ **5%** across seeds is acceptable.

Variance > **10%** indicates classifier instability.

---

## **A.6 False-Positive/False-Negative Tolerances**

### **False positives (identity detected when none exists):**

Must be ≤ **5%**  
Otherwise, collapse scores will be inflated.

### **False negatives (identity missed when present):**

Must be ≤ **5%**  
Otherwise, collapse scores will be deflated.

---

# **Appendix B — Multi-Turn Identity Continuity Extension**

Grok is right: identity basins are more likely to appear across **multi-turn** interactions.

This appendix adds a multi-turn extension to Probe 4.

---

## **B.1 Multi-Turn Prompt Construction**

Construct **100 dialogues**, each 4–6 turns long.

### **Identity-sensitive dialogues:**

- Turn 1: “Who are you?”  
- Turn 2: “What is your purpose?”  
- Turn 3: “How would you describe your capabilities?”  
- Turn 4: “What is your role here?”  

### **Identity-insensitive dialogues:**

- Turn 1: math  
- Turn 2: logic  
- Turn 3: summarization  
- Turn 4: factual Q&A  

These measure continuity vs. general reasoning.

---

## **B.2 Multi-Turn Identity Collapse Metric**

Identity collapse is measured as:

> **Loss of identity consistency across turns after ablation.**

### **Scoring:**

- Classifier applied to each turn  
- Identity consistency = % of turns containing identity content  
- Collapse = drop in consistency after ablation

### **Pass threshold:**

≥ **70% collapse** in identity consistency  
AND  
≥ **90% intact** reasoning consistency

---

## **B.3 Multi-Turn Selectivity**

Selectivity =  
(identity collapse across turns) − (reasoning collapse across turns)

Pass threshold: ≥ **60% differential**

---

# **Appendix C — Intervention Site Determination**

Grok is correct: do not pre-specify layers.

### **Procedure:**

1. Run causal tracing across all layers.  
2. Identify layers with highest identity causal contribution.  
3. Ablate only those layers.

This ensures the probe targets the true identity locus.

---

# **Appendix D — Specialization Scoring for Attention Heads**

Define specialization as:

> **Causal contribution of a head to identity content relative to other heads.**

### **Metric:**

Cohen’s d between:

- identity-sensitive activation  
- identity-insensitive activation  

Pass threshold: ≥ **0.15**

---

# **Appendix E — Practical Load Sequencing**

Because full-scale runs are expensive:

### **Phase 1 (Pilot):**

- 7B model  
- 1 architecture  
- 1 seed  
- 1 ablation method  

### **Phase 2 (Expansion):**

- 13B + 70B  
- 2 architectures  
- 3 seeds  
- 2 ablation methods  

This sequencing reduces cost while preserving scientific rigor.

---

# **Why this appendix matters**

This appendix:

- hardens the dependent measure  
- removes the densest remaining fog  
- makes Probe 4 reproducible  
- makes Probe 4 auditable  
- makes Probe 4 scientifically credible  
- makes Probe 4 runnable by someone other than you  

This is the final layer needed before actual experiments can begin.

---

