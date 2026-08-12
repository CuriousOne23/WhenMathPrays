# ⭐ **tp_coordination.md**  
### *The Path‑A Control Loop, Phase Authority, Freeze Semantics, and Deterministic Coordination*

---

## **1. Purpose**

This document defines the **Path‑A control loop** — the conductor that coordinates all primitives, freeze points, routing decisions, IdOB cycles, and commit gating.

It specifies:

- the **phase sequence**  
- the **allowed writers** and **allowed readers** per phase  
- the **freeze points**  
- the **routing arbitration rules**  
- the **IdOB cycle rules**  
- the **commit gating rules**  
- the **turn termination contract**

Together with `tp_path_a_map.md` (score) and `tp_state.md` (packet), this document completes the coordination layer of the Thought Pipeline.

---

# **2. Phases of Path‑A**

Path‑A is divided into **five deterministic phases**:

1. **Intake Phase**  
2. **Context Phase**  
3. **Cue Extraction & Routing Phase**  
4. **Identity‑Conditioned Refinement Phase**  
5. **Commit Phase**

Each phase has:

- a fixed set of primitives  
- fixed freeze semantics  
- fixed authority rules  
- fixed routing transitions  

---

# **3. Global Control Loop (Baton Algorithm)**

This is the conductor’s algorithm:

```
phase = Intake

while phase != Commit:
    run next primitive in phase sequence
    primitive reads allowed TP fields
    primitive writes allowed TP fields
    if primitive is a freeze point:
        freeze its field group
    if primitive is RB:
        phase = RB.decide_next_phase(TP)
    else:
        phase = next_phase_in_sequence

run OuBA
freeze committed TP snapshot
hand off to COB/CST/CIL
turn ends
```

Routing (RB) is the **only primitive** that can change the phase.

All other primitives advance deterministically within their movement.

---

# **4. Phase Authority Table**

This table defines **who can write**, **who can read**, **what is frozen**, and **how transitions occur**.

### ⭐ **4.1 Intake Phase (InB → IIInB → IE)**

| Aspect | Authority |
|--------|-----------|
| **Allowed Writers** | InB, IIInB (repair proposals only), **IE** (first commit) |
| **Allowed Readers** | CEx, CE, TPU, OB family, IdOB |
| **Frozen Fields** | Intake envelope, initial meaning shell, initial identity shell |
| **Mutable Fields** | None after IE |
| **Next Phase Decided By** | Deterministic: Context Phase |

---

### ⭐ **4.2 Context Phase (CEx → CE)**

| Aspect | Authority |
|--------|-----------|
| **Allowed Writers** | CEx, **CE** |
| **Allowed Readers** | TPU, OB family, IdOB, RB, TR, DCB |
| **Frozen Fields** | Context Frame, context metadata, clarifying metadata, MSL metadata, CIL lineage metadata |
| **Mutable Fields** | None after CE |
| **Next Phase Decided By** | Deterministic: Cue Extraction & Routing Phase |

---

### ⭐ **4.3 Cue Extraction & Routing Phase (TPU → OB Family → RBU/DCB/TR/RB)**

| Aspect | Authority |
|--------|-----------|
| **Allowed Writers** | **TPU** (meaning corrections), SOB/SROB/CnOB/SmOB/SSG/STPX (residue fields), RBU/DCB/TR/RB (routing metadata) |
| **Allowed Readers** | IdOB, RB, TR, DCB, OuBA |
| **Frozen Fields** | Structural residue, constraint residue, semantic‑adjacent residue, semantic‑layer residue |
| **Mutable Fields** | Meaning fields (TPU only), routing metadata |
| **Next Phase Decided By** | **RB** (routing baton) |

RB chooses:

- **Structural Basin**  
- **Semantic Basin**  
- **Identity Basin**  
- **Correction Basin**  
- **Commit Basin**

---

### ⭐ **4.4 Identity‑Conditioned Refinement Phase (IdOB → MCB → routing loop)**

| Aspect | Authority |
|--------|-----------|
| **Allowed Writers** | **IdOB** (identity core, commitments, freeze signatures, identity continuity flags), **MCB** (next_context) |
| **Allowed Readers** | RB, TR, DCB, OuBA |
| **Frozen Fields** | Identity fields freeze *per cycle* when stable; next_context freezes at MCB |
| **Mutable Fields** | Identity core (IdOB only), next_context (MCB only) |
| **Next Phase Decided By** | **RB** after each IdOB cycle |

RB either:

- sends Path‑A back into another IdOB cycle, or  
- sends Path‑A to Commit Phase.

---

### ⭐ **4.5 Commit Phase (OuBA)**

| Aspect | Authority |
|--------|-----------|
| **Allowed Writers** | **OuBA** (final single writer) |
| **Allowed Readers** | COB, CST‑CORE, CST‑MS, CST‑MUX, CIL |
| **Frozen Fields** | Entire TP packet: meaning core, identity core, commitments, freeze signatures, provenance, next_context |
| **Mutable Fields** | None |
| **Next Phase Decided By** | Turn ends; handoff to COB/CST/CIL |

---

# **5. Routing Arbitration Rules (RB)**

RB is the **baton**.  
It decides the next phase based on:

- Context Frame  
- structural residue  
- constraint residue  
- semantic‑adjacent residue  
- semantic‑layer residue  
- identity continuity flags  
- commitments  
- freeze signatures  
- curvature signals  
- routing vector (TR)  
- next_context metadata  

RB must obey:

- **freeze signatures** (hard constraints)  
- **commit gating rules**  
- **bounded IdOB cycles**  
- **single‑writer invariants**  
- **no backtracking across freeze points**

RB cannot:

- rewrite meaning  
- rewrite identity  
- rewrite context  
- bypass commit gating  
- bypass freeze signatures  

RB can only:

- choose the next basin  
- choose commit eligibility  
- choose IdOB cycles  
- choose correction basin  
- choose structural/semantic basin  

---

# **6. IdOB Cycle Rules**

IdOB cycles continue while:

- identity continuity flags are raised  
- commitments are unresolved  
- freeze‑signature conflicts exist  
- referent/qualifier/subculture/stance/coherence/importance require refinement  
- semantic‑layer cues indicate instability  
- curvature indicates instability  
- RB selects identity basin  

IdOB cycle termination requires:

- identity stability (or stably open)  
- commitments stable or stably carried  
- freeze signatures respected  
- semantic‑layer stability  
- curvature stability  
- RB selecting commit basin  

IdOB is the **only primitive** allowed to modify identity fields.

---

# **7. Commit Gating Rules**

Commit is allowed only when:

- identity continuity flags are cleared or stably carried  
- commitments are stable or stably carried  
- freeze signatures have no conflicts  
- semantic‑layer cues indicate stability  
- curvature signals indicate stability  
- meaning core is stable  
- identity core is stable  
- routing selects commit basin  

Commit gating is enforced by:

- RB  
- TR  
- DCB  
- IdOB  
- OuBA (final check)

Commit gating prevents premature commit and ensures deterministic meaning.

---

# **8. Turn Termination**

A turn ends when:

1. **OuBA freezes the TP packet**  
2. **Committed snapshot** is produced  
3. Snapshot is handed to:  
   - COB  
   - CST‑CORE  
   - CST‑MS  
   - CST‑MUX  
   - CIL  
4. **next_context** is delivered to next turn’s CEx  
5. Next turn begins at InB with:  
   - committed meaning  
   - committed identity  
   - continuity objects  
   - stability signals  
   - next_context  

This is the **cross‑turn contract**.

---

# **9. Deterministic Invariants**

- No primitive may write fields outside its authority.  
- No primitive may rewrite frozen fields.  
- No primitive may bypass routing.  
- No primitive may bypass commit gating.  
- IdOB is the only identity writer.  
- TPU is the only meaning writer before commit.  
- OuBA is the only writer at commit.  
- Freeze signatures override all routing decisions.  
- Commit is the only global freeze.  
- Every turn produces exactly one committed snapshot.  
- Replay determinism: same input → same output.

---

# **End of tp_coordination.md**

---
