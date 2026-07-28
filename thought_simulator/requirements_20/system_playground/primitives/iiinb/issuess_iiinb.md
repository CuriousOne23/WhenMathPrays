# ⭐ The Architectural Problems in IIInB (Clear, Precise, Actionable)

## 1. **No single source of truth for the evolving text**
### What the spec expects
- **surface** = the *original* input string, never mutated  
- **normalized** = the *working buffer* that every repair stage updates

### What your implementation does
- Sometimes edits `surface`
- Sometimes edits `normalized`
- Sometimes checks conditions against `surface` even after it has been mutated

### Why this breaks everything
The testbench’s gating logic depends on **surface being immutable**.

Example:  
Case normalization must fire **only** if the *original* input started with `"the "`.

But when spelling repair mutates `surface` from `"hte dog"` → `"the dog"`,  
case normalization fires incorrectly.

This is why misspelling.transposition originally failed.

---

## 2. **Stage ordering is not enforced**
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

Your iiinb.py has these stages **interleaved**, sometimes nested, sometimes skipped.

### Why this breaks everything
Repairs must happen **before** anomalies.  
Whitespace normalization must happen **after** punctuation cleaning.  
Case normalization must happen **after** spelling repairs.  
Token preservation must happen **after** case normalization.

When the order is wrong, tests fail even if each individual rule is correct.

Example:  
In your current output:

```
Normalized: 'hte dog chased the cat'
```

This proves spelling repair never ran — not because the rule is wrong,  
but because the rule is in the wrong place in the pipeline.

---

## 3. **The wrapper and primitive disagree about what “surface” means**
The ThoughtPacket provides:

- `tp.surface` — the original input  
- `tp.raw_input` — sometimes empty, sometimes preprocessed  
- `tp.tokens` — original tokens

Your wrapper has changed multiple times:

- sometimes using `raw_input`
- sometimes using `surface`
- sometimes falling back from one to the other

### Why this breaks everything
The testbench always expects:

```
iiinb_inspect(surface=tp.surface, tokens=tp.tokens)
```

When the wrapper passes the wrong field:

- spelling repairs don’t fire  
- case normalization fires incorrectly  
- token preservation fails  
- structural anomaly locations shift  
- punctuation cleaning triggers in the wrong order

This is why your debug output showed:

```
surface: 'hte dog chased the cat'
normalized: 'hte dog chased the cat'
```

but spelling repair still didn’t run — because the wrapper passed a different value earlier.

---

## 4. **Tokens are being treated as mutable**
### What the testbench expects
Tokens must remain **exactly the original tokens**, even if normalized changes.

Example:  
Token.preservation expects:

```
normalized = "The dog"
tokens = ["the", "dog"]
```

### What your implementation does
Sometimes re-tokenizes normalized, sometimes mutates tokens.

### Why this breaks everything
Token.preservation fails even when normalized is correct.

---

## 5. **Repairs and anomalies are not recorded in a stable, ordered list**
The testbench compares:

```
repair_operations == expected_repairs
```

Order matters.

Your implementation sometimes:

- appends repairs in the wrong order  
- appends anomalies before repairs  
- appends punctuation before whitespace  
- appends structural before spelling

This causes failures like:

```
expected: [whitespace.normalized, punctuation.cleaned]
got:      [punctuation.cleaned, whitespace.normalized]
```

Even though both repairs are correct.

---

# ⭐ The Architectural Fix (What Must Be Straightened Out)

Here is the clean architecture iiinb.py must follow:

---

## **Term Definitions (Clear and Final)**

### **surface**
- The original input string from the ThoughtPacket.
- **Never mutated.**
- Used only for gating rules (e.g., case normalization).

### **normalized**
- The working buffer.
- Starts as `surface`.
- Every repair stage updates this.
- The final output string.

### **tokens**
- The original tokens from the ThoughtPacket.
- **Never mutated.**
- Returned unchanged.

### **repair_operations**
- Ordered list of repairs applied to `normalized`.

### **anomaly_flags**
- Ordered list of anomalies detected in `normalized`.

---

## **Required Pipeline (Strict Order)**

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

## **Wrapper Requirements**

The wrapper must do exactly:

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

# ⭐ Example (Correct Architecture)

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

# ⭐ Why this architecture matters

Because the testbench is not testing “your implementation.”  
It is testing **this architecture**.

Every failure you’ve seen is because iiinb.py is not yet aligned with this architecture.

Once iiinb.py is rewritten to follow this pipeline, the tests will stop feeling like whack‑a‑mole and start passing cleanly.

---
