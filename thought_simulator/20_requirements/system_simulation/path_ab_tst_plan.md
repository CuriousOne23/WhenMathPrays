# **TS Path A+B Integration Test Plan (Revised)**  
### **Version: TS‑ITP‑AB‑002**

This version introduces:

- **Numeric scoring**  
- **Separate expectations for Path A, Path B, and A+B**  
- **Explicit metrics**  
- **Clear pass/fail thresholds**  

---

# **0. Scoring Framework**

Each test produces **three scores**, each 0–100:

| Component | Meaning | Passing Threshold |
|----------|----------|------------------|
| **A‑Score** | Path A correctness | ≥ 90 |
| **B‑Score** | Path B correctness | ≥ 90 |
| **AB‑Score** | A+B integration correctness | ≥ 90 |

Final test result:

- **PASS** if all three ≥ 90  
- **FAIL** otherwise  

---

# **1. Test Structure Template (Used for AB1–AB8)**

Each test now has:

### **1. Input Specification**
- Raw input  
- Metadata  
- Fault injection (if any)  
- Concurrency conditions (if any)

### **2. Path A Expected Output**
- Meaning envelope  
- Referent map  
- OB/RB/TB trace  
- Truth-state (TPTB)  
- Safety-state (TPSF)  
- Stability envelope  
- Invariants  
- Error class (if applicable)

### **3. Path B Expected Output**
- Expression envelope  
- Tone  
- Stance  
- Style  
- Emotional mirroring  
- Discourse mode  
- Final natural-language output  
- Human-readable TP projection

### **4. A+B Integration Expectations**
- Meaning preserved  
- Truth preserved  
- Safety preserved  
- No referent drift  
- No semantic mutation  
- Expression applied correctly  
- TP internally consistent  

### **5. Metrics**
- Latency  
- Routing correctness  
- Truth/safety correctness  
- Referent stability  
- Checksum integrity  
- Cross-session leak count  
- Error-class correctness  

### **6. Scoring**
- A‑Score  
- B‑Score  
- AB‑Score  

---

# **2. Test Cases**

### **2.0 Why These Eight Tests (Rationale for the AB‑Suite)**  
The AB1–AB8 suite is not specific to any one architecture. These eight tests represent the minimal, complete, and orthogonal set of failure modes that any cognitive or reasoning system can exhibit, regardless of implementation details. Any system that processes meaning, maintains internal state, and produces structured output can fail in only eight distinct ways: (1) failure on the clean path, (2) failure at boundaries, (3) failure under degraded input, (4) failure under structural faults, (5) failure of isolation when multiple thought streams are active, (6) failure of semantic integrity within its internal representations, (7) failure to correctly handle contradictions within the content itself, and (8) failure to maintain stability over extended sequences (drift).

Each AB test isolates exactly one of these failure modes. Together, they provide full coverage of the invariants required for stable reasoning: correctness, boundary safety, repair‑without‑invention, structural integrity, isolation, semantic integrity, contradiction preservation, and long‑horizon stability. The tests do not overlap, and removing any one of them would leave a blind spot in the system’s safety or correctness guarantees. This makes the AB‑suite the smallest set of tests that still provides complete architectural validation for any system intended to perform reliable cognitive or semantic processing.

---

## **AB1 — Happy Path**

### **Input**
A clean, unambiguous user message.

### **Path A Expected Output**
- Correct meaning envelope  
- Correct referents  
- Correct OB/RB/TB trace  
- TPTB = TRUE or SUPPORTED  
- TPSF = SAFE  
- No errors  
- All invariants satisfied  

### **Path B Expected Output**
- Tone appropriate  
- No semantic drift  
- Style applied correctly  
- Human-readable TP projection correct  

### **A+B Integration**
- Meaning preserved  
- Truth preserved  
- Safety preserved  
- Expression correct  

### **Metrics**
- Latency A ≤ 40 ms  
- Latency B ≤ 15 ms  
- Routing correctness ≥ 98%  
- Referent stability = 100%  
- Checksum valid  
- Leak count = 0  

### **Scoring**
- **A‑Score:** 0–100  
- **B‑Score:** 0–100  
- **AB‑Score:** 0–100  

---

## **AB2 — Boundary Conditions**

### **Input**
Minimal or maximal valid input.

### **Path A Expected Output**
- Meaning envelope still correct  
- TPTB = TRUE or UNKNOWN  
- TPSF = SAFE  
- No silent drops  

### **Path B Expected Output**
- Minimal expression  
- No hallucination  
- No over‑interpretation  

### **A+B Integration**
- No drift  
- No over‑projection  

### **Metrics**
- Latency within budget  
- Routing correctness ≥ 95%  

### **Scoring**
Same 3‑score system.

---

## **AB3 — Degraded Input**

### **Input**
Noisy, partial, or malformed but recoverable.

### **Path A Expected Output**
- Meaning envelope repaired  
- TPTB = UNKNOWN or PARTIAL  
- TPSF = SAFE  
- Repair markers present  

### **Path B Expected Output**
- Neutral tone  
- No invented meaning  

### **A+B Integration**
- Meaning preserved  
- No semantic invention  

### **Metrics**
- Repair success ≥ 90%  
- No hallucination  

### **Scoring**
Same 3‑score system.

---

## **AB4 — Fault Injection**

### **Input**
Checksum mismatch, missing ID, corrupted field.

### **Path A Expected Output**
- TPSF = BLOCK  
- Error class = STRUCTURAL  
- No meaning envelope produced  

### **Path B Expected Output**
- No synthesis  
- Error message only  

### **A+B Integration**
- Safety boundary respected  

### **Metrics**
- Correct error class  
- No output leakage  

### **Scoring**
Same 3‑score system.

---

## **AB5 — Concurrency**

### **Input**
Two or more simultaneous requests.

### **Path A Expected Output**
- Session isolation  
- No cross‑session contamination  
- Leak count = 0  

### **Path B Expected Output**
- Independent expression envelopes  

### **A+B Integration**
- No cross‑session drift  

### **Metrics**
- Isolation = 100%  
- Latency stable  

### **Scoring**
Same 3‑score system.

---

## **AB6 — Structural Corruption**

### **Input**
Malformed JSON, missing fields, invalid types.

### **Path A Expected Output**
- TPSF = BLOCK  
- Error class = STRUCTURAL  

### **Path B Expected Output**
- No synthesis  

### **A+B Integration**
- Safety preserved  

### **Metrics**
- Correct error class  
- No partial output  

### **Scoring**
Same 3‑score system.

---

## **AB7 — Semantic Contradiction**

### **Input**
Two contradictory claims.

### **Path A Expected Output**
- TPTB = CONTRADICTORY  
- Both claims represented  
- No collapse  

### **Path B Expected Output**
- Neutral tone  
- No resolution invented  

### **A+B Integration**
- Meaning preserved  
- Contradiction surfaced  

### **Metrics**
- Contradiction detection ≥ 95%  

### **Scoring**
Same 3‑score system.

---

## **AB8 — Regression**

### **Input**
Previously failing cases.

### **Path A Expected Output**
- All prior failures fixed  
- No regressions  

### **Path B Expected Output**
- Stable expression  

### **A+B Integration**
- All invariants preserved  

### **Metrics**
- Regression count = 0  

### **Scoring**
Same 3‑score system.

---
