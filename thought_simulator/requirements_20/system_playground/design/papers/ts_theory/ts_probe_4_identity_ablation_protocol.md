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
