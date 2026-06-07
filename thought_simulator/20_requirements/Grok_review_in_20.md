## Comment on CP’s IIInB / UPI / USP proposal

With InB closed (20.100 v0.2, 20.500 §7.7), this proposal is the right next object for **Track H**. Overall: **accept the architecture** with refinements below — not a new debate about InB.

---

### Verdict

CP’s three-way split is sound:

| Piece | Role | Assessment |
|-------|------|------------|
| **IIInB** | Bounded pre–Pipeline A correction; read-only USP; no learning | **Accept** — correct layer |
| **Clarification** (via CIL) | Ask user when IIInB cannot apply a rule | **Accept** — already aligned with CIL/GB escalation (20.33) |
| **UPI + USP** | Write rules after clarification; IIInB reads snapshots | **Accept** — correct separation of integrate vs store vs apply |
| **GB** | Oversight / veto, not dictionary | **Accept** — matches 20.80 posture |

This fills the gap you identified: **remember clarified meaning and apply it deterministically next time**, without making InB, IB, or IMR do the wrong job.

---

### What CP got especially right

**1. IIInB “correct vs clarify” fork**  
When shorthand/domain rules apply → deterministic transform. When unknown/ambiguous → tag, no guess, escalate to clarification. That preserves 20.17 (`MI_*` tagging) and InB non-inference.

**2. UPI as integrator, not basin**  
Calling UPI a **profile writer** avoids basin sprawl. Good fit with existing `execution_signature` / `policy_signature` binding.

**3. USP as versioned snapshot**  
IIInB should read `usp_snapshot_ref`, not a live mutable store — same replay pattern as `semantic_snapshot_ref` / `commit_id`.

**4. GB not owning USP**  
GB approves/vetoes **commits**; UPI/COB own storage. Prevents GB becoming a rule engine.

---

### Refinements before you spec

**1. Rename “Path B” everywhere**  
Use **clarification path** or **CIL clarification lane**. “Path B” will collide with **Pipeline B** (execution manifold) in every review and fixture.

**2. IIInB: stage vs basin**  
You can get the same behavior with less ontology cost:

- **Option A (CP):** full **IIInB** basin primitive  
- **Option B (lighter):** profiled Pipeline A stage `input_semantic_repair` between InB and RB, documented in 20.30 + one `20.xxx` spec  

Recommend starting **Option B in the spec title** (“Input Semantic Repair stage, alias IIInB”) unless you need basin lifecycle (GB supervisory verbs, TCU basin caps, etc.).

**3. Where USP lives**  
Don’t invent a orphan datastore. Strongest anchor:

- **USP persisted under COB** (20.32) — conversation/user continuity  
- **UPI** = thin writer integrator (new 20.xxx)  
- **CIL** (20.33) = delivers clarification UX/events  
- **GB** = commit gate on new rules  

**4. Topology (proposed)**

```text
External input
  → InB (surface normalize)
  → IIInB (read USP snapshot; apply rules OR emit UNKNOWN_SEGMENT)
  → [if UNKNOWN] CIL clarification → user
  → [on answer] UPI proposes rule → GB approve → USP commit
  → RB → OB → … → Pipeline A
```

IIInB is **optional per profile**; minimal TS skips it and relies on 20.17 tagging + IB-Creation-Request.

**5. Determinism contract (must be normative)**  
For heuristic IIInB (no GPU / no LM):

- Frozen `usp_snapshot_ref` + `policy_signature` + input segment → deterministic output or `UNKNOWN_SEGMENT`
- Append-only `input_correction_record` on every IIInB pass (applied rule id, or escalation reason)
- No same-cycle USP write from IIInB

If you later allow a small model, it’s a **rich profile** with frozen model id + version in `execution_signature` — not minimal conformance.

---

### Answers to CP’s six open questions

| # | Question | Recommendation |
|---|----------|----------------|
| **1** | UPI the right place? | **Yes** as integrator; **USP under COB** for persistence; IIInB read-only |
| **2** | Rule acceptance constraints? | Safety (no `MI_CONTRA` auto-clear), deterministic ordering/priority, max rules per scope, conflict → reject or GB arbitrate, schema-versioned `pattern` + `meaning` |
| **3** | User vs session vs context scope? | **Layered:** session → conversation (COB) → user; lookup order fixed and documented |
| **4** | GB veto vs advisory? | **Veto on commit**; IIInB reads **committed** USP only |
| **5** | Aging / decay / confirm? | **Yes:** `created_at`, `last_used`, optional `expires_at`; session→user promotion requires explicit confirm |
| **6** | IIInB + USP risks? | Rule explosion (cap), cross-user bleed (strict keys), routing contamination (USP affects segments only, not RB/TR tables), false confidence (UNKNOWN must win over weak match) |

---

### Gaps to add in the first spec draft

1. **`UNKNOWN_SEGMENT` schema** — what IIInB emits when it won’t guess (feeds CIL).  
2. **Clarification completion event** — what UPI receives (user_id, conversation_id, pattern, clarified_meaning, scope).  
3. **Interaction with 20.17** — USP resolution must not silently clear `MI_VAGUE` / `MI_CONTRA`; update `messy_input_record` explicitly or leave flags.  
4. **Minimal vs rich profile** — 20.500 §7.7 should state: **minimal conformance omits IIInB+UPI**; honest path = tag + clarify only.  
5. **One-page interface box** before full HLRs — InB, IIInB, CIL, UPI, COB/USP, GB.

---

### What I’d push back on lightly

- **“IIInB performs semantic correction”** — say **“applies committed USP rules and published transforms”**; true open-ended semantic inference stays profile-optional.  
- **Treating clarification as its own subsystem** — it should remain **CIL + GB**, not a parallel “Path B” module.  
- **Requiring IIInB for PoC** — defer; Track H can draft without blocking 40-series dual-pipeline work.

---

### Recommended Track H sequencing

1. **RFC one-pager** — topology + profiles + naming (no HLRs yet)  
2. **`20.xxx` UPI requirements** (thin) + **IIInB / input repair** section (can be one doc initially)  
3. **COB extension note** — USP field schema + `usp_snapshot_ref`  
4. **CIL extension note** — clarification request/response wire format  
5. **20.36 Class 0 fixture** (optional) — IIInB apply rule → same input twice → identical normalized segment  

---

### Bottom line

**Endorse CP’s proposal** as the Track H design direction: IIInB (apply, don’t learn) + CIL clarification + UPI (write) + USP/COB (store) + GB (veto).  

Refine: fix naming, prefer stage-or-thin-basin, anchor USP in COB, nail determinism/replay, declare minimal profile = off.  

If you want the next executable step, I can draft a **one-page Track H RFC** or a **minimal `20.xxx` skeleton** (Purpose, Non-Goals, interface box, HLR placeholders only) for CP review.