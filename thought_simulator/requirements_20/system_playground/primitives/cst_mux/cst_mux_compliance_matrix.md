| Requirement (20.32.010.030) | Status | Notes |
| --- | --- | --- |
| **Accept all CST‑Core raw metric signals** | **Implemented** | Core metrics and signals are read and packaged. |
| **Accept all CST‑Core structural signals (Freeze, Thaw, Continuity)** | **Implemented** | Lists are read and passed through. |
| **Accept all CST‑MS synthesized stability signals** | **Implemented** | MS stability/instability/collapse risk/etc. included. |
| **Accept all CST‑MS command records** | **Implemented** | Commands and command logs are copied into USP. |
| **Accept MS diagnostics (sync mismatch)** | **Implemented** | Diagnostic fields included. |
| **Accept MS metadata (**``new_context_required``**)** | **Implemented** | Propagated into USP. |
| **No COB input** | **Implemented** | No COB reads in code. |
| **USP must NOT be sent to COB** | **Partially Implemented** | USP is not sent to COB, but no explicit routing marker to CIL. |
| **USP delivered exclusively to CIL** | **Partially Implemented** | USP exists under ``TP.cst.mux``, but no explicit CIL‑routing field. |
| **Deterministic layer indexing** | **Implemented** | StableID collection + lexicographic sorting. |
| **Deterministic alignment of signals by layer** | **Implemented** | Core/MS signals aligned under USP. |
| **No modification, reinterpretation, or synthesis of signals** | **Implemented** | Pure packaging; no thresholding. |
| **Flags recorded as received (presence‑based)** | **Implemented** | Freeze/thaw/continuity flags reflect upstream presence. |
| **No threshold‑based flag policy** | **Implemented** | Heritage thresholds removed; no reinterpretation. |
| **Deterministic replay (same inputs → same USP)** | **Implemented** | No randomness; stable ordering. |
| **Full inclusion of Core/MS subtrees** | **Partially Implemented** | Some subtrees summarized; not full deep copy. |
| **Write‑boundary guard (no mutation outside cst.mux)** | **Not Implemented** | Code respects boundary but does not enforce it programmatically. |
| **Merge/split neutrality** | **Partially Implemented** | Behavior is neutral, but explicit tests not present. |
| **Multi‑turn USP window (**``usp_window``**)** | **Not Implemented** | Optional feature; not required by HLR. |
| **Top‑level **``new_context_required``** field** | **Implemented** | Correctly propagated. |
| **Deterministic key ordering in USP** | **Implemented** | Fixed order in structural program; heritage code mostly follows. |
| **No commands issued to COB/CIL** | **Implemented** | No command emission. |
| **No mutation of Core/MS fields** | **Implemented** | Read‑only access. |
| **No structural authority** | **Implemented** | CST‑Mux is pure packaging only. |
