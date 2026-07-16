## **0. Purpose**
This working paper collects all **operational questions** that must be answered before the Conversation Object Basin (COB) can be fully specified.

COB is the keystone of the TS context layer.  
Once COB is answered, CST, CIL, CEx, SSRGn, temporal ordering, snapshot strategy, and collapse/recovery will fall naturally into place.

This paper will grow until the question surface saturates, then shrink as answers stabilize.

---

# **1. Core Operational Questions (User‑Identified)**

These are the foundational operational questions that define COB’s behavior.

### **1.1 Priority & Relevance**
1. How do we establish priority of COB conversations — which one is relevant now, which is second, etc.?

### **1.2 Communication Upstream**
2. Do we communicate that priority to Path A? If so, how?

### **1.3 Capacity & Eviction**
3. How do we update the 20 conversations?  
   If the 21st comes along, which do we overwrite/replace and why?

### **1.4 Information Density**
4. How much information do we store in the 20 conversations?

### **1.5 Information Type**
5. What type of information do we look for and store — and why?

### **1.6 Path A / Path B Relevance**
6. What information is useful to Path A and eventually to Path B?

### **1.7 Assignment**
7. How does COB discern which information goes with which conversation or a new conversation?

### **1.8 New Conversation Resolution**
8. What is the resolution of a new conversation — when does it become a new conversation vs. additional information to an old one?

### **1.9 Size Control**
9. How do we keep control of the size of each conversation?  
   We cannot let it grow unbounded.

---

# **2. Additional Operational Questions (System‑Identified)**

These are additional operational questions required for a complete COB substrate.

---

## **2.1 Operational Timing & Turn Integration**
10. When exactly does COB update during a turn?  
11. Is COB updated once per turn or multiple times?  
12. Does COB update synchronously or asynchronously with CST signals?  
13. Does COB produce a stable snapshot each turn?

---

## **2.2 Operational Merge Behavior**
14. How does COB handle partial updates?  
15. How does COB handle contradictory updates?  
16. How does COB handle noisy or low-confidence updates?  
17. How does COB handle updates that apply to multiple layers?

---

## **2.3 Operational Split Behavior**
18. What operational threshold triggers a split?  
19. How does COB split a layer without losing continuity?  
20. How does COB assign referents to new layers after a split?

---

## **2.4 Operational Decay & Aging**
21. How does COB decay old or unused identity layers?  
22. How does COB decay referent strength over time?  
23. How does COB decay ambiguity over time?  
24. How does COB decay lineage depth?

---

## **2.5 Operational Pruning & Compression**
25. What information is pruned from identity layers?  
26. How does COB compress referent maps?  
27. How does COB summarize lineage instead of storing full history?  
28. How does COB prune ambiguity entries?

---

## **2.6 Operational Assignment & Routing**
29. What is the operational algorithm for assigning new information to a layer?  
30. What similarity metrics are used?  
31. How does COB handle ambiguous assignment?  
32. How does COB handle multi-layer assignment?

---

## **2.7 Operational Eviction Policy**
33. What is the eviction policy when the 21st conversation appears?  
34. Do we evict the weakest? The oldest? The least-used?  
35. Do we merge before evicting?  
36. Can CST override eviction decisions?

---

## **2.8 Operational Interaction with Path A**
37. Does COB provide identity hints back to Path A?  
38. Does COB influence referent candidate generation?  
39. Does COB influence structural token interpretation?  
40. Does COB influence SSRGn regeneration?

---

## **2.9 Operational Interaction with Path B**
41. What COB information is relevant to Path B?  
42. Does Path B read identity layers?  
43. Does Path B read referent maps?  
44. Does Path B read lineage?  
45. Does Path B read ambiguity?

---

## **2.10 Operational Failure Modes**
46. How does COB detect identity collapse?  
47. How does COB detect referent collapse?  
48. How does COB detect lineage collapse?  
49. How does COB detect continuity collapse?  
50. What emergency signals exist?  
51. How does COB recover from collapse?

---

# **3. Next Steps**
- Confirm question saturation.  
- Begin answering the keystone questions in `cob_context_resolution.md`.  
- Extract stable answers into formal 20.x requirement documents.  
- Shrink this paper as answers accumulate.

---
