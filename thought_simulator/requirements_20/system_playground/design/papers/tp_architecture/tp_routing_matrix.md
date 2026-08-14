# ⭐ **tp_routing_matrix.md**  
### *Routing Inputs, Routing Outputs, Basin Selection Logic, and Commit Gating Matrix*

---

## **1. Purpose**

This document defines the **routing decision matrix** for Path‑A.  
It specifies:

- the **inputs** RB uses  
- the **conditions** that trigger each basin  
- the **outputs** RB produces  
- the **commit gating matrix**  
- the **IdOB cycle matrix**  
- the **routing stability and curvature rules**

This is the deterministic routing substrate that coordinates TPU, OB family, IdOB, and OuBA.

---

# **2. Routing Inputs (RB Read Set)**

RB reads only **frozen or stable fields** from the TP packet.

| Input Group | Source | Freeze Point | Notes |
|-------------|--------|--------------|-------|
| **Context Frame** | CE | CE Freeze | Topic, intent, stance, referents, commitments, importance, identity flags |
| **Structural Residue** | SOB/SROB | OB Freeze | Clause boundaries, anchors, structural importance |
| **Constraint Residue** | CnOB | OB Freeze | Missing slots, constraint conflicts |
| **Semantic‑Adjacent Residue** | SmOB/SSG | OB Freeze | Modality, affect, underspec markers, activation vectors |
| **Semantic‑Layer Residue** | STPX | OB Freeze | Semantic-layer hash, frame markers |
| **Identity Continuity Flags** | IdOB | Per-cycle freeze | Raised/cleared per IdOB cycle |
| **Commitments** | IdOB/Context | Commit Freeze | Open, stable, stably carried |
| **Freeze Signatures** | Identity Layer | Commit Freeze | Hard constraints |
| **Curvature Signals** | DCB | Per-cycle | Instability, drift, routing escalation |
| **Routing Vector (TP.TR)** | TR | Per-cycle | Basin scoring vector |
| **Next Context Metadata** | MCB | Per-cycle | Qualifiers, stance, direction, coherence |

RB does **not** read:

- meaning fields directly  
- identity core directly  
- TPU correction metadata  
- intake envelope  
- scoring metadata (ISc)  

RB only reads **routing-relevant signals**.

---

# **3. Basin Selection Matrix**

RB selects one of **five basins**:

1. **Structural Basin**  
2. **Semantic Basin**  
3. **Correction Basin**  
4. **Identity Basin**  
5. **Commit Basin**

Below is the deterministic matrix.

---

## ⭐ **3.1 Structural Basin Selection**

| Condition | Required Signals | Notes |
|-----------|------------------|-------|
| Structural instability | High structural importance, clause boundary conflict | SOB/SROB |
| Structural ambiguity | Multiple structural parses | SOB/SROB |
| Structural drift | Curvature structural component | DCB |
| Structural underspecification | Missing anchors | SOB |

**Routing Output:**  
→ Run structural refinement primitives (SOB → SROB → CnOB → SmOB → SSG → STPX)

---

## ⭐ **3.2 Semantic Basin Selection**

| Condition | Required Signals | Notes |
|-----------|------------------|-------|
| Semantic instability | Semantic-layer hash conflict | STPX |
| Semantic drift | Curvature semantic component | DCB |
| Semantic underspecification | Underspec markers | SmOB |
| Semantic adjacency conflict | Activation vectors unstable | SSG |

**Routing Output:**  
→ Run semantic refinement primitives (SmOB → SSG → STPX)

---

## ⭐ **3.3 Correction Basin Selection (TPU)**

| Condition | Required Signals | Notes |
|-----------|------------------|-------|
| Meaning conflict | ISc score_conflict | ISc |
| Meaning underspecification | Missing semantic roles | CnOB |
| Meaning correction required | TPU correction eligibility | TPU |
| Constraint violation | Constraint residue conflict | CnOB |

**Routing Output:**  
→ Run TPU (meaning corrections)

---

## ⭐ **3.4 Identity Basin Selection (IdOB)**

| Condition | Required Signals | Notes |
|-----------|------------------|-------|
| Identity continuity flags raised | identity_continuity_flags = true | IdOB |
| Referent instability | referent lineage conflict | IdOB |
| Qualifier instability | qualifier lineage conflict | IdOB |
| Subculture shift | subculture continuity conflict | IdOB |
| Stance/direction/coherence shift | stance/direction/coherence conflict | IdOB |
| Semantic‑importance drift | importance drift | IdOB |
| Freeze‑signature conflict | freeze_signature conflict | Identity Layer |
| Commitment instability | open commitments unresolved | IdOB |

**Routing Output:**  
→ Run IdOB cycle  
→ Then run MCB  
→ Then return to routing

---

## ⭐ **3.5 Commit Basin Selection (OuBA)**

Commit basin is selected only when **all gating conditions are satisfied**.

| Condition | Required Signals | Notes |
|-----------|------------------|-------|
| Identity stable or stably open | identity_continuity_flags cleared or stably carried | IdOB |
| Commitments stable | commitment_set stable | IdOB |
| Freeze signatures respected | no freeze conflicts | Identity Layer |
| Semantic-layer stable | semantic_layer_hash stable | STPX |
| Curvature stable | no instability flags | DCB |
| Meaning stable | TPU corrections complete | TPU |
| Routing vector commit-eligible | TP.TR indicates commit | TR |

**Routing Output:**  
→ Run OuBA (final commit)

---

# **4. IdOB Cycle Matrix**

RB decides whether IdOB must run again.

| Condition | RB Decision | Notes |
|-----------|-------------|-------|
| identity_continuity_flags raised | Run IdOB again | Identity not stable |
| freeze_signature conflict | Run IdOB again | Hard constraint |
| commitments unresolved | Run IdOB again | Must stabilize or carry |
| semantic-layer instability | Run IdOB again | Semantic drift |
| curvature instability | Run IdOB again | Drift detected |
| referent/qualifier/subculture/stance/coherence unstable | Run IdOB again | Identity drift |
| all stable | Proceed to commit basin | Commit gating satisfied |

IdOB cycles are **bounded** by:

- freeze signatures  
- curvature  
- commit gating  
- resource limits (20-series spec)

---

# **5. Commit Gating Matrix**

Commit is allowed only when **all** conditions are satisfied.

| Gating Condition | Source | Must Be |
|------------------|--------|---------|
| Identity continuity | IdOB | Cleared or stably carried |
| Commitments | IdOB | Stable or stably carried |
| Freeze signatures | Identity Layer | No conflicts |
| Semantic-layer stability | STPX | Stable |
| Curvature stability | DCB | Stable |
| Meaning stability | TPU | Stable |
| Routing vector | TR | Commit-eligible |

If **any** gating condition fails → RB selects **Identity Basin**.

If **all** gating conditions pass → RB selects **Commit Basin**.

---

# **6. Routing Stability & Curvature Rules**

Curvature (DCB) is the **instability detector**.

| Curvature Signal | Routing Effect |
|------------------|----------------|
| Structural instability | Structural Basin |
| Semantic instability | Semantic Basin |
| Identity instability | Identity Basin |
| Meaning instability | Correction Basin |
| Global instability | IdOB Basin (identity stabilization) |
| No instability | Commit Basin (if gating satisfied) |

Curvature ensures:

- bounded cycles  
- no infinite routing loops  
- deterministic commit eligibility  

---

# **7. Routing Outputs (RB Write Set)**

RB writes:

- `routing_metadata`  
- `routing_decision` (basin)  
- `routing_reason`  
- `routing_trace`  
- `routing_cycle_count`  
- `routing_commit_flag`  

RB never writes:

- meaning  
- identity  
- context  
- commitments  
- freeze signatures  

RB is **pure control logic**.

---

# **8. Deterministic Routing Invariants**

- Routing decisions are deterministic functions of frozen fields.  
- RB cannot rewrite frozen fields.  
- RB cannot bypass commit gating.  
- RB cannot bypass freeze signatures.  
- RB cannot force commit when gating fails.  
- RB cannot force IdOB termination when identity is unstable.  
- RB cannot force TPU when meaning is stable.  
- RB cannot force OB family when cues are stable.  
- RB must terminate in commit basin.

---

# **End of tp_routing_matrix.md**

---
