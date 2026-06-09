## Commentary on Controlled Rename / Identity Migration Architecture

Overall this is a sound direction and aligns with the repo’s post-independence policy. The “address maintenance, not semantic change” framing is correct and matches what `00.00.42`, `30.00`, and `50.05` already imply. Below are refinements and risks worth resolving before implementation.

---

### What works well

**Identity migration as a distinct operation** — Separating rename from re-review is the right call. CI green + inventories synced is sufficient approval for Class A (slug/path) changes.

**30 derives from 10.50** — Correct. Treat 30↔10.50 as one atomic rename unit, not two independent processes.

**Deterministic pipeline with dry-run/apply** — Extending the `align_design_numbering.py` pattern (`--plan` → human sign-off → `--apply`) is proven in this repo.

**Refactor log in `archive/`** — Preserves audit trail without leaving stale names in active canon.

---

### Concerns and refinements

#### 1. Name tables vs. existing inventories — duplication risk

You already have structural inventories:

- `30.01_verification_inventory_index.md`
- `50.00_design_traceability_index.md`
- `40.510_refactor.md`

Introducing parallel JSON name tables creates a **second source of truth** unless you pick one of:

| Option | Tradeoff |
|--------|----------|
| **A.** Name tables are canonical; inventories are **generated** from them | Clean SSOT, but inventories become build artifacts |
| **B.** Inventories stay canonical; name tables are **derived/cache** for the rename script | Less migration pain, tables are tooling-only |
| **C.** Merge — inventories adopt name-table schema in-place | One-time migration cost, clearest long-term |

Without choosing A, B, or C, drift between table and inventory is likely within one or two renames.

**Recommendation:** Option A or C. If tables are SSOT, state explicitly that `30.01` / `50.00` / `40.510` rows are **projections**, not independently edited.

---

#### 2. “No scanning” vs. “no stale references” — internal tension

The plan says the script performs pure mechanical transformation with no scanning, but CI must ensure no stale references outside `archive/`. Those two goals conflict unless you maintain a **complete reference manifest** in the name tables (every file that may cite every identity).

That manifest is effectively a dependency graph. If it’s incomplete, you need scanning (`validate_doc_reference_targets.py`, `rg`) as a safety net anyway.

**Recommendation:** Reframe as:

- **Primary:** deterministic transforms driven by name table + explicit `REPLACEMENT_PAIRS`
- **Verification:** full-repo scan at the end (existing validators), not as the transform engine

“No heuristics during transform” is achievable. “No scanning ever” is not, if you want stale-reference guarantees.

---

#### 3. Bidirectional propagation — scope is too broad as written

The propagation list is correct for **reference updates**, but easy to misread as **peer-tier renames**. Under independence policy:

| Rename in | Must rename peer tier? | Must update references in |
|-----------|------------------------|---------------------------|
| **40** | No | 30, 50, 10.50, 20 (only explicit path cites) |
| **50** | No | 30, 10.50, 40, 20 (explicit cites only) |
| **30 / 10.50** | **Yes — each other** | 50, 40, 20 (explicit cites) |

Also, **steps D and E on every rename** (rewrite governance docs, CI scripts, control-flow docs) is over-scoped. Those should change only when:

- a new tier/band pattern is introduced, or
- a rename touches a **documented example** that uses the old address as normative illustration

For a routine `40.100` → `40.2700` rename, updating `40.510`, module refs, and cross-tier citations should suffice. Rewriting `CONTRIBUTING_CHANGE_WORKFLOW.md` each time adds noise and review cost.

**Recommendation:** Split propagation into:

- **Tier-local mandatory** (inventories, module files, Python in renamed folder)
- **Cross-tier reference sweep** (scan + replace known address strings)
- **Governance/CI touch** (only when the renamed path appears as normative example or hardcoded test fixture)

---

#### 4. Class A vs. Class B renames need explicit policy

The plan bundles filename changes with HLR/LLR ID changes. Those are different risk classes:

| Class | Example | ID fields change? | Re-review? |
|-------|---------|-------------------|------------|
| **A — slug/path** | `50.220_regulator_design_support` → `50.220_regulator_design_spec` | No | No |
| **B — band** | `50.270` → `50.10` | Yes (`LLR-50.270-*` → `LLR-50.10-*`) | No content re-review, but **ID migration approval** required |

Class B needs a broader `REPLACEMENT_PAIRS` list and explicit warning about external/historical LLR consumers. The plan should state that Class B is allowed but heavier, not equivalent to Class A.

---

#### 5. 20-series scope

20 is independent. Propagation to 20 should be **reference-driven only** (files containing the old path string), not “all 20 release files.” The current `20.200_traceability_matrix.md` may list cross-layer paths — that row updates, but `20.102_usp_requirements.md` does not change just because `50.80` renamed unless it explicitly cites `50.80`.

---

#### 6. Python and artifact handling

The plan correctly flags Python. Add explicit rules:

- **Folder rename** → imports must update (blocking)
- **JSON run artifacts** → either rewrite in-place, or freeze old artifacts in `archive/` and stop citing them in active capsules. Don’t leave capsules pointing at paths that no longer exist.
- **`ARTIFACT_NAME` constants** → follow band only if policy says artifact filenames are identity-bearing (your `40.100` harness uses dated artifact names — clarify whether band is embedded)

---

#### 7. Bootstrap problem

You can’t flip to “no hardcoded names” until:

1. Initial name tables are populated from current disk state
2. A one-time audit finds hardcoded names in CI/scripts
3. CI enforces “no new hardcoded canonical paths outside tables” going forward

The first rename is the expensive one. Say that explicitly so expectations are set.

---

#### 8. Token-savings claim — valid with nuance

Token savings are real **if** the AI only reads: name table delta + plan output + validator results. Savings disappear if someone still pastes full diffs or runs exploratory greps. The architecture enables low-token workflow; it doesn’t guarantee it without discipline (run script locally, paste summary only).

---

### Suggested architecture adjustments (summary)

1. **Declare SSOT relationship** between name tables and `30.01` / `50.00` / `40.510`.
2. **Split rename classes** A (path) and B (band + IDs).
3. **Narrow mandatory governance/CI updates** to normative examples and hardcoded fixtures, not every rename.
4. **Keep end-of-pipeline scanning** via existing validators; use tables for transform, not discovery.
5. **Document 30↔10.50 as atomic** — one table entry, one PR, one apply.
6. **20 propagation = explicit citations only**.
7. **Bootstrap phase** as a prerequisite milestone before “no hardcoded names” is enforceable.

---

### Verdict

**Approve the architecture in principle**, with the refinements above. The core insight — centralized identity, mechanical propagation, CI proof, no content re-review — is right for this repo.

The main risk is **over-engineering the propagation surface** (governance/CI rewrites on every rename) and **under-specifying the SSOT relationship** with existing markdown inventories. Nail those two before writing `rename_identity.py`.

Happy to review a revised v2 of this plan or a concrete name-table schema before any implementation.