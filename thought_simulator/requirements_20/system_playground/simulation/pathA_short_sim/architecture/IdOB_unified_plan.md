# IdOB — Path-A meaning contract and unified plan
## Theory · Architecture · Engine · Debugger · Log contract
### Path-A short simulator
### 2026-09-23; meaning lock 2026-09-28

Status: consolidated plan. R1–R3 and D1–D3 landed. R4a catalog next.
Scope: short sim only. Meaning Composition Block (MCB) omitted (R5).
Seam (names, on-ramp): [idob_seam.md](idob_seam.md)
Object space (eight catalog families): [idob_object_space.md](../notes/idob_object_space/idob_object_space.md)
Meaning-as-packet teaching contract: [idob_meaning_lock.md](idob_meaning_lock.md)
Observer: [user_guide.md](../user_guide.md)

Construct: **Identity Observation Block (IdOB) space $\mathcal{I}$ is a frozen registry of IdOB objects (IdOBObjects);
IdOB is the deterministic overlap-sum of their contributions;
the packet on the Thought Packet (TP) is that sum; the debugger observes that packet;
`run_examples.py` is the emitter that makes the space visible.**

Meaning on this path is the packet. Details and the instrument alias table live in [idob_meaning_lock.md](idob_meaning_lock.md). Do not import Meaning Signal Layer (MSL), Cognitive Identity Envelope (CIE), or Structure-to-Meaning (S2M) $M$ into this file as if they ran here. R5 does not become their parking lot.

---

## 0. Four layers, one fog

| Layer | Owner files | Current reality |
|---|---|
| Theory | seam, meaning lock, this plan | Meaning($U$)=IdOB($U$) as packet; space = eight YAML files |
| Architecture | PSC / object schema | Catalog exists; apply still bound to `idob.legacy` |
| Engine | `idob/sum.py`, `idob/packets.py`, `idob/registry.py` | Split objects write the packet; `semantic_core` merged as dict |
| Observer | `run_examples.py` → `run.log` → `pathA_dbug.py` | Teaching cards updated 2026-09-28; debugger must not re-sum |

Hard rule: **the debugger does not move until the engine has one writer and the log emits a space.**

---

## 1. Naming lock (all four layers)

See also [idob_seam.md](idob_seam.md).

| Token | Meaning |
|---|---|
| IdOB | Summation operator / primitive. Not an object. |
| IdOB space $\mathcal{I}$ | Frozen registry snapshot |
| IdOBObject | One bounded extractor |
| family | YAML `family` field. Helpers may share another family (see object-space). |
| activation / activation_set | Objects with act=1 |
| inactive_objects | $\mathcal{I}\setminus A(U)$ |
| contribution / contributions | Per-object packet fragments |
| contributors | Activated ids, `(priority, name)` order |
| idob_packet | Sum written to `tp.idob` |
| semantic_core | **dict only** after IdOB |
| selected_ops | list[str], stable unique |
| identity_geometry | structural_identity \| referential_identity \| semantic_identity |
| truth_relation | mood: declarative \| interrogative \| unknown |
| truth_relation_family | descriptive_state \| descriptive_locative \| descriptive_mixed \| interrogative_wh \| interrogative_polar \| unknown |
| tru_hint | TRU mood hint on TP / log |
| tru_alignment | tru_hint vs summed mood |
| overlap_near / overlap_far | Declared edges |
| overlap_mode | merge \| suppress \| blend \| coexist |
| overlap_events | Executed resolutions `{a,b,mode,fields}` |
| meaning_delta | Legacy vs split claimed fields |
| PSC / psc_violations | Contract + logged breaks |
| registry_digest | Hash of object YAML |
| residual_activated | residual_identity in $A(U)$ |
| R0–R6 | Engine gates |
| D0–D4 | Debugger gates |

Forbidden: “IdOB object” as the primitive; list `semantic_core` as canonical; debugger-only synonyms; six linguistic types as the catalog; importing MSL / CIE / S2M $M$ into this packet.

---

## 2–10. Engine, log, debugger, gates

Unchanged in substance from the 2026-09-23 plan: theory sum, catalog frame, invariants I1–I10, packet schema §3.3, log contract, debugger observer rule, R0–R6 / D0–D5, gate proofs.

Live corrections against YAML:

- Eight **files**; `agent_action.family` is `residual_identity`; `modifier_resolution.family` is `mixed_descriptive`.
- Apply symbols still `idob.legacy:_…_apply`. Empty `activation: {}` is legal in v1.
- R5 remains MCB copies only. R5 does not receive MSL, CIE, or S2M geometry.
- Open item: helper-vs-family lock; empty activation trees vs documented predicate language.

One-sentence plan: **R1–R3 made the sum real; D1–D3 observe the packet; R4a names $\mathcal{I}$ as a hashed YAML catalog; the packet stays still; meaning here stays the packet.**
