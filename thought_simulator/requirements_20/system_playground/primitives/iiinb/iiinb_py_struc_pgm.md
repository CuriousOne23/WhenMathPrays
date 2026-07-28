# IIInB Python structured programming guidance (`iiinb.py`)

This document defines the **structured programming blueprint** for `iiinb.py`, implementing the **IIInB primitive** as specified in `20.101_iiinb_prim.md` and tested by `iiinb_testbench.yaml` / `iiinb_testbench.py`.

The goals:

- **Correctness:** faithfully implement the IIInB primitive and all HLRs.  
- **Determinism & replayability:** no randomness, no external services, fully replayable.  
- **Debuggability:** clear control flow, explicit invariants, traceable repair proposals.  
- **Tractability:** small, well‑named functions with narrow responsibilities.  
- **Changeability:** systematic extension via rulesets, not ad‑hoc edits.

---

## 1. Module‑level architecture

**File:** `thought_simulator/requirements_20/system_playground/primitives/iiinb/iiinb.py`

### 1.1 Top‑level responsibilities

- **Input:** `TP.intake.surface`, `TP.intake.tokens` (canonicalized output from InB).  
- **Output:** *repair proposals only* (no applied repairs), e.g. `IE.repair_proposals`.  
- **Scope:** pre‑semantic, deterministic, no global state, no semantic_core access.

### 1.2 Recommended top‑level structure

Order of definitions in `iiinb.py`:

1. **Imports** (standard library only; no network, no randomness).  
2. **Typed data structures**:
   - `Token`, `IntakeView`, `RepairOperation`, `RepairProposal`, `IIInBRulesetContext`.  
3. **Public entrypoint**:
   - `run_iiinb(intake_view: IntakeView) -> RepairProposal`.  
4. **Validation & invariants**:
   - `validate_intake_view(...)`, `assert_pre_semantic_constraints(...)`.  
5. **Rule engine**:
   - `apply_ruleset(...)` orchestrating deterministic shorthand/normalization rules.  
6. **Concrete rule functions**:
   - `rule_expand_deterministic_shorthand(...)`  
   - `rule_normalize_punctuation(...)`  
   - `rule_normalize_casing_unicode(...)`  
   - `rule_fix_repeated_characters(...)`  
7. **Metadata & hashing**:
   - `compute_input_hash(...)`, `build_repair_proposal(...)`.  
8. **Debugging helpers** (optional, testbench‑friendly):
   - `format_repair_operations_for_log(...)`.

---

## 2. Data structures and contracts

### 2.1 Intake view

**Goal:** isolate IIInB from global TP state.

- **Structure:**  
  - `surface: str` — canonicalized surface string.  
  - `tokens: list[Token]` — token sequence from InB.  
- **Constraints:**  
  - Token order preserved.  
  - No semantic annotations.

### 2.2 Repair operations

Each repair operation must be:

- **Deterministic:** same input → same operation list.  
- **Local:** operates on token indices or spans, never on semantics.  
- **Explicit:** includes rule ID and parameters.

Recommended fields:

- `rule_id: str`  
- `span: tuple[int, int]` (token indices)  
- `operation_type: str` (e.g. `"expand_shorthand"`, `"normalize_punctuation"`)  
- `details: dict` (rule‑specific parameters)

### 2.3 Repair proposal

Single object returned by `run_iiinb`:

- `ruleset_id: str`  
- `input_hash: str`  
- `timestamp: str` (ISO, deterministic source—e.g. injected by caller if needed)  
- `operations: list[RepairOperation]`

IIInB **must not** apply repairs; IE consumes this proposal later.

---

## 3. Control flow and function decomposition

### 3.1 Public entrypoint

```python
def run_iiinb(intake_view: IntakeView) -> RepairProposal:
    validate_intake_view(intake_view)
    assert_pre_semantic_constraints(intake_view)

    ruleset_ctx = IIInBRulesetContext.from_intake(intake_view)
    operations = apply_ruleset(ruleset_ctx)

    input_hash = compute_input_hash(intake_view)
    return build_repair_proposal(input_hash, operations, ruleset_ctx)
```

### 3.2 Validation layer

- **`validate_intake_view`**:
  - Ensures structural integrity (non‑empty tokens, consistent indices, etc.).  
  - On failure: raise a deterministic exception (no partial output).

- **`assert_pre_semantic_constraints`**:
  - Confirms no semantic fields are present.  
  - Confirms no access to TP.process, CE, CIL, semantic_core, OB.

### 3.3 Ruleset orchestration

```python
def apply_ruleset(ctx: IIInBRulesetContext) -> list[RepairOperation]:
    operations: list[RepairOperation] = []

    operations.extend(rule_expand_deterministic_shorthand(ctx))
    operations.extend(rule_normalize_punctuation(ctx))
    operations.extend(rule_normalize_casing_unicode(ctx))
    operations.extend(rule_fix_repeated_characters(ctx))

    return operations
```

- **Ordering is explicit and fixed** to preserve determinism.  
- Each rule function:
  - Reads from `ctx` (intake view + config).  
  - Returns a list of `RepairOperation`.  
  - Never mutates global state or applies repairs.

---

## **4. — Deterministic Indexing Rules for RepairOperations**

IIInB must use **token‑based indexing only**, never raw‑character indexing.  
This resolves all prior ambiguity around spaces, `<broken>`, and multi‑correction spans.

### **Indexing Requirements**
- **0‑based indexing** for all token positions.  
- **Spans refer to token indices**, not character offsets.  
- **Spaces are not counted**; they are implicit separators between tokens.  
- **`<broken>` tokens** (invalid Unicode, decoding failures) are represented as:
  - a deterministic token type (e.g., `Token(kind="invalid_unicode", value="�")`)
  - never embedded directly into repair text  
  - never used to compute character offsets  

### **RepairOperation Span Rules**
- `span = (start_token_index, end_token_index)`  
- `start_token_index` inclusive, `end_token_index` exclusive  
- spans must always refer to **existing tokens**  
- spans must never refer to raw character positions  

### **Deterministic Behavior**
Given identical `TP.intake.tokens`, IIInB must produce identical spans and identical repair operations, regardless of:
- whitespace  
- punctuation  
- Unicode replacement characters  
- malformed input sequences  

This guarantees multi‑correction tests behave deterministically and replayably.

---

## *5. — Casing Rules and Sentence‑Initial Behavior**

This section prevents the historical bug where:

> “hte dog chased the cat” → repair incorrectly showed “The dog…”

IIInB must **never** perform semantic casing or sentence‑initial capitalization.

### **Casing Requirements**
- IIInB performs **only deterministic Unicode/casing normalization**, such as:
  - converting full‑width Latin letters to ASCII  
  - normalizing combining marks  
  - normalizing canonical Unicode forms (NFC/NFD)  

- IIInB must **not**:
  - uppercase sentence‑initial tokens  
  - lowercase proper nouns  
  - apply English grammar rules  
  - infer semantics from casing  

### **RepairOperation Behavior**
- If IIInB proposes a spelling correction (e.g., “hte” → “the”), the corrected form must preserve:
  - the deterministic normalized casing  
  - **not** semantic casing  
- IE or later primitives handle capitalization rules.

This ensures IIInB remains strictly pre‑semantic.

---

## **6.— Unicode Normalization and Replacement Character Handling**

This section resolves the YAML test 15 failure:

> “café�” → normalize to “café”

### **Invalid Unicode Handling**
- The Unicode replacement character `�` must be treated as:
  - a deterministic invalid‑codepoint token  
  - never guessed or reconstructed semantically  
  - never embedded directly into surface output  

### **Normalization Requirements**
IIInB must propose deterministic operations such as:

- `remove_invalid_unicode`  
- `normalize_unicode_combining_marks`  
- `normalize_unicode_form` (NFC recommended)  

### **RepairOperation Rules**
- Unicode normalization must be expressed as operations on token spans.  
- IIInB must not emit surface strings directly.  
- IIInB must not drop tokens unless:
  - the token is deterministically invalid  
  - the testbench explicitly requires removal  

### **Deterministic Replayability**
Given identical malformed Unicode input, IIInB must always produce:
- identical invalid‑Unicode tokens  
- identical normalization operations  
- identical repair proposals  

This guarantees YAML test 15 always passes.

---

## 7. Determinism, isolation, and forbidden behavior

### 7.1 Determinism

- No calls to:
  - random number generators  
  - time sources (unless injected deterministically)  
  - external services or environment‑dependent APIs  
- No branching on non‑input state.

### 7.2 Semantic isolation

Forbidden in `iiinb.py`:

- semantic inference  
- intent guessing  
- pronoun resolution  
- ellipsis resolution  
- context‑dependent shorthand expansion

### 7.3 Global state isolation

`iiinb.py` must **not**:

- read or write TP.process, TP.metadata, CE, CIL, semantic_core, OB.  
- depend on mutable global configuration.

---

## 8. Debugging, logging, and testbench alignment

### 8.1 Debug‑friendly design

- Keep rule functions small and pure: input → list of operations.  
- Prefer **explicit assertions** over silent failure.  
- Provide a helper to pretty‑print operations for local debugging.

### 8.2 Testbench alignment

- Ensure `run_iiinb` is the function used by `iiinb_testbench.py`.  
- Keep signatures stable; add new behavior via:
  - new rule functions  
  - extended `details` fields in `RepairOperation`  
  - updated `ruleset_id`

---

## 9. Change management and extension

When IIInB needs to evolve:

- **Add new rules** as new functions; do not overload existing ones.  
- **Update `ruleset_id`** when rule semantics change.  
- Keep this document in sync with:
  - `20.101_iiinb_prim.md`  
  - `iiinb_testbench.yaml` / `iiinb_testbench.py`  
  - `issuess_iiinb.md` (for known pitfalls and invariants)

---
