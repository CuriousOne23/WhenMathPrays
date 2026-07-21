### cst_core.md  
#### Context Stability Tracker — Core Module White Paper  
#### Thought Simulator — Path‑A Identity Layer

---

## 1. Role of CST‑Core in the CST architecture

**CST‑Core** is the *instantaneous structural stability engine* inside CST.

- **CST‑MS**: long‑horizon merge/split determination over $\ge 10$ turns.   
- **CST‑Core**: per‑turn structural stability metrics and correction signals (drift, ambiguity, collapse, freeze/thaw, register stability, continuity).   
- **CST‑Mux**: merges CST‑Core and CST‑MS outputs into a single CSTSignals stream for COB/CIL.

CST‑Core operates only on **structural fields** of COB’s frozen identity‑layer snapshot and OuBA cues—never on semantic content.   

---

## 2. Structural metadata and counters

CST‑Core reads, per identity layer:

- **Referent map** (token sets, clusters, anchors).  
- **Temporal anchors** (time references, recency).  
- **Discourse anchors** (topic, thread, segment markers).  
- **Field‑importance map** (importance weights per field).  
- **Lineage** (parent/child identity references).  
- **Decay, strength, importance, register, ordering metrics**.   

To support long‑horizon integration and per‑turn decisions, CST‑Core maintains:

- **Total count** of references per context and per field over the last $N$ turns (typically $N = 10$).  
- **Temporal order of references** (time‑ordered sequence of hits).  
- **Frequency over last 10 TS cycles** for:
  - identity references,  
  - referent tokens,  
  - temporal anchors,  
  - discourse anchors,  
  - register cues,  
  - field‑importance hits.

Formally, for a given identity layer $L$ and structural feature $f$ (e.g., a referent token, anchor, or register cue):

- **Total count over window**:
  $$
  C_f^{(L)} = \sum_{k = t-9}^{t} \mathbf{1}\{f \in \text{snapshot}_k(L)\}
  $$
- **Frequency over window**:
  $$
  F_f^{(L)} = \frac{C_f^{(L)}}{10}
  $$
- **Ordered reference history**:
  $$
  H_f^{(L)} = \big( h_{t-9}, h_{t-8}, \dots, h_t \big)
  $$
where $h_k$ encodes presence, strength, or importance of $f$ at turn $k$.

These counters extend to **fields** (e.g., temporal anchors, discourse anchors, register states) as well as contexts, matching the long‑horizon integration requirements.   

---

## 3. Drift detection

CST‑Core computes **drift metrics** for identity, referent, temporal, discourse, lineage, and register structures, aligned with the stability metric set.   

For a structural feature vector $x_t^{(L)}$ at turn $t$ (e.g., referent distribution, anchor positions):

- **Per‑turn drift**:
  $$
  D^{(L)}(t) = d\big(x_t^{(L)}, x_{t-1}^{(L)}\big)
  $$
- **Integrated drift over window**:
  $$
  \bar{D}^{(L)} = \frac{1}{10} \sum_{k = t-9}^{t} D^{(L)}(k)
  $$

Here $d(\cdot,\cdot)$ is a deterministic structural distance (e.g., set difference, ordering distance, or weighted field difference), chosen per metric:

- **identity_drift**: change in overall identity structure.  
- **referent_drift**: change in referent map.  
- **lineage_drift**: change in lineage connections.  
- **register_drift**: change in register state.   

CST‑Core compares $\bar{D}^{(L)}$ against monotonic thresholds:

- If $\bar{D}^{(L)} > \theta_{\text{drift}}^{(L)}$, emit a **drift** signal for layer $L$.   

---

## 4. Oscillation detection

Oscillation is **alternation between structural states** across the integration window.   

For a feature $f$ and layer $L$:

- Define a binary or categorical state sequence:
  $$
  s_k^{(L)} = \text{state of } f \text{ at turn } k,\quad k \in [t-9, t]
  $$
- Oscillation score:
  $$
  O_f^{(L)} = \sum_{k = t-9}^{t-1} \mathbf{1}\{s_k^{(L)} \neq s_{k+1}^{(L)}\}
  $$

If $O_f^{(L)}$ exceeds an oscillation threshold $\theta_{\text{osc}}^{(L)}$, CST‑Core flags **oscillation** for:

- referent oscillation,  
- temporal‑anchor oscillation,  
- discourse‑anchor oscillation,  
- identity‑layer oscillation,  
- register oscillation.   

---

## 5. Collapse detection

Collapse is **long‑term loss of structural coherence**.   

For a stability function $S_f^{(L)}(t)$ (e.g., referent, temporal, discourse, field‑importance, register):

- Stability over window:
  $$
  \bar{S}_f^{(L)} = \frac{1}{10} \sum_{k = t-9}^{t} S_f^{(L)}(k)
  $$
- Collapse score:
  $$
  C_f^{(L)} = 1 - \bar{S}_f^{(L)}
  $$

If $C_f^{(L)} > \theta_{\text{collapse}}^{(L)}$, CST‑Core contributes to:

- **identity_collapse_score**  
- **referent_collapse_score**  
- **lineage_collapse_score**  
- **continuity_collapse_score**  
- **register_collapse_score**   

When collapse scores exceed thresholds, CST‑Core participates in issuing **identity_collapse**, **referent_collapse**, **lineage_collapse**, **continuity_collapse**, and register‑related collapse signals, respecting the deterministic signal ordering.   

---

## 6. Ambiguity and lineage continuity

### 6.1 Ambiguity

Ambiguity metrics quantify **overlap, uncertainty, or instability** in structural mappings:

- **referent_ambiguity**: overlapping or unstable referent assignments.  
- **structural_ambiguity**: instability in field‑importance or ordering.  
- **identity_ambiguity**: uncertainty in identity boundaries.  
- **register_ambiguity**: unstable register cues.   

For a feature $f$:

- Ambiguity score:
  $$
  A_f^{(L)}(t) = \text{ambiguity measure at turn } t
  $$
- Integrated ambiguity:
  $$
  \bar{A}_f^{(L)} = \frac{1}{10} \sum_{k = t-9}^{t} A_f^{(L)}(k)
  $$

If $\bar{A}_f^{(L)} > \theta_{\text{amb}}^{(L)}$, CST‑Core emits **ambiguity** signals and adjusts drift/collapse decisions accordingly.   

### 6.2 Lineage continuity

Lineage continuity measures whether identity objects maintain consistent parent/child relationships over time:

- **lineage_continuity**: stability of lineage graph.  
- **identity_continuity**: continuity of identity presence and structure.   

For lineage structure $L_t$ at turn $t$:

- Continuity score:
  $$
  K^{(L)}(t) = \text{continuity measure between } L_t \text{ and } L_{t-1}
  $$
- Integrated continuity:
  $$
  \bar{K}^{(L)} = \frac{1}{10} \sum_{k = t-9}^{t} K^{(L)}(k)
  $$

Low $\bar{K}^{(L)}$ contributes to **lineage_drift** and continuity‑related collapse scores.

---

## 7. Freeze and thaw

Freeze/thaw are **control signals** used when collapse or ambiguity threaten continuity.   

### 7.1 When to freeze

CST‑Core participates in freeze decisions when:

- **collapse_score** exceeds **freeze_threshold**:
  $$
  C_{\text{total}}^{(L)} > \theta_{\text{freeze}}^{(L)}
  $$
- **ambiguity** exceeds a critical threshold:
  $$
  \bar{A}_{\text{total}}^{(L)} > \theta_{\text{amb,crit}}^{(L)}
  $$
- **lineage continuity** is at risk:
  $$
  \bar{K}^{(L)} < \theta_{\text{cont}}^{(L)}
  $$

In these cases, CST issues **freeze** signals for affected layers, causing COB to pause structural changes while CST continues metric computation and queues structural signals (split, merge, retire) until thaw.   

### 7.2 When to thaw

Thaw occurs only when:

- Collapse scores fall below recovery thresholds:
  $$
  C_{\text{total}}^{(L)} \le \theta_{\text{recover}}^{(L)}
  $$
- Continuity is restored:
  $$
  \bar{K}^{(L)} \ge \theta_{\text{cont,recover}}^{(L)}
  $$

CST then issues **thaw** signals, allowing COB to resume applying queued structural corrections (split/merge/retire/weaken/strengthen) in a deterministic recovery sequence.   

---

## 8. Register and field‑importance stability

CST‑Core extends the stability metric set to **register** and **field‑importance**:

- **register_drift**, **register_ambiguity**, **register_continuity**, **register_collapse_score**.   
- **strength_stability**, **importance_stability**, **decay_progress**.   

For register state $R_t^{(L)}$:

- Register stability:
  $$
  S_{\text{reg}}^{(L)}(t) = \text{stability of } R_t^{(L)}
  $$
- Integrated register stability:
  $$
  \bar{S}_{\text{reg}}^{(L)} = \frac{1}{10} \sum_{k = t-9}^{t} S_{\text{reg}}^{(L)}(k)
  $$

CST‑Core issues **strengthen_register** or **weaken_register** when $\bar{S}_{\text{reg}}^{(L)}$ crosses deterministic thresholds, supporting continuity and preventing register collapse.   

Similarly, field‑importance stability $S_f(t)$ guides **weaken/strengthen** signals for identity layers when long‑term relevance or irrelevance is detected.   

---

## 9. Determinism, thresholds, and replay

CST‑Core adheres to the global CST determinism and threshold rules:

- All metrics are **pure functions** of COB snapshot, OuBA cues, previous CST signals, and deterministic metric history.   
- Thresholds are **monotonic, bounded, replay‑safe**, and updated deterministically:
  $$
  \theta_{t+1} = f\big(\theta_t, \text{metric history}\big)
  $$
- No randomness, external state, or wall‑clock time is used.   

CST‑Core’s metrics and signals are logged with full justification and values, enabling deterministic replay of stability behavior across identity‑layer evolution.   

---

## 10. Summary

CST‑Core is the **structural stability engine** of CST:

- It tracks **counts, ordering, and frequency** of contexts and fields over the last 10 TS cycles.  
- It computes **drift, oscillation, collapse, ambiguity, continuity, register and field‑importance stability** using deterministic functions and thresholds.  
- It decides **freeze/thaw** based on collapse and continuity risk, while leaving merge/split determination to CST‑MS and signal aggregation to CST‑Mux.  
