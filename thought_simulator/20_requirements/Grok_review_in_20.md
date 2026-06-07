## Comment on the proposed 20.45 Purpose rewrite

The rewrite is **directionally good** for primitive focus: it says what IMR is for, where it sits (post–Pipeline B), and that it **does not** perform semantic correction itself. That helps amid IIInB, UPI, InB, IB, etc.

A few issues to fix before paste, plus a merged version below.

---

### What works

| Element | Why it helps |
|--------|----------------|
| **Detect and classify mismatches** | Matches taxonomy (HLR-001–003) |
| **Pipeline B realization context** | Correct layer — not input repair |
| **Type B → bounded `CorrectionTrigger`** | Aligns with HLR-007–010, 029–030 |
| **No direct `semantic_core` writes** | Matches HLR-008 and 20.12 |
| **“Supervisory governor”** | Signals IMR schedules/audits; Pipeline A executes |

This is stronger than the current Purpose, which only says “Pipeline B feedback into Pipeline A” and “first pre-PoC hardening module” — weak for onboarding.

---

### What to adjust

**1. Type A and Type C are missing from Purpose**  
The draft is almost entirely Type B. IMR is a **three-type** classifier; Purpose should mention all three in one sentence each, or readers assume IMR = semantic re-interpretation only.

**2. “User intent” is slightly loose**  
Normatively IMR works on **`evaluator_signal` + `semantic_snapshot_ref` + `oub_artifact_ref`** (HLR-002), not inferred intent. Prefer **“evaluator-indicated mismatch”** or **“committed meaning vs realized output.”**

**3. “Cognitive interpretation errors, projection errors”**  
Fine as prose, but tie to taxonomy: Type A = expression/register; Type B = semantic/factual; Type C = safety/policy.

**4. Tension with your v0 posture (if still active)**  
If Jeff still wants **no mandated A→B→A feedback loop** in minimal conformance, this Purpose **foregrounds Type B** as core mission (“supervisory governor for interpretation **correction**”). That’s accurate for **current 20.45 HLRs**, but it fights a **product** decision to demote Type B to an extension profile.

**Pick one:**

- **Keep Type B in Purpose** (matches existing HLRs) — document v0/minimal as a **profile** elsewhere.  
- **v0 monitor-only** — Purpose should lead with **detect/classify/log**; Type B as **optional extension** (would need HLR/profile edits later, not Purpose alone).

**5. Add explicit “what IMR is not”** (one line)  
With Track H open, Purpose should point away from input correction:

> IMR does **not** perform pre–Pipeline A input error correction (see 20.500 §7.7, IIInB/UPI).

**6. Keep the 20.12 / HLR-20.012-009 hook**  
The current Purpose cites parent invariant satisfaction — worth retaining in one line.

---

### “Supervisory governor” — acceptable with nuance

The phrase fits if you mean: **classify, cap, dedupe, queue triggers, audit** — not **run** Pipeline A or **fix** meaning.  

Avoid implying IMR is GB or a closed feedback controller. **“Mismatch evaluator and trigger scheduler”** is more precise; “governor” is OK if paired with “does not mutate `semantic_core`.”

---

### Recommended Purpose (merge CP draft + fixes)

Use this instead of paste-as-is — same style, fuller primitive boundary:

```markdown
## Purpose

The **Interpretation Mismatch Routine (IMR)** detects and classifies mismatches between **committed `semantic_core`**, **Pipeline B realization** (`exec_plan`, `oub_artifact_ref`), and **evaluator signals** after expression. IMR is a Pipeline B post-realization evaluator: it SHALL NOT perform semantic or input correction itself.

IMR classifies every evaluated mismatch into **Type A** (expression/register), **Type B** (semantic/factual/logical), or **Type C** (safety/policy) per the taxonomy below. Type A MAY schedule realization-only retry on the same `semantic_snapshot_ref`. Type C SHALL route through GB per safety policy. When a mismatch is semantic (Type B), IMR MAY emit a bounded `CorrectionTrigger` that schedules a **limited** Pipeline A re-interpretation of explicitly listed TP/MTP fields in a **subsequent** cycle; all semantic updates occur only through approved Pipeline A pathways (HLR-20.045-008).

IMR therefore serves as the **mismatch evaluator and trigger scheduler** for post-output feedback: it records when realization diverges from committed meaning or evaluator expectations, enforces caps and cooldowns, and queues safe correction pathways without violating [20.12](20.12_ts_invariants.md) (HLR-20.012-009).

**Out of scope:** pre–Pipeline A input error correction ([20.100](20.100_inb_requirements.md), [20.500](20.500_refactoring_for_dual_TS_pipeline.md) §7.7 IIInB/UPI); inquiry or ambiguity handling ([20.90](20.90_ib_requirements.md) IB).
```

---

### Verdict

| Question | Answer |
|----------|--------|
| Paste CP’s rewrite as-is? | **Almost** — add Types A/C, tighten “user intent,” add out-of-scope line, keep 20.12 ref |
| Good for primitive focus? | **Yes** — especially with IIInB/UPI/InB boundaries explicit |
| Enough alone if v0 = IMR monitor-only? | **No** — Purpose must match profile decision; may need a **Conformance profiles** note under Purpose |

**Process:** Purpose-only change is **low risk** if it doesn’t weaken HLRs. Bump 20.45 to v0.3 with changelog: “Purpose clarify — primitive boundary vs input correction (Track H align).”

I can apply the merged Purpose to `20.45_imr_requirements.md` if you and CP approve the wording above (and confirm whether Type B stays **normative** or moves to **extension** in the same edit).