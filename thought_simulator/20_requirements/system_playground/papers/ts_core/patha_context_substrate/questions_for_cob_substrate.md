# **questions_for_cob_substrate.md**  
### *COB Substrate — Operational Questions (Working Paper v0.3)*

---

## **0. Purpose**
This working paper collects all **operational questions** that must be answered before the Conversation Object Basin (COB) can be fully specified.

COB is the keystone of the TS context layer.  
Once COB is solid, CST, CIL, CEx, SSRGn, temporal ordering, snapshot strategy, and collapse/recovery become straightforward.

This paper will grow until the question surface saturates, then shrink as answers stabilize.

---

# **1. Core Operational Questions (Highest Priority)**  
These are the foundational questions that define COB’s behavior.  
Answering these unlocks the entire TS context layer.

---

## **1.1 Identity Layer Model**
1. What is the exact schema of an identity layer?  
2. What fields must each layer contain (referent map, lineage, strength, ambiguity, timestamps, decay state)?  
3. Fixed array of 20 slots or dynamic with a hard cap?  
4. How is lineage represented (tree, DAG, linked list, versioned history)?  
5. How are multi-word referents and competing referents represented?

---

## **1.2 Referent Map Model**
6. What is the exact schema of a referent map entry?  
7. How are surface forms, attributes, strength, confidence, ambiguity, and lineage pointers stored?  
8. How are multi-turn referent updates merged?

---

## **1.3 Layer Lifecycle & Capacity**
9. How are new layers created, split, merged, weakened, strengthened, or retired?  
10. What is the aging/decay policy?  
11. What happens when all 20 layers are occupied or when a new distinct identity appears?

---

## **1.4 Update Mechanics**
12. How does COB ingest and merge new SSRGn meaning?  
13. What are the rules for conflict resolution between new meaning and existing layers?  
14. How does COB handle ambiguous, partial, or conflicting referents?  
15. How does COB handle referent explosion or collapse?

---

# **2. Supporting Operational Questions**  
These questions refine COB’s behavior once the core model is defined.

---

## **2.1 Determinism & Replay**
16. How is the full COB state replayed deterministically from the SSRGn sequence?  
17. How are layer IDs, referent IDs, and snapshots versioned for auditability?  
18. How are merge/split/decay operations made deterministic?

---

## **2.2 Interaction with CST**
19. What COB fields does CST read?  
20. What signals does CST send and how are they applied or rejected?  
21. How does COB maintain determinism under CST corrections?

---

## **2.3 Interaction with CIL**
22. What COB fields does CIL read?  
23. How does CIL merge short-term cues with COB identity layers?  
24. How does CIL handle ambiguous or conflicting COB layers?

---

## **2.4 Interaction with CEx**
25. What COB fields does CEx read?  
26. How does CEx use referent maps, lineage, and strength/importance?

---

## **2.5 Interaction with SSRGn & Path B**
27. What SSRGn fields does COB ingest?  
28. How does COB merge regenerated meaning, ambiguity, and structure?  
29. What COB information is relevant to Path B (via CoHI or other mechanisms)?

---

## **2.6 Collapse & Recovery**
30. What constitutes identity collapse, referent collapse, lineage collapse, or continuity collapse?  
31. What emergency signals exist?  
32. How does COB detect and recover from collapse?

---

## **2.7 Resource Constraints & Scaling**
33. Maximum referents per identity layer?  
34. Maximum ambiguity entries, lineage depth, or updates per turn?  
35. How do we prevent memory blow-up across long sessions?

---

# **3. Additional Operational Questions (System-Identified)**  
These questions emerged from architectural analysis and are required for a complete COB substrate.

---

## **3.1 Operational Timing & Turn Integration**
36. When exactly does COB update during a turn?  
37. Is COB updated once per turn or multiple times?  
38. Does COB update synchronously or asynchronously with CST signals?  
39. Does COB produce a stable snapshot each turn?

---

## **3.2 Operational Merge Behavior**
40. How does COB handle partial updates?  
41. How does COB handle contradictory updates?  
42. How does COB handle noisy or low-confidence updates?  
43. How does COB handle updates that apply to multiple layers?

---

## **3.3 Operational Split Behavior**
44. What operational threshold triggers a split?  
45. How does COB split a layer without losing continuity?  
46. How does COB assign referents to new layers after a split?

---

## **3.4 Operational Decay & Aging**
47. How does COB decay old or unused identity layers?  
48. How does COB decay referent strength over time?  
49. How does COB decay ambiguity over time?  
50. How does COB decay lineage depth?

---

## **3.5 Operational Pruning & Compression**
51. What information is pruned from identity layers?  
52. How does COB compress referent maps?  
53. How does COB summarize lineage instead of storing full history?  
54. How does COB prune ambiguity entries?

---

## **3.6 Operational Assignment & Routing**
55. What is the operational algorithm for assigning new information to a layer?  
56. What similarity metrics are used?  
57. How does COB handle ambiguous assignment?  
58. How does COB handle multi-layer assignment?

---

## **3.7 Operational Eviction Policy**
59. What is the eviction policy when the 21st conversation appears?  
60. Do we evict the weakest? The oldest? The least-used?  
61. Do we merge before evicting?  
62. Can CST override eviction decisions?

---

## **3.8 Operational Interaction with Path A**
63. Does COB provide identity hints back to Path A?  
64. Does COB influence referent candidate generation?  
65. Does COB influence structural token interpretation?  
66. Does COB influence SSRGn regeneration?

---

## **3.9 Operational Interaction with Path B**
67. What COB information is relevant to Path B?  
68. Does Path B read identity layers?  
69. Does Path B read referent maps?  
70. Does Path B read lineage?  
71. Does Path B read ambiguity?

---

## **3.10 Operational Failure Modes**
72. How does COB detect identity collapse?  
73. How does COB detect referent collapse?  
74. How does COB detect lineage collapse?  
75. How does COB detect continuity collapse?  
76. What emergency signals exist?  
77. How does COB recover from collapse?

---

# **4. Final Missing Operational Questions (Keystone Additions)**  
These are the last remaining operational questions needed for full saturation.

---

## **4.1 Identity Drift vs. Topic Drift**
78. How does COB distinguish identity drift from topic drift?  
79. How does COB detect when a topic shift should NOT create a new identity layer?  
80. How does COB detect when a topic shift SHOULD create a new identity layer?

---

## **4.2 Referent Fusion vs. Referent Collision**
81. How does COB detect when two referents should be fused?  
82. How does COB detect when two referents should remain separate?  
83. How does COB detect referent collision (same surface form, different meaning)?

---

## **4.3 Identity Freeze / Thaw Mechanism**
84. Does COB support an identity freeze state?  
85. What operations are allowed on a frozen layer?  
86. What operations are forbidden on a frozen layer?  
87. How does COB thaw a frozen layer?

---

# **5. Next Steps**
- Confirm that the COB question surface is now saturated.  
- Begin answering the keystone questions in `cob_context_resolution.md`.  
- Extract stable answers into formal 20.x requirement documents.  
- Shrink this paper as answers accumulate.

---
