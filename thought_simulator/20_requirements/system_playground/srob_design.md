SROB (Structural‑Semantic Output Buffer) takes the raw structure that SOB exposes and adds the first layer of meaning‑aware patterning on top of it. Where SOB only says “what the message looks like” (symbols, layout, buckets), SROB is the first OB allowed to say “what this structure is doing linguistically.” Concretely, SROB scans the canonical TP message, conditioned on SOB’s structural signature, and detects shallow structural‑semantic patterns: question vs. instruction vs. assertion, list vs. narrative, code‑like vs. prose‑like, math‑like vs. plain text, definition/description/enumeration forms, and other speech‑act and intent shapes. It then compresses these into a bounded residue slice of pattern flags, intent/act buckets, and domain‑hint bits. This SROB residue becomes the second routing component RB uses—bridging from purely structural SOB to later constraint (CnOB) and semantic (SmOB) reasoning without doing full semantics itself.

Here’s a clean SROB structure, parallel in spirit to what you just did for SOB.

---

### 1. SROB purpose

SROB (Structural‑Semantic Output Buffer) takes:

- **Input:** `TP.msg` + `TP.residue.sob`  
- **Output:** a **bounded pattern residue** capturing *shallow* intent and structural‑semantic shape (not full meaning).

It answers:  
> “Given this structure, what is this message *doing* linguistically?”

---

### 2. SROB top‑level outputs

```yaml
srob_residue = {
  srob_speech_act_class,     # what kind of utterance this is
  srob_intent_shape_flags,   # how the user is trying to act
  srob_content_mode_flags,   # what kind of content this looks like
  srob_pattern_mask,         # structural‑semantic pattern bits
  srob_domain_hint_mask,     # very weak domain hints
}
```

All bounded, all bitfields/buckets.

---

### 3. Speech‑act classification

**Goal:** shallow “how is this being said?” classification.

- **srob_speech_act_class** (3–4 bits, mutually exclusive primary class)  
  - ASSERTION  
  - QUESTION  
  - INSTRUCTION / COMMAND  
  - SUGGESTION / REQUEST  
  - META‑TALK (about the system / about the conversation)  
  - OTHER / MIXED

This uses both SOB structure and lexical cues, but stays shallow.

---

### 4. Intent‑shape flags

**Goal:** “what kind of move is this?” at a coarse level.

- **srob_intent_shape_flags** (bitfield)  
  - HELP_SEEKING  
  - EXPLANATION_REQUEST  
  - REWRITE / EDIT_REQUEST  
  - GENERATION_REQUEST (write, create, draft)  
  - EVALUATION_REQUEST (judge, compare, critique)  
  - CONFIGURATION / SETUP (define rules, modes, constraints)  
  - CLARIFICATION / FOLLOWUP  

Multiple bits can be on; this is not a single class.

---

### 5. Content‑mode flags

**Goal:** “what kind of artifact does this look like?”

- **srob_content_mode_flags** (bitfield)  
  - CODE_LIKE  
  - MATH_LIKE  
  - LIST_LIKE  
  - TABLE_LIKE  
  - SPEC_LIKE / REQUIREMENTS_LIKE  
  - NARRATIVE_LIKE  
  - DIALOGUE_LIKE  

These refine SOB’s structural modes with shallow semantics.

---

### 6. Pattern mask

**Goal:** capture recurring structural‑semantic patterns.

- **srob_pattern_mask** (bitfield)  
  - DEFINITION_PATTERN (“X is Y”, “X means Y”)  
  - ENUMERATION_PATTERN (“first…, second…”)  
  - CONDITIONAL_PATTERN (“if…, then…”)  
  - EXAMPLE_PATTERN (“for example…”, “e.g.…”)  
  - CONTRAST_PATTERN (“however…”, “but…”)  
  - REFERENCE_PATTERN (“as above…”, “see section…”)  

Again: bounded, no deep semantics.

---

### 7. Domain‑hint mask

**Goal:** very weak, non‑binding domain hints.

- **srob_domain_hint_mask** (bitfield)  
  - PROGRAMMING_HINT  
  - MATH_HINT  
  - DOCUMENTATION_HINT  
  - UI/TOOLING_HINT  
  - DATA/FILE_HINT  

These are hints for routing, not commitments.

---

### 8. How SROB relates to SOB

- SOB: “what is the **shape** of this message?”  
- SROB: “given that shape, what **kind of act/pattern** is this?”  

SROB never does full semantics; it just turns structure + shallow lexical cues into:

- speech‑act class  
- intent‑shape flags  
- content‑mode flags  
- pattern mask  
- domain‑hint mask  

All of that becomes the **second residue slice** RB can use for routing.
