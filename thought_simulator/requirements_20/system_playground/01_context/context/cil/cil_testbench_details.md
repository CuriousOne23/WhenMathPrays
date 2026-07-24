# **cil_testbench_details.md**  
### *system_playground — CIL Testbench Details (Informative)*

---

# **1. Purpose of the Testbench**  
*(Informative)*

The CIL testbench validates the system_playground implementation of the **Conversation Identity Layer (CIL)**.  
Its purpose is to confirm that CIL correctly integrates:

- identity‑layer objects from **COB**  
- stability signals originating from **CST**  
- ordering metrics  
- ambiguity indicators  
- lineage hints  
- referent certainty/ambiguity fields  

into a single, deterministic **CIL Intake Packet**.  
This packet is consumed directly by **CEx**, as described in *20.107 CEx Extract*   [Current page](citation-section://1146975448/5).

CIL also contributes historical information to the **TP (Thought Packet)**, allowing OuBA to reconstruct:

- what CST did  
- what COB did  
- when they did it  
- how identity‑layer objects evolved during the current message  

This historical continuity is defined in *20.105 TP Requirements*   [Current page](citation-section://1146975448/7).

---

# **2. What the Testbench Evaluates**  
*(Informative)*

The testbench evaluates CIL across five major behaviors:

1. **Identity Selection**  
2. **Certainty & Ambiguity Aggregation**  
3. **Stability Aggregation**  
4. **Lineage Aggregation**  
5. **Packet Construction & TP Integration**  

Each behavior is tested using synthetic identity‑layer objects and ordering metrics produced by COB, along with stability indicators originating from CST.  
(Sections   [Current page](citation-section://1146975448/8),   [Current page](citation-section://1146975448/9))

---

# **3. Why These Behaviors Are Tested**  
*(Informative)*

## **3.1 CEx Compatibility**

CEx consumes **only** the CIL Intake Packet.  
It does not read COB or CST directly   [Current page](citation-section://1146975448/13).  
Therefore, CIL must pack identity‑layer information in the exact structure CEx expects.

The testbench verifies that:

- packet shape matches CEx schema  
- fields appear in the correct blocks  
- ordering, ambiguity, stability, and lineage indicators are preserved  
- packet metadata is consistent  

## **3.2 Historical Continuity for TP**

CIL contributes to TP by embedding:

- CST stability summaries  
- COB identity‑layer transformations  
- ordering and ambiguity indicators  
- lineage hints  
- packet metadata  

This ensures OuBA can reconstruct:

- what happened  
- why it happened  
- when it happened  

## **3.3 Deterministic Behavior**

CEx requires deterministic packet structure for deterministic correction expansion.  
The testbench ensures:

- identical COB + CST inputs → identical packets  
- ordering rules behave deterministically  
- ambiguity and stability aggregation is stable  
- packet metadata is consistent  

---

# **4. How the Testbench Works**  
*(Informative)*

The testbench uses synthetic identity‑layer objects with controlled metrics:

- recency, frequency, density  
- certainty, ambiguity  
- drift, oscillation, collapse  
- freeze/thaw  
- lineage stability  

These objects simulate COB output.  
Stability metrics simulate CST output.

CIL processes these objects and produces a CIL Intake Packet.  
The testbench inspects each block to verify:

- correct selection  
- correct aggregation  
- correct ordering  
- correct stability integration  
- correct lineage integration  
- correct packet metadata  

---

# **5. Detailed Test Descriptions**  
*(Informative — tests preserved, corrected, expanded)*

---

## **5.1 Identity Selection Test**

### **What is tested**  
CIL selects identity‑layer objects using ordering metrics:

- recency  
- frequency  
- density  

A deterministic scoring function is applied:

$$
\text{Score}(o) = w_r r + w_f f + w_d d
$$

### **How it is tested**  
Synthetic objects are assigned ordering metrics.  
CIL selects the top‑ranked objects (default: 5).  
The testbench verifies that selection is deterministic across repeated runs.

### **Why it matters**  
CEx depends on a stable identity set for correction expansion.

### **Expected good results**  
- same inputs → same selected objects  
- ordering block matches expected ranking  
- no oscillation across runs  

### **Expected bad results**  
- inconsistent selection  
- ordering instability  
- nondeterministic ranking  

---

## **5.2 Certainty & Ambiguity Aggregation Test**

### **What is tested**  
CIL extracts certainty and ambiguity indicators from selected objects.

### **How it is tested**  
Objects are assigned synthetic certainty/ambiguity values.  
CIL aggregates these into unified blocks.

### **Why it matters**  
CEx uses these indicators to determine referent confidence and ambiguity expansion.

### **Expected good results**  
- correct aggregated certainty block  
- correct aggregated ambiguity block  
- missing fields handled gracefully  

### **Expected bad results**  
- incorrect aggregation  
- missing indicators  
- nondeterministic ordering  

---

## **5.3 Stability Aggregation Test**

### **What is tested**  
CIL aggregates stability metrics originating from CST:

- drift  
- oscillation  
- collapse  
- merge/split  
- freeze/thaw  

### **How it is tested**  
Objects are assigned synthetic stability metrics.  
CIL aggregates them into a stability block.

### **Why it matters**  
CEx uses stability indicators to determine whether referent expansion should be conservative or aggressive.

### **Expected good results**  
- stability block preserves per‑object values  
- aggregated summaries match expected values  
- deterministic behavior  

### **Expected bad results**  
- incorrect stability summaries  
- nondeterministic aggregation  

---

## **5.4 Lineage Aggregation Test**

### **What is tested**  
CIL collects lineage stability indicators and lineage hints.

### **How it is tested**  
Objects are assigned lineage stability values (stable/unstable).  
CIL aggregates these into a lineage block.

### **Why it matters**  
CEx uses lineage hints to determine referent inheritance and identity continuity.

### **Expected good results**  
- lineage block contains correct stability indicators  
- lineage hints preserved  
- deterministic ordering  

### **Expected bad results**  
- incorrect lineage propagation  
- nondeterministic lineage ordering  

---

## **5.5 Packet Construction & TP Integration Test**

### **What is tested**  
CIL constructs the full CIL Intake Packet:

$$
\text{Packet} = \{ \text{IdentitySet},\ \text{Ordering},\ \text{Ambiguity},\ \text{Stability},\ \text{Lineage} \}
$$

### **How it is tested**  
The testbench inspects each block for:

- correct fields  
- correct ordering  
- correct aggregation  
- correct metadata  

### **Why it matters**  
CEx consumes this packet directly.  
TP captures this packet for historical continuity.

### **Expected good results**  
- packet structure matches CEx schema  
- packet metadata is correct  
- packet is deterministic  
- fields are internally consistent  

### **Expected bad results**  
- malformed blocks  
- missing fields  
- nondeterministic packet structure  

---

## **5.6 NEW — Next‑Turn Context Representation Test**

### **What is tested**  
CIL must represent next‑turn context fields exactly as provided by COB.

### **How it is tested**  
1. Synthetic next‑turn context fields are inserted into COB.  
2. COB merges them into the stabilized snapshot.  
3. CIL receives the snapshot and constructs the packet.  
4. The testbench inspects the next‑turn context block.

### **Why it matters**  
CEx relies on next‑turn context for continuity across turns.

### **Expected good results**  
- fields appear exactly as provided  
- no mutation, repair, or reinterpretation  
- deterministic representation  

### **Expected bad results**  
- field duplication  
- semantic reinterpretation  
- nondeterministic ordering  

---

# **6. What Good Results Look Like**  
*(Informative)*

A successful testbench run produces:

- deterministic identity selection  
- correct certainty/ambiguity aggregation  
- correct stability aggregation  
- correct lineage aggregation  
- correct ordering metrics  
- correct packet metadata  
- stable packet structure across repeated runs  
- no missing fields  
- no malformed blocks  
- no ordering oscillation  
- no ambiguity spikes  
- no stability misalignment  

The final packet is ready for consumption by CEx and insertion into TP.

---

# **7. Summary**  
*(Informative)*

The CIL testbench ensures that CIL:

- integrates COB and CST outputs  
- produces deterministic packets  
- preserves ordering, ambiguity, stability, and lineage  
- packs fields exactly as CEx expects  
- contributes historical continuity to TP  
- behaves predictably under controlled inputs  

This guarantees that CEx receives a stable, interpretable identity‑layer context for correction expansion, and that OuBA can reconstruct the full historical chain of identity‑layer processing.

---
Just tell me what you want next.
