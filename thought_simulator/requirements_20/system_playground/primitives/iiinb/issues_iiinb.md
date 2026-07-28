# ⭐ Architectural Issues in IIInB  
*(Fully rewritten, all original content preserved)*

IIInB’s current implementation struggles not because individual repair rules are wrong, but because several **architectural invariants** are violated. These invariants are required by the spec and enforced by the testbench. When they are broken, even correct repair logic produces incorrect results.

Below is a precise, actionable breakdown of the architectural problems and the required fixes.

---

# 🚩 1. No Single Source of Truth for the Evolving Text

## What the spec requires
- **surface** = the *original* input string  
  - immutable  
  - used only for gating rules  
- **normalized** = the *working buffer*  
  - every repair stage updates this  
  - final output is `normalized`

## What the current implementation does
- Sometimes edits `surface`
- Sometimes edits `normalized`
- Sometimes checks conditions against `surface` *after* it has been mutated

## Why this breaks everything
The testbench depends on **surface being immutable**.

Example:  
Case normalization must fire **only** if the original input started with `"the "`.

If spelling repair mutates `surface` from `"hte dog"` → `"the dog"`,  
case normalization fires incorrectly.

This is why `misspelling.transposition` originally failed.

---

# 🚩 2. Stage Ordering Is Not Enforced

The testbench implicitly defines a strict pipeline:

1. unicode normalization  
2. structural cleaning  
3. repetition cleaning  
4. shorthand expansion  
5. **spelling repairs**  
6. punctuation cleaning  
7. whitespace normalization  
8. illegal‑character anomaly detection  
9. case normalization  
10. token preservation  

## What the current implementation does
Stages are:
- interleaved  
- nested  
- skipped  
- executed in inconsistent order

## Why this breaks everything
Even correct rules fail when executed in the wrong order:

- Repairs must happen **before** anomalies  
- Whitespace normalization must happen **after** punctuation cleaning  
- Case normalization must happen **after** spelling repairs  
- Token preservation must happen **after** case normalization  

Example:  
If spelling repair is placed too late:

```
Normalized: 'hte dog chased the cat'
```

This proves spelling repair never ran — not because the rule is wrong, but because it is in the wrong place in the pipeline.

---

# 🚩 3. Wrapper and Primitive Disagree About What “surface” Means

ThoughtPacket provides:

- `tp.surface` — original input  
- `tp.raw_input` — sometimes empty, sometimes preprocessed  
- `tp.tokens` — original tokens  

## What the current wrapper does
- sometimes uses `raw_input`
- sometimes uses `surface`
- sometimes falls back between them

## Why this breaks everything
The testbench always expects:

```
iiinb_inspect(surface=tp.surface, tokens=tp.tokens)
```

If the wrapper passes the wrong field:

- spelling repairs don’t fire  
- case normalization fires incorrectly  
- token preservation fails  
- structural anomaly locations shift  
- punctuation cleaning triggers in the wrong order  

This explains debug logs like:

```
surface: 'hte dog chased the cat'
normalized: 'hte dog chased the cat'
```

Spelling repair didn’t run because the wrapper passed a different value earlier.

---

# 🚩 4. Tokens Are Being Treated as Mutable

## What the testbench expects
Tokens must remain **exactly the original tokens**, even if normalized changes.

Example:

```
normalized = "The dog"
tokens = ["the", "dog"]
```

## What the current implementation does
- sometimes re-tokenizes normalized  
- sometimes mutates tokens  

## Why this breaks everything
Token.preservation fails even when normalized is correct.

---

# 🚩 5. Repairs and Anomalies Are Not Recorded in a Stable, Ordered List

The testbench compares:

```
repair_operations == expected_repairs
```

Order matters.

## What the current implementation does
- appends repairs in the wrong order  
- appends anomalies before repairs  
- appends punctuation before whitespace  
- appends structural before spelling  

Example:

```
expected: [whitespace.normalized, punctuation.cleaned]
got:      [punctuation.cleaned, whitespace.normalized]
```

Both repairs are correct — but the order mismatch causes failure.

---

# ⭐ Architectural Fix (What Must Be Straightened Out)

Below is the clean architecture iiinb.py must follow.

---

# 📘 Term Definitions (Clear and Final)

### **surface**
- Original input string  
- **Never mutated**  
- Used only for gating rules (e.g., case normalization)

### **normalized**
- Working buffer  
- Starts as `surface`  
- Every repair stage updates this  
- Final output string

### **tokens**
- Original tokens  
- **Never mutated**  
- Returned unchanged

### **repair_operations**
- Ordered list of repairs applied to `normalized`

### **anomaly_flags**
- Ordered list of anomalies detected in `normalized`

---

# 📘 Required Pipeline (Strict Order)

```
normalized = surface
repair_ops = []
anomaly_flags = []

1. unicode normalization
2. structural cleaning
3. repetition cleaning
4. shorthand expansion
5. spelling repairs
6. punctuation cleaning
7. whitespace normalization
8. illegal-character anomalies
9. case normalization (based on original surface)
10. return original tokens
```

Every stage:

- reads from `normalized`
- writes back to `normalized`
- never touches `surface`
- never touches `tokens`

---

# 📘 Wrapper Requirements

Wrapper must do exactly:

```python
surface = tp.surface
tokens = tp.tokens
result = iiinb_inspect({"surface": surface, "tokens": tokens})
```

No fallback.  
No raw_input.  
No preprocessing.  
No mutation.

---

# 📘 Example (Correct Architecture)

Input:

```
surface = "hte dog chased the cat"
tokens = ["hte", "dog", "chased", "the", "cat"]
```

Pipeline:

1. unicode → no change  
2. structural → no change  
3. repetition → no change  
4. shorthand → no change  
5. spelling → `"hte"` → `"the"`  
6. punctuation → no change  
7. whitespace → no change  
8. anomalies → none  
9. case normalization → surface does NOT start with `"the "` → skip  
10. tokens → unchanged  

Output:

```
normalized = "the dog chased the cat"
tokens = ["hte", "dog", "chased", "the", "cat"]
repair_ops = [{"type": "spelling.transposed", ...}]
anomaly_flags = []
```

This passes.

---

# ⭐ Why This Architecture Matters

The testbench is not testing “your implementation.”  
It is testing **this architecture**.

Every failure you’ve seen is because iiinb.py is not yet aligned with this architecture.

Once iiinb.py is rewritten to follow this pipeline, the tests will stop feeling like whack‑a‑mole and start passing cleanly.

---
