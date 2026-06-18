## 1. SOB-First Processing

All TPs enter the system through the **Structured Output Buffer (SOB)**. The SOB gate is the mandatory first stage — no TP bypasses it.

**Rationale:**
- Enforces a canonical entry point, making packet provenance traceable.
- Normalizes TP structure before downstream routing decisions are made.
- Prevents malformed or partially-initialized TPs from polluting the OB address space.

**Procedure:**
1. TP arrives at SOB intake.
2. SOB validates packet headers and structural integrity.
3. TP is stamped with a SOB sequence identifier (SOB-SID).
4. TP is forwarded to the Residue Extraction stage.

---

## 2. Residue Extraction

After SOB processing, the system extracts the **residue** — the semantically significant remainder of a TP after its primary payload is parsed.

**Definition:**  
The residue `R(TP)` is the set of contextual features that remain latent in a TP after its primary content has been decoded. These features carry routing-relevant signal that the primary payload alone does not expose.

**Extraction steps:**
1. Decode primary TP payload.
2. Diff the decoded content against the TP's raw encoding.
3. Capture the latent feature vector from the diff as `R(TP)`.
4. Normalize `R(TP)` into a fixed-width residue signature `σ`.

**Why residue matters:**  
Direct content-based routing ignores contextual coherence. The residue encodes *how* a TP relates to its neighbors in thought space, which is essential for accurate OB targeting.

---

## 3. Address-Fragment Generation

The normalized residue signature `σ` is used to generate a set of **address fragments** — partial OB addresses that collectively specify a region of the OB address space.

**Fragment generation:**
- `σ` is partitioned into `k` segments: `σ₁, σ₂, …, σₖ`
- Each segment is hashed into an address fragment `Fᵢ = H(σᵢ ∥ SOB-SID)`
- The fragment set `F = {F₁, F₂, …, Fₖ}` represents the TP's addressable footprint

**Properties:**
- Fragments are order-independent — no fragment carries positional priority over another.
- Fragment collisions are expected and handled by the XOR addressing stage (see §4).
- Fragment count `k` is tunable; higher `k` increases address resolution at the cost of routing overhead.

---

## 4. XOR-Based OB Addressing

The fragment set `F` is combined via **XOR folding** to produce a single OB target address.

**Address computation:**

```
OB_ADDR = F₁ ⊕ F₂ ⊕ … ⊕ Fₖ
```

**Why XOR:**
- XOR is commutative and associative — fragment ordering does not affect the result.
- XOR preserves bit diversity across fragments; no single fragment dominates the address.
- Collision rate is bounded and predictable, enabling the RB loop (§6) to resolve conflicts efficiently.

**Address space:**  
`OB_ADDR` maps into a flat OB address space of width `W` bits. The space is divided into fixed-size cells; each cell holds exactly one TP payload plus its residue signature.

---

## 5. Monotonic Similarity Gradient

Before final OB placement, the system evaluates the **monotonic similarity gradient** at the candidate `OB_ADDR` to determine routing fitness.

**Definition:**  
The similarity gradient `∇S` at address `a` measures how smoothly semantic similarity changes across neighboring OB cells around `a`. A monotonic gradient at `a` indicates that the local neighborhood is well-ordered — placing the incoming TP at `a` preserves rather than disrupts semantic continuity.

**Gradient evaluation:**
1. Sample the `n` nearest OB neighbors of `OB_ADDR`.
2. Compute pairwise similarity scores between each neighbor and the incoming TP.
3. Check for monotonicity: scores must be non-increasing as distance from `OB_ADDR` grows.
4. If monotonicity holds → address is accepted.
5. If monotonicity breaks → address is rejected; the RB routing loop is triggered (§6).

**Significance:**  
The gradient check is the primary quality gate for OB placement. It ensures that the OB maintains a globally coherent semantic topology rather than degenerating into a flat hash table.

---

## 6. RB Routing Loop

When an OB address is rejected by the gradient check, or when a collision is detected, the **Routing Buffer (RB) loop** resolves placement.

**Loop structure:**

```
WHILE OB_ADDR is invalid OR occupied:
    OB_ADDR ← next_candidate(OB_ADDR, R(TP))
    evaluate ∇S at OB_ADDR
    IF ∇S is monotonic AND cell is free:
        BREAK
    IF iteration_count > MAX_ITER:
        escalate to RB overflow handler
```

**Candidate generation (`next_candidate`):**
- Perturbs `OB_ADDR` by XOR-ing with a step function derived from `R(TP)` and the current iteration index.
- Guarantees that successive candidates diverge from the original address while remaining within the same semantic neighborhood.

**RB overflow handler:**
- Triggered when `MAX_ITER` is exceeded without a valid placement.
- Logs the TP in the RB overflow queue.
- Initiates a global rebalance scan if the overflow queue depth exceeds threshold `τ`.

**Loop termination guarantees:**
- Because the step function is derived from `R(TP)`, the candidate sequence is deterministic and non-repeating within a finite address space.
- Termination within `MAX_ITER` is guaranteed for address spaces with occupancy below the saturation threshold.

---

## 7. Efficiency Rationale

The combined architecture (SOB → residue → fragments → XOR → gradient → RB) is designed to minimize routing cost while maximizing semantic coherence in the OB.

| Stage | Cost Model | Benefit |
|---|---|---|
| SOB processing | O(1) per TP | Canonical entry, traceability |
| Residue extraction | O(P) where P = payload size | Routing-signal amplification |
| Fragment generation | O(k) | Tunable address resolution |
| XOR folding | O(k) | Collision-bounded, order-free addressing |
| Gradient evaluation | O(n) where n = neighbor count | Semantic topology preservation |
| RB loop | O(MAX_ITER) worst case, O(1) typical | Conflict resolution without global locks |

**Key design choices:**
- **No global lock:** The RB loop resolves conflicts locally, using only the TP's own residue. No system-wide lock is ever acquired during routing.
- **Determinism:** Every stage is deterministic given the same TP input. This enables replay and audit.
- **Tunability:** `k` (fragment count), `n` (gradient neighbors), `MAX_ITER`, and `τ` (overflow threshold) are all runtime-configurable without architectural changes.
- **Graceful degradation:** The overflow handler and rebalance scan ensure the system degrades gracefully under high load rather than hard-failing.

---

## 8. Summary Sequence

```
TP
 └─► SOB intake & validation
       └─► Residue extraction → σ
             └─► Address-fragment generation → F = {F₁…Fₖ}
                   └─► XOR folding → OB_ADDR
                         └─► Monotonic gradient check
                               ├─ PASS → place TP at OB_ADDR
                               └─ FAIL → RB routing loop
                                           ├─ resolve → place TP
                                           └─ overflow → RB overflow handler
```

---

*Document: `routing_of_tp_ob_rb.md` — TS Routing Architecture*
