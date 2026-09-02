date: 2026-09-02
events processed: EVENT policy 2026-08-30; EVENT decision 2026-08-30 (stamp=human); EVENT doc-change field-name authority 20.116 2026-08-30 (stamp=human); EVENT decision Cluster 1 IdOB invoke 2026-08-30 (stamp=human); EVENT decision Cluster 2 meaning-write 2026-08-30 (stamp=human); EVENT decision Cluster 3 OuBA door 2026-08-30 (stamp=human); EVENT doc-change 20.40 v1.3 2026-08-30 (stamp=human); EVENT decision TP.semantic.importance IdOB-prm 2026-08-31 (stamp=human); EVENT doc-change Path-A wording alignment 2026-08-31 (stamp=human, kind=view); Harness charter 2026-09-02 (stamp=human); Terms charter 2026-09-02 (stamp=human); EVENT policy Terms charter amend 2026-09-02 (stamp=human)
flow-tracker = 20.705 §2 and §3.6
field-name authority = 20.116 series
20.40 v1.3; freeze = HLR-20.40-019; 003/007/008 = SOB–SmOB only.
TP.semantic.importance writer = IdOB-prm only; routing = structure fields.
Path-A wording alignment in one off-main PR; write=no on main requirement files until merge.
decision: CTP means only the 20.145 primitive (Path A hop in 20.705 §2). HLR-20.40-017 is NA. OuBA commit is not called CTP.
decision: Cluster 1 — IdOB invoke and stretch. Winner is HLR-20.40.050-062 and 20.705 §2. HLR-20.40.050-011 (invoke only after RB→RTU) is NA.
decision: Cluster 2 — meaning-write law. Winner is 20.116.020-003, HLR-20.105-116, and IdOB-prm. Only IdOB-prm may birth stand-in M, TP.idob, and TP.semantic.meaning_delta_h (plus listed root flags). 20.40 umbrella “no semantic interpretation” on 20.40.010–.060 does not apply to IdOB-prm.
decision: Cluster 3 — OuBA door and conversation polarity. Winner is 20.15 §2.14 and 20.116: OuBA freeze is the sole COB meaning-ingest door.
decision: IdOB-prm is the sole producer of TP.semantic.importance. SOB/SROB/SmOB/CnOB local envelope importance is not a write of TP.semantic.importance. Routing uses structure fields only.
expect (importance 2026-08-31): Meaning: mark global-importance ownership as IdOB-prm only. Local envelope importance on SOB/SROB/SmOB/CnOB is not a write of TP.semantic.importance. Route: do not route on TP.semantic.importance. Score structure fields only. Matrix: do not add a new hop row for importance. Inventory only when the wording PR lands. Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “TP.semantic.importance writer = IdOB-prm only; routing = structure fields.” Do not edit requirement files. Do not create Bots or writers.
expect (wording alignment 2026-08-31, kind=view): Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “Path-A wording alignment in one off-main PR; write=no on main requirement files until merge.” write=no on main copies of the files listed above. Do not land edits on main from bots. Score 20.705 §2 verbatim. Do not treat a shortened chain (e.g. CTP→RB→RTU→IdOB→OuBA→COB/CST) as law. Do not create Bots. Do not start a 20.705 cleanup. Do not declare Path B inactive.
scoring: 20.705 §2 is the Path A string as written. Score R-002 / M-009 / M-011 against §2. Do not replace §2 with a shorter chain. write=no.
spine:

S1 | files=20.31, 20.15, 20.206 | shalls=HLR-20.206-001, HLR-20.206-002, HLR-20.206-003, VR-6 | issue=open: 20.206 wording, not a new door | why it matters=B consume-OuBA vs reject-meaning still a 20.206 wording conflict | owner=human | write=no
S1 remains open 2026-08-30 | 20.206 wording, not as a new door.

S2 | files=20.15, 20.31 | shalls=HLR-20.31-004, HLR-20.31-005, HLR-20.31-006 | issue=scaffold vs 20.31 mismatch | why it matters=20.31 forbids standalone Path A meaning fields that 20.15 still lists on the TP datapacket | owner=human | write=no

S3 | files=20.206 | shalls=HLR-20.206-005, IMR-B, IMR-C | issue=open: 20.206 wording, not a new door | why it matters=IMR-B re-run B vs route through Path A is still a 20.206 wording conflict | owner=human | write=no
S3 remains open 2026-08-30 | 20.206 wording, not as a new door.

S4 | files=20.206, 20.700.050 | shalls=HLR-20.206-003, HLR-20.206-006 | issue=support file citing a hop the spine does not allow | why it matters=20.700.050 (cited by HLR-20.012-033/035) feeds Path B via KnB/SSR and CoHI; 20.206’s exclusive B-start list and A→OuBA→B→OuBB order do not include those hops | owner=human | write=no

E1 | files=20.705, 20.15, 20.12, 20.206 | shalls=20.15-§3 (no id), HLR-20.012-005, HLR-20.012-020, HLR-20.206-006 | issue=support file citing a hop the spine does not allow / contradictory shalls: §3.6 hop CIL→CEx re-enters Path A CEx after OuBA, while §2/20.15 place CEx only after IE and treat OuBA as Path A exit | why it matters=§3.6 hop CIL→CEx re-enters Path A CEx after OuBA, while §2/20.15 place CEx only after IE and treat OuBA as Path A exit | owner=human | write=no
E1 decided 2026-08-30 | two CEx jobs.

E2 | files=20.705, 20.15 | shalls=20.15-§2.14 (no id), 20.15-§4.22 (no id) | issue=decided: command vs ingest | why it matters=§3.6 CSTCore→COB and CSTMS→COB are command hops, not COB ingest; 20.15 ingest door remains OuBA freeze only | owner=human | write=no
E2 decided 2026-08-30 | command vs ingest.

meaning:

M-001 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-007, HLR-20.40-008, HLR-20.40.050-001, HLR-20.105-094, HLR-20.105-116 | decided 2026-08-31 stamp=human against 20.40 v1.3. Remaining 20.40 wording is done. | closed against 20.40 v1.3 | owner=human | write=no

M-002 | 20.40_ob_requirements.md, 20.40.010_sob_prim.md, 20.40.020_srob_prim.md, 20.40.030_cnob_prim.md, 20.40.040_smob_prim.md | HLR-20.40-003 vs HLR-20.40.010-030, HLR-20.40.020-027, HLR-20.40.030-011, HLR-20.40.040-014 | decided 2026-08-31 stamp=human against 20.40 v1.3 (read ≠ write). Remaining 20.40 wording is done. | closed against 20.40 v1.3 | owner=human | write=no

M-003 | 20.40.010_sob_prim.md, 20.40.020_srob_prim.md, 20.105.010_tp_meta_fields.md, 20.105_tp_requirements.md | HLR-20.40.010-016, HLR-20.40.010-028, HLR-20.40.020-026, HLR-20.40.020-036, HLR-20.105-096 | Missing SOB→SROB handoff: SROB SHALL accept and refine structural-importance emitted by SOB; SOB residue/output shalls never name importance. TP still lists SOB as a producer of TP.semantic.importance. | First hop of the importance chain has no SOB producer. | owner=human | write=no

M-004 | 20.40_ob_requirements.md, 20.40.040_smob_prim.md, 20.40.050_idob_prim.md | HLR-20.40-001, HLR-20.40-016, HLR-20.40.040-028, HLR-20.40.040-038, HLR-20.40.050-032 | Missing SmOB→IdOB handoff: chain certifies valid input for next through SmOB, then SmOB SHALL be valid for SSG and RB only; IdOB SHALL refine SmOB importance; umbrella may route to IdOB or OuBA instead of finishing SmOB. | IdOB’s SmOB-cue duty is not a certified hop, and the umbrella can skip the producer. | owner=human | write=no

M-005 | 20.32_cob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md, 20.105.010_tp_meta_fields.md | HLR-20.32-004, HLR-20.32-016, HLR-20.32-111, HLR-20.32-112, HLR-20.32-129, HLR-20.32-138, HLR-20.105-106, HLR-20.105-107 | decided 2026-08-31 stamp=human: no mid-lineup COB meaning write | closed: no mid-lineup COB meaning write | owner=human | write=no

M-006 | 20.32_cob_requirements.md, 20.105_tp_requirements.md, 20.105.010_tp_meta_fields.md | HLR-20.32-062, HLR-20.32-079, HLR-20.32-117–136, HLR-20.105-094, HLR-20.105-116, HLR-20.105.010-001 | Field-ledger / write-authority mismatch: COB SHALL maintain TP.cob.* and ingest TP.next_context{}, and SHALL append TP.lineage_log[]; 20.105.010 has no TP.cob and places next-context under TP.metadata.next_context.*; TP write law excepts only TPU, OuBA, and listed IdOB paths. | COB’s named TP hops are not on the ledger and not in the write exception. | owner=human | write=no

M-007 | 20.32_cob_requirements.md | HLR-20.32-083, HLR-20.32-095, HLR-20.32-097, HLR-20.32-100, HLR-20.32-103 | Contradictory shalls on the COB next-context handoff: merge next-turn fields into identity layers and into clarifying structures; treat those fields as read-only and reflect them without modification; SHALL NOT write them into current-turn clarifying fields. | COB cannot jointly merge, not-modify, and not-write the same next-turn clarifying payload. | owner=human | write=no

M-008 | 20.32_cob_requirements.md, 20.105_tp_requirements.md | HLR-20.32-003, HLR-20.32-009, HLR-20.32-054, HLR-20.105-103, HLR-20.105-104 | decided 2026-08-31 stamp=human as two CEx jobs | closed as two CEx jobs | owner=human | write=no

M-009 | 20.40_ob_requirements.md | HLR-20.40-001, HLR-20.40-016 | decided 2026-08-31 stamp=human toward 20.705 §2. Remaining 20.40.050-011 wording is human. | closed toward §2 | owner=human | write=no

M-010 | 20.40_ob_requirements.md, 20.40.050_idob_prim.md, 20.105_tp_requirements.md | HLR-20.40-017; 20.105 commit sentence; HLR-20.40.050-062 | Term mismatch: 20.40 OuBA freezes meaning into a Committed Thought Packet (CTP); 20.105 commit is TPU → OuBA → semantic_core; 20.40.050/20.105 CTP is a pre-RB hop (CTP-prm). | Same token, two meanings. | owner=human | write=no

M-010 decided 2026-08-30 | CTP = 20.145 primitive only (20.705 §2). HLR-20.40-017 NA. Remaining work is 20.40 wording. write=no until human edits.

M-011 | 20.40.050_idob_prim.md | HLR-20.40.050-011 | decided 2026-08-31 stamp=human toward 20.705 §2. Remaining 20.40.050-011 wording is human. | closed toward §2 | owner=human | write=no

M-012 | 20.32_cob_requirements.md | HLR-20.32-009 vs HLR-20.32-120 | Contradictory shalls: outputs exclusively to CIL vs snapshot consumed by CIL and CEx. | CIL vs CEx consumer is not one shall. | owner=human | write=no

Support-file drift:
M-013 | 20.40.060_ouba_prim.md, 20.40_ob_requirements.md | HLR-20.40.060-001, HLR-20.40-001 | Support file cites a hop this set does not allow: OuBA SHALL accept only meaning states that passed through IdOB; umbrella may route to OuBA without IdOB. | owner=human | write=no

M-014 | 20.40.060_ouba_prim.md, 20.105_tp_requirements.md | HLR-20.40.060-021, HLR-20.40.060-022, HLR-20.105-001 | Support file cites a hop this set does not allow: OuBA SHALL commit truth_evidence[] and tb_trace[] required by COB; TP forbids TB / Path-B semantics on TP. | owner=human | write=no

M-015 | 20.705_patha_pathb_flow.md, 20.40_ob_requirements.md, 20.40.050_idob_prim.md | HLR-20.40-016, HLR-20.40.050-012 | decided 2026-08-31 stamp=human toward 20.705 §2. Remaining 20.40.050-011 wording is human. | closed toward §2 | owner=human | write=no

M-016 | 20.705_patha_pathb_flow.md, 20.40.050_idob_prim.md | HLR-20.40.050-062 | decided 2026-08-31 stamp=human toward 20.705 §2. Remaining 20.40.050-011 wording is human. | closed toward §2 | owner=human | write=no

M-017 | 20.700_master_glossary.md, 20.40_ob_requirements.md | HLR-20.40-007 | Support file cites a hop this set does not allow: glossary “No semantic interpretation before SmOB” vs umbrella ban for all OB layers including SmOB. | owner=human | write=no

20.200 and folder README cited no hop this set forbids. No writers. No rewrites.

M-705-001 | 20.32_cob_requirements.md | HLR-20.32-054 | decided 2026-08-31 stamp=human as two CEx jobs | closed as two CEx jobs | owner=human | write=no

M-705-002 | 20.32_cob_requirements.md | HLR-20.32-111 | decided 2026-08-31 stamp=human: no mid-lineup COB meaning write | closed: no mid-lineup COB meaning write | owner=human | write=no

M-705-003 | 20.32_cob_requirements.md | HLR-20.32-112 | decided 2026-08-31 stamp=human: no mid-lineup COB meaning write | closed: no mid-lineup COB meaning write | owner=human | write=no

M-705-004 | 20.32_cob_requirements.md | HLR-20.32-120 | decided 2026-08-31 stamp=human as two CEx jobs | closed as two CEx jobs | owner=human | write=no

M-705-005 | 20.32_cob_requirements.md | HLR-20.32-124 | decided 2026-08-31 stamp=human as two CEx jobs | closed as two CEx jobs | owner=human | write=no

M-705-006 | 20.40.040_smob_prim.md | HLR-20.40.040-009 | §2 hop SmOB → WrdNm: SSG SHALL receive SmOB as its sole pre-semantic input, requiring SmOB → SSG and skipping WrdNm | Adjacent Path A consumer after SmOB is WrdNm, then ISc, then SSG | owner=human | write=no

M-705-007 | 20.40.040_smob_prim.md | HLR-20.40.040-038 | §2 hop SmOB → WrdNm: SmOB output SHALL be valid input for SSG and RB, requiring SmOB → SSG/RB and skipping WrdNm | Adjacent Path A consumer after SmOB is WrdNm, then ISc, then SSG | owner=human | write=no

M-705-008 | 20.40.050_idob_prim.md | HLR-20.40.050-011 | decided 2026-08-31 stamp=human toward 20.705 §2. Remaining 20.40.050-011 wording is human. | closed toward §2 | owner=human | write=no

M-705-009 | 20.105_tp_requirements.md | HLR-20.105-100 (unlabeled; CCR-carry shall before 101) | §3.6 hop CIL → CEx: CCR envelope is for downstream consumption by CEx-Pck, COB, CIL, and CST, reversing CIL → CEx and requiring CEx → COB | CEx-CCR cannot feed COB/CIL/CST on the same cycle as CIL → CEx; §3.6 ingest into COB/CST is OuBA → COB / OuBA → CSTCore | owner=human | write=no

M-705-010 | 20.105_tp_requirements.md | HLR-20.105-104 | §3.6 hop CIL → CEx: COB uses CEx-CCR selected_conversation to project into CIL, reversing CIL → CEx and requiring CEx → COB | Same-cycle CCR → COB → CIL runs after CEx but §3.6 is COB → CIL → CEx | owner=human | write=no

M-705-011 | 20.105_tp_requirements.md | HLR-20.105-106 | §3.6 hop CIL → CEx: COB reads TP.cex.ccr.selected_conversation and projects into CIL, reversing CIL → CEx and requiring CEx → COB | Same-cycle CCR → COB → CIL runs after CEx but §3.6 is COB → CIL → CEx | owner=human | write=no

M-705-012 | 20.105_tp_requirements.md | HLR-20.105-110 | §3.6 hop CIL → CEx: identical CCR output yields identical COB CIL projections, reversing CIL → CEx and requiring CEx → COB | Same-cycle CCR → COB → CIL runs after CEx but §3.6 is COB → CIL → CEx | owner=human | write=no

route:

R-001 | 20.37, 20.50, 20.145; drift 20.40.050, 20.15, 20.705 | HLR-20.37-023, HLR-20.37-071, HLR-20.37-072, HLR-20.050-027, HLR-20.050-049, HLR-20.050-069; drift HLR-20.40.050-012, HLR-20.40.050-062 | missing hop | TR `routing_fields{}` has no hop-type keys and RB’s only named destination is TR (`selected_ob_ids[]` untyped); nothing in the routing shalls names a typed structure-to-meaning hop into IdOB after committed RB, so the first S2M crossing cannot be scheduled as a typed route. | owner=human | write=no

R-002 | 20.51, 20.705 | HLR-20.051-007 vs 20.705 §2 as written | decided hop-order (20.145 + §2 win) | Hop-order is decided: CTP(20.145) immediately before RB on the full §2 string. | owner=human | write=no

R-002 remains hop-order (CTP before vs after RB), not “CTP is dead”. 20.145 stays live; do not retire the row.
R-002 decided 2026-08-30 | hop-order (20.145 +§2 win).

R-003 | 20.51; drift 20.15, 20.705, 20.145 | HLR-20.051-007 (vs informative header/§1/§2 sequences); HLR-20.145-028 | invented diagram route | 20.51’s header Downstream invents `TR → CTP → WrdNm` (skips RB); that file also shows three mutually different Path-A strings, none of which match HLR-20.051-007, so a router cannot take a single allowed route into IdOB from this slice. | owner=human | write=no

R-004 | 20.56, 20.37, 20.50 | HLR-20.056-011, HLR-20.056-014, HLR-20.050-032, HLR-20.37-023 | table vs TR vs RB/RBU vs CTP mismatch | The only routing-table schema is Path-B (`opbeh`/`obg`/`xlater`, keyed by `routing_epoch_id`, no TP paths, no TR/RB aliases) while Path-A S2M would have to be typed in unspecified `TP.TR.routing_fields{}` that RB consumes but is forbidden to bind to that table, so there is no lookup row for an efficient typed hop into IdOB. | owner=human | write=no

R-005 | 20.51, 20.145, 20.705 | HLR-20.051-007 vs §2 TR→CTP→RB | decided hop-order (20.145 + §2 win) | Hop-order is decided: CTP(20.145) immediately before RB on the full §2 string. | owner=human | write=no
R-005 decided 2026-08-30 | hop-order (20.145 +§2 win).

R-006 | 20.51, 20.705 | HLR-20.051-007 vs §2 TR→CTP→RB→IdOB | decided hop-order (20.145 + §2 win) | Hop-order is decided: CTP(20.145) immediately before RB; IdOB after that RB. | owner=human | write=no
R-006 decided 2026-08-30 | hop-order (20.145 +§2 win).

R-007 | 20.51, 20.705 | HLR-20.051-007 vs §2 RB→WrdNm | decided hop-order (20.145 + §2 win) | Hop-order is decided: RB→WrdNm vs RB→IdOB as §2 typed successors, not inverted CTP. | owner=human | write=no
R-007 decided 2026-08-30 | hop-order (20.145 +§2 win).

R-008 | 20.51, 20.705 | 20.51 Downstream header vs §2 TR→CTP→RB | decided hop-order (20.145 + §2 win) | Hop-order is decided: header no longer invents a skip of RB after CTP. | owner=human | write=no
R-008 decided 2026-08-30 | hop-order (20.145 +§2 win).

R-009 | 20.50, 20.705 | HLR-20.050-069, HLR-20.050-049 vs §2 RB→IdOB | decided hop-order (20.145 + §2 win); remains open: missing typed RB destination (20.50) | Hop-order decided; still open only because 20.50 does not SHALL IdOB as a typed RB destination. | owner=human | write=no
R-009 decided 2026-08-30 | hop-order (20.145 +§2 win). remains open only as missing typed RB destinations in 20.50.

R-010 | 20.50, 20.705 | HLR-20.050-069, HLR-20.050-049 vs §2 RB→IdOB | decided hop-order (20.145 + §2 win); remains open: missing typed RB destination (20.50) | Hop-order decided; remainder is 20.50, not 20.37: RB still lacks a typed hop into IdOB. | owner=human | write=no
R-010 decided 2026-08-30 | hop-order (20.145 +§2 win). remains open only as missing typed RB destinations in 20.50.

R-011 | 20.50, 20.705 | HLR-20.050-069, HLR-20.050-049 vs §2 RB→IdOB | decided hop-order (20.145 + §2 win); remains open: missing typed RB destination (20.50) | Hop-order decided; remainder is 20.50, not 20.145: RB still lacks a typed hop into IdOB. | owner=human | write=no
R-011 decided 2026-08-30 | hop-order (20.145 +§2 win). remains open only as missing typed RB destinations in 20.50.

R-012 | 20.37, 20.50, 20.705 | HLR-20.37-039, HLR-20.37-046, HLR-20.050-027 vs §2 DCB→TR / RTU→TR | conflicting hop (§2 DCB→TR / RTU→TR) | TR-gating SHALLs RB→TR whenever `tr_needs_update`, a hop §2 does not list (RB successors are WrdNm / IdOB / OuBA), so TR re-entry is not sequenced as §2 RTU→TR→CTP→RB→IdOB. | owner=human | write=no

R-013 | 20.50, 20.145, 20.705 | 20.50 (no CTP shall) vs HLR-20.145-028 vs §2 CTP→RB | missing hop (§2 CTP→RB) | RB never names CTP as immediate predecessor, so arbitration is not bound to the freeze hop §2 places immediately before every RB, including the RB that must enter IdOB. | owner=human | write=no

R-014 | 20.37, 20.145, 20.705 | 20.37 §6 / HLR-20.37-004 (RB consumes TP.TR) vs HLR-20.145-029 vs §2 TR→CTP | missing hop (§2 TR→CTP) | TR names only RB as consumer and never CTP, collapsing the mandatory TR→CTP hop that §2 inserts before every RB on the path into IdOB. | owner=human | write=no

R-015 | 20.56, 20.37, 20.50, 20.705 | HLR-20.056-011, HLR-20.056-014, HLR-20.050-032 vs §2 TR→CTP→RB→IdOB | table vs TR vs RB/RBU vs CTP mismatch | 20.56 epoch tables are Pipeline-B-only, SHALL NOT alias TR/RB, SHALL NOT carry TP paths, and Path A RB SHALL NOT read `routing_epoch_id`, so no table row can express the Path A typed hop into IdOB. | owner=human | write=no

R-016 | 20.50, 20.705 | HLR-20.050-021 / `selected_ob_ids[]` vs §2 RB→WrdNm | missing typed RB destination (20.50) | Remains open only as missing typed RB destination in 20.50: WrdNm is not a SHALL’d successor of the first/third RB. | owner=human | write=no
R-016 remains open 2026-08-30 | missing typed RB destinations in 20.50.

R-017 | 20.50, 20.705 | HLR-20.050-021 / `route_proposal` vs §2 RB→OuBA | missing typed RB destination (20.50) | Remains open only as missing typed RB destination in 20.50: OuBA is not a SHALL’d alternate RB exit. | owner=human | write=no
R-017 remains open 2026-08-30 | missing typed RB destinations in 20.50.

readme-bot:
matrix:

MX-001 | 20.200, README, 20.15_xlate_requirements.md, 20.15_ts_architecture_scaffold.md, 20.43_xlater_requirements.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix still keys 20.15 to a non-live XlateR filename; live 20.15 law is the architecture scaffold and live XlateR law is 20.43. | owner=human | write=no

MX-002 | 20.200, README, 20.30.080_resp_gen_sem.md, 20.30.080_rg_resp_gen_sem.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix RG row cites a filename that is not on disk; live RG law is 20.30.080_rg_resp_gen_sem.md. | owner=human | write=no

MX-003 | 20.200, README, 20.31_semantic_specification.md, 20.31_patha_meaning_spec.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix 20.31 row cites a non-live name; live Path A meaning law is 20.31_patha_meaning_spec.md. | owner=human | write=no

MX-004 | 20.200, README, 20.44_ts_isc_scoring.md, 20.45_ts_isc_scoring.md, 20.44_wrdnm_primitive.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix 20.44 still names ISC scoring; live 20.44 is WRDNM and live ISC law is 20.45_ts_isc_scoring.md. | owner=human | write=no

MX-005 | 20.200, README, 20.101_iiinb_requirements.md, 20.101_iiinb_prim.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix IIInB row cites `_requirements.md`; live IIInB law is 20.101_iiinb_prim.md. | owner=human | write=no

MX-006 | 20.200, README, 20.110_oub_requirements.md, 20.110_oubb_requirements.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix 20.110 still names OuB; live 20.110 law is OuBB (`20.110_oubb_requirements.md`). | owner=human | write=no

MX-007 | 20.200, README, 20.145_ctp_prm.md, 20.145_ctp_prim.md | HLR-20.200-002 | extra row for a file that moved or was renamed | Matrix CTP row cites `_prm.md`; live CTP law is 20.145_ctp_prim.md. | owner=human | write=no

MX-008 | 20.200, 20.30.070_rbu_mtp_sem.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix still traces RBU+MTP semantics to 20.30.070_rbu_mtp_sem.md, which has no live 20-series file of that name. | owner=human | write=no

MX-009 | 20.200, 20.45_imr_requirements.md, 20.45_ts_isc_scoring.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix IMR row cites 20.45_imr_requirements.md; that name is not live (live 20.45 is ISC scoring). | owner=human | write=no

MX-010 | 20.200, 20.58_oub_execution_manifold_integration.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix still traces an OuB execution-manifold doc that has no live 20-series file of that name. | owner=human | write=no

MX-011 | 20.200, 20.102_usp_requirements.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix USP row cites 20.102_usp_requirements.md; that name is not among live 20-series files. | owner=human | write=no

MX-012 | 20.200, 20.103_upi_requirements.md | HLR-20.200-002 | matrix row filename ≠ live file | Matrix UPI row cites 20.103_upi_requirements.md; that name is not among live 20-series files. | owner=human | write=no

MX-013 | 20.200, README, 20.40.050_idob_prim.md | HLR-20.200-002 | missing row for an authoritative module | IdOB is on the README auth list and live as 20.40.050_idob_prim.md, but 20.200 has no row for it. | owner=human | write=no

MX-014 | 20.200, README, 20.40.060_ouba_prim.md, 20.40.060.010_ouba_input_data_spec.md, 20.40.060.700_ouba_field_ref.md | HLR-20.200-002 | missing row for an authoritative module | OuBA and its two live input/field companions are on the README auth list; 20.200 has no OuBA rows (it still has stale OuB 20.110/20.58 names). | owner=human | write=no

MX-015 | 20.200, README, 20.47_ssg_prim.md | HLR-20.200-002 | missing row for an authoritative module | SSG is on the README auth list and live as 20.47_ssg_prim.md, but 20.200 has no row for it. | owner=human | write=no

MX-016 | 20.200, README, 20.15_ts_architecture_scaffold.md, 20.30.005_rtu_prim.md, 20.30.080_rg_resp_gen_sem.md, 20.30.085_rsg_prim.md, 20.30.090_rsg_mapping_rules.md, 20.31_patha_meaning_spec.md, 20.32.010.010_cst-core.md, 20.32.010.020_cst-ms.md, 20.32.010.030_cst-mux.md, 20.40.055_mcb_prim.md, 20.44_wrdnm_primitive.md, 20.45_ts_isc_scoring.md, 20.48.010_knc_prim.md, 20.48.020_knm_prim.md, 20.48.030_knf_prim.md, 20.49_stpx_prim.md, 20.52_ssr_data_packet.md, 20.53_rrw_process.md, 20.54_ssrgn_prim.md, 20.101_iiinb_prim.md, 20.105.010_tp_meta_fields.md, 20.105.020_tp_meta_provenance.md, 20.105.030_tp_meta_usage.md, 20.107.010_cex-ie_primitive.md, 20.107.020_cex-ccr_primitive.md, 20.107.030_cex-pck_primitive.md, 20.108.010_ce_candidate_set.md, 20.110_oubb_requirements.md, 20.110.010_oubb_stack.md, 20.112_li_prim.md, 20.113_cohi_prim.md, 20.145_ctp_prim.md, 20.155_trsch_prim.md | HLR-20.200-002 | missing row for an authoritative module | 33 further README-auth live modules have no 20.200 row under their live names, so the matrix does not cover current 20-series law for those modules. | owner=human | write=no

MX-017 | 20.200, README, 20.16_gb_responsibility_matrix.md, 20.18_failure_modes_and_success_criteria.md, 20.38_ts_implementation_guidelines.md, 20.39_ts_core_data_structures.md, 20.55_srp_requirements.md, 20.56_routing_table_schema.md, 20.57_trig_rb_semantic_trigger_requirements.md, 20.190_glossary.md, 20.205_execution_packet_xp_requirements.md | HLR-20.200-002 | README authoritative list ≠ matrix set | Nine live files are matrix rows but are not on `## Authoritative Requirement Files` (they sit on `## Directory index (coverage-aligned)` or `## Reference Documents`); auth list is 96 names, matrix is 79. | owner=human | write=no

MX-018 | 20.200 | HLR-20.200-001 | design-anchor TBD left as if current | 74 of 79 Design Anchor cells publish `50.*.md (TBD)` as the current design-anchor value, so placeholders are treated as live governance targets. | owner=human | write=no

MX-019 | 20.200, 20.705, 20.109_ie_prim.md | HLR-20.200-001; HLR-20.200-002; `[IE →](20.109_ie_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[IE →](20.109_ie_prim.md)`. | owner=human | write=no

MX-020 | 20.200, 20.705, 20.44_wrdnm_primitive.md | HLR-20.200-001; HLR-20.200-002; `[WrdNm →](20.44_wrdnm_primitive.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[WrdNm →](20.44_wrdnm_primitive.md)` (the 20.44 row is ISC, not WrdNm). | owner=human | write=no

MX-021 | 20.200, 20.705, 20.47_ssg_prim.md | HLR-20.200-001; HLR-20.200-002; `[SSG →](20.47_ssg_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[SSG →](20.47_ssg_prim.md)`. | owner=human | write=no

MX-022 | 20.200, 20.705, 20.49_stpx_prim.md | HLR-20.200-001; HLR-20.200-002; `[STPX →](20.49_stpx_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[STPX →](20.49_stpx_prim.md)`. | owner=human | write=no

MX-023 | 20.200, 20.705, 20.30.005_rtu_prim.md | HLR-20.200-001; HLR-20.200-002; `[RTU →](20.30.005_rtu_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[RTU →](20.30.005_rtu_prim.md)`. | owner=human | write=no

MX-024 | 20.200, 20.705, 20.40.050_idob_prim.md | HLR-20.200-001; HLR-20.200-002; `[IdOB →](20.40.050_idob_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[IdOB →](20.40.050_idob_prim.md)`. | owner=human | write=no

MX-025 | 20.200, 20.705, 20.40.055_mcb_prim.md | HLR-20.200-001; HLR-20.200-002; `[MCB →](20.40.055_mcb_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[MCB →](20.40.055_mcb_prim.md)`. | owner=human | write=no

MX-026 | 20.200, 20.705, 20.40.060_ouba_prim.md | HLR-20.200-001; HLR-20.200-002; `[OuBA (End of Path A)](20.40.060_ouba_prim.md)` | missing hop row vs 20.705 §2 | 20.200 has no row for the §2 hop `[OuBA (End of Path A)](20.40.060_ouba_prim.md)`. | owner=human | write=no

MX-027 | 20.200, 20.705, 20.32.010_cst_requirements.md | HLR-20.200-001; HLR-20.200-002; `[CST](20.32.010_cst_requirements.md)`; `OuBA --> CSTCore`; `COB --> CSTCore` | missing hop row vs 20.705 §3.6 | 20.200 has no row for the §3.6 CST hop (`OuBA --> CSTCore` / `[CST](20.32.010_cst_requirements.md)`). | owner=human | write=no

MX-028 | 20.200, 20.705, 20.40.060_ouba_prim.md | HLR-20.200-001; HLR-20.200-002; `OuBA --> COB`; `OuBA --> CSTCore` | missing hop row vs 20.705 §3.6 | 20.200 has no row for the §3.6 hops `OuBA --> COB` and `OuBA --> CSTCore`. | owner=human | write=no

MX-029 | 20.200, 20.705, 20.101_iiinb_requirements.md, 20.101_iiinb_prim.md | HLR-20.200-001; HLR-20.200-002; `[IIInB →](20.101_iiinb_prim.md)` | stale hop filename vs 20.705 §2 | The 20.200 row `20.101_iiinb_requirements.md` does not match the §2 hop `[IIInB →](20.101_iiinb_prim.md)` (live file is `20.101_iiinb_prim.md`). | owner=human | write=no

MX-030 | 20.200, 20.705, 20.44_ts_isc_scoring.md, 20.45_ts_isc_scoring.md | HLR-20.200-001; HLR-20.200-002; `[ISc →](20.45_ts_isc_scoring.md)` | stale hop filename vs 20.705 §2 | The 20.200 row `20.44_ts_isc_scoring.md` (scope ISC scoring) does not match the §2 hop `[ISc →](20.45_ts_isc_scoring.md)` (live file is `20.45_ts_isc_scoring.md`). | owner=human | write=no

MX-031 | 20.200, 20.705, 20.145_ctp_prm.md, 20.145_ctp_prim.md | HLR-20.200-001; HLR-20.200-002; `[CTP →](20.145_ctp_prim.md)` | stale hop filename vs 20.705 §2 | The 20.200 row `20.145_ctp_prm.md` does not match the §2 hop `[CTP →](20.145_ctp_prim.md)` (live file is `20.145_ctp_prim.md`). | owner=human | write=no

MX-032 | 20.200, 20.705, 20.107_cex_extract.md | HLR-20.200-001; `[CEx →](20.107_cex_extract.md)`; `CIL --> CEx` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.107_cex_extract.md` has design-anchor `50.107_cex_design.md (TBD)` while §2 hop `[CEx →](20.107_cex_extract.md)` / §3.6 `CIL --> CEx` is treated as current. | owner=human | write=no

MX-033 | 20.200, 20.705, 20.108_ce_envelope.md | HLR-20.200-001; `[CE →](20.108_ce_envelope.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.108_ce_envelope.md` has design-anchor `50.108_ce_design.md (TBD)` while §2 hop `[CE →](20.108_ce_envelope.md)` is treated as current. | owner=human | write=no

MX-034 | 20.200, 20.705, 20.46_tpu_req.md | HLR-20.200-001; `[TPU →](20.46_tpu_req.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.46_tpu_req.md` has design-anchor `50.046_tpu_design.md (TBD)` while §2 hop `[TPU →](20.46_tpu_req.md)` is treated as current. | owner=human | write=no

MX-035 | 20.200, 20.705, 20.40.010_sob_prim.md | HLR-20.200-001; `[SOB →](20.40.010_sob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.010_sob_prim.md` has design-anchor `50.040_sob_design.md (TBD)` while §2 hop `[SOB →](20.40.010_sob_prim.md)` is treated as current. | owner=human | write=no

MX-036 | 20.200, 20.705, 20.40.020_srob_prim.md | HLR-20.200-001; `[SROB →](20.40.020_srob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.020_srob_prim.md` has design-anchor `50.040_srob_design.md (TBD)` while §2 hop `[SROB →](20.40.020_srob_prim.md)` is treated as current. | owner=human | write=no

MX-037 | 20.200, 20.705, 20.40.030_cnob_prim.md | HLR-20.200-001; `[CnOB →](20.40.030_cnob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.030_cnob_prim.md` has design-anchor `50.040_cnob_design.md (TBD)` while §2 hop `[CnOB →](20.40.030_cnob_prim.md)` is treated as current. | owner=human | write=no

MX-038 | 20.200, 20.705, 20.40.040_smob_prim.md | HLR-20.200-001; `[SmOB →](20.40.040_smob_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.40.040_smob_prim.md` has design-anchor `50.040_smob_design.md (TBD)` while §2 hop `[SmOB →](20.40.040_smob_prim.md)` is treated as current. | owner=human | write=no

MX-039 | 20.200, 20.705, 20.44_ts_isc_scoring.md, 20.45_ts_isc_scoring.md | HLR-20.200-001; `[ISc →](20.45_ts_isc_scoring.md)` | TBD design-anchor on a 20.705 hop | The 20.200 ISC row `20.44_ts_isc_scoring.md` has design-anchor `50.044_isc_design.md (TBD)` while §2 hop `[ISc →](20.45_ts_isc_scoring.md)` is treated as current. | owner=human | write=no

MX-040 | 20.200, 20.705, 20.51_rbu_prim.md | HLR-20.200-001; `[RBU →](20.51_rbu_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.51_rbu_prim.md` has design-anchor `50.051_rbu_design.md (TBD)` while §2 hop `[RBU →](20.51_rbu_prim.md)` is treated as current. | owner=human | write=no

MX-041 | 20.200, 20.705, 20.106_dcb_requirements.md | HLR-20.200-001; `[DCB →](20.106_dcb_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.106_dcb_requirements.md` has design-anchor `50.106_dcb_design.md (TBD)` while §2 hop `[DCB →](20.106_dcb_requirements.md)` is treated as current. | owner=human | write=no

MX-042 | 20.200, 20.705, 20.37_thought_router_tr_specification.md | HLR-20.200-001; `[TR →](20.37_thought_router_tr_specification.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.37_thought_router_tr_specification.md` has design-anchor `50.037_tr_design.md (TBD)` while §2 hop `[TR →](20.37_thought_router_tr_specification.md)` is treated as current. | owner=human | write=no

MX-043 | 20.200, 20.705, 20.145_ctp_prm.md, 20.145_ctp_prim.md | HLR-20.200-001; `[CTP →](20.145_ctp_prim.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.145_ctp_prm.md` has design-anchor `50.145_ctp_design.md (TBD)` while §2 hop `[CTP →](20.145_ctp_prim.md)` is treated as current. | owner=human | write=no

MX-044 | 20.200, 20.705, 20.50_rb_requirements.md | HLR-20.200-001; `[RB →](20.50_rb_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.50_rb_requirements.md` has design-anchor `50.050_rb_design.md (TBD)` while §2 hop `[RB →](20.50_rb_requirements.md)` is treated as current. | owner=human | write=no

MX-045 | 20.200, 20.705, 20.32_cob_requirements.md | HLR-20.200-001; `OuBA --> COB`; `[COB → ](20.32_cob_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.32_cob_requirements.md` has design-anchor `50.032_cob_design.md (TBD)` while §3.6 hop `OuBA --> COB` / `[COB → ](20.32_cob_requirements.md)` is treated as current. | owner=human | write=no

MX-046 | 20.200, 20.705, 20.33_cil_requirements.md | HLR-20.200-001; `COB --> CIL`; `[CIL](20.33_cil_requirements.md)` | TBD design-anchor on a 20.705 hop | The 20.200 row `20.33_cil_requirements.md` has design-anchor `50.033_cil_design.md (TBD)` while §3.6 hop `COB --> CIL` / `[CIL](20.33_cil_requirements.md)` is treated as current. | owner=human | write=no
MX note 2026-08-30 | 20.145 stays a live module; do not retire the row. write=no

harness:

charter 2026-09-02 stamp=human | agent=Harness | label=Path A IdOB Rulechecker | GitHub label=ts-harness
scope: primitives/idob/ + testbenches/path_a/identity/ (idob_* only)
emit: H-* rows — pass, or fail with wall = Φ write | Φ vs E | routing_filter | packet schema | fixture miss
score: INV-M0 (20.12.010) and 20.116.020 — rich EEE is not birth; only IdOB may fill Φ; isolation fixtures legal (20.40.050-053)
write=no. Do not edit law, fixtures, 20.705, or 20.50. Do not clean 20.705. Do not create Catalog, Flow, Terms, or any other bot.
status: first report 2026-09-02 — H-001–H-008 pass (wall=none)
H-001 | idob_rulechecker.py, idob_testbench.py, idob_rules.yaml, idob_testbench.yaml, idob_tests_to_run.yaml, primitives/idob/idob.py | idob_output_001, idob_utterance_001, idob_packet_001, idob_write_boundary_001, idob_no_structural_001, idob_rank_map_001, idob_key_stable_001, idob_flags_001 | issue=pass (wall=none) | why it matters=baseline: all six enabled S2M fixtures clear every IdOB wall check | owner=human | write=no
H-002 | idob_s2m_04_unmapped, idob_s2m_05_miss; 20.12.010_inv_m0.md | HLR-20.12.010-001, HLR-20.12.010-002; INV-M0 cut (Φ vs E) | issue=pass (wall=none) | why it matters=pre-birth legal: Φ stays ⊥ (selected_group_id/meaning_semantics null) with utterance/structure present; richness of E is not treated as birth | owner=human | write=no
H-003 | idob_s2m_01_rock, idob_s2m_02_deadline, idob_s2m_03_sleepy; 20.12.010, 20.116.020 | HLR-20.12.010-001, HLR-20.116.020-003 | issue=pass (wall=none) | why it matters=Φ fill only via IdOB-prm (selected_group_id + six-axis meaning_semantics); CIE prime is after birth, not a substitute for B | owner=human | write=no
H-004 | idob_s2m_06_write_boundary; 20.116.020_ownership_rw.md | HLR-20.116.020-003; idob_write_boundary_001 | issue=pass (wall=none) | why it matters=process.routing_filter survives IdOB unchanged; routing_filter_mutated=false | owner=human | write=no
H-005 | idob_rules.yaml no_structural / no_routing_or_dcb; 20.116.020 | HLR-20.116.020-003; idob_no_structural_001 | issue=pass (wall=none) | why it matters=IdOB did not mutate structural/SSG fields or DCB geometric_state on enabled fixtures | owner=human | write=no
H-006 | idob_packet_001; primitives/idob/idob_s2m_packet.yaml | packet schema (resolution_status, ready_for_ouba, path_b_eligible, idob_complete + bools) | issue=pass (wall=none) | why it matters=tp.idob packet schema keys present and typed as required by the rulechecker | owner=human | write=no
H-007 | idob_testbench.yaml; 20.40.050_idob_prim.md | HLR-20.40.050-053 | issue=pass (wall=none) | why it matters=progressive isolation fixtures (utterance/card/packs/cie without live RB/RTU) remain legal and executed | owner=human | write=no
H-008 | 20.12.010 (coverage note); identity idob_* runner only | INV-M0 §2 attacker lineup (CE→CIL→SmOB→MCB) | issue=pass (wall=none) | why it matters=law already records those four attackers are not on this isolation runner; out of charter scope (idob_* only) — not a fixture miss here; full INV-M0 lineup assert is later Catalog/Harness work | owner=human | write=no


terms:

charter 2026-09-02 stamp=human (amended) | agent=Terms | label=Glossary / 20.700 | GitHub label=ts-terms
scope: 20.700 family only. write=no. Suggest-only T-*. Do not create Catalog or Flow. Do not change Harness.
jobs: (1) discrepancy vs associated requirements home (2) obsolete terms; keep-in-place=yes; do not delete headings
Job 1: for each 20.700.xxx entry, compare Purpose/Focus/When/Why/Is not/Example/Normative home to the live home named in that entry; also 20.116 series, 20.12.010 INV-M0, 20.145 CTP-prm only, 20.40 v1.3, Clusters 1–3, 20.705 §2/§3.6 as hop trackers only. Classes: token collision | missing row | stale freeze/CTP | cue named as birth | sole-writer erases 20.116.020 walls | When/hop order ≠ home shall or §2 | Normative home non-live filename.
Job 2: obsolescence first-class — stale (name live, definition wrong) | NA/superseded (use dead; keep heading; Purpose states removal; home points at winner) | empty (heading with no required fields / no requirements home; block; do not fill). Keep-in-place default. Do not mark NA only because Path A unused this week.
row: T-nnn | 20.700.xxx file(s) | home file + live winner or none | class=discrepancy|stale|NA|superseded|empty|missing|collision|cue-as-birth | keep-in-place=yes|n/a | issue=<one line> | suggested Purpose/When/home line only | owner=human | write=no
If nothing new after T-001–T-009: T-000 | none.
write=no. Do not edit 20.700, 20.190, 20.116, 20.705, playground, fixtures, or shalls.
status: charter amended 2026-09-02; awaiting T-010+ or T-000 | none
T-001 | 20.700.010_primitives_glossary.md, 20.145_ctp_prim.md | HLR-20.145-028, HLR-20.145-029, HLR-20.145-030; Helm CTP=20.145 only | stale freeze/CTP: glossary CTP-prm still “Collect/Consolidate Thought Point” — “Collect all IdOB-outputs from an IdOB-set… After an IdOB-set completes… runs only after all parallel IdOB-prm instances finish”; example `…→RB→OB1…OBn→CTP→RB` | Law freezes TP as-is immediately before every RB (`TR→CTP→RB`), even when IdOB has not run; SHALL NOT wait for IdOB or combine multi-IdOB outputs. Glossary still teaches the superseded post-IdOB consolidation mode 20.145 marked NA | owner=human | write=no
T-002 | 20.700.020_processes_glossary.md, 20.145_ctp_prim.md | HLR-20.145-028, HLR-20.145-030; Helm CTP=20.145 only | stale freeze/CTP: Path A process block cycles `OB₀→RB→{OB₁…OBₙ}→CTP→RB` and example “CTP merges them into a single TP snapshot” | Same live distance: CTP named as merge/consolidation after OB-set, not as the 20.145 pre-RB policy-freeze hop; OuBA commit is correctly not called CTP here, but CTP’s own meaning is still wrong | owner=human | write=no
T-003 | 20.700.010_primitives_glossary.md (TrSch-prm + CTP-prm), 20.145_ctp_prim.md, 20.116.020_ownership_rw.md | HLR-20.145-028/029/030; 20.116.020 §4 `TR→CTP→RB→IdOB` | token collision: TrSch Purpose/When/Example bind CTP to “consolidated IdOB-output packet” / “after CTP-prm consolidates the outputs of an IdOB-set” | Same token CTP used as IdOB consolidator feeding TrSch, vs law stretch where CTP precedes RB and can precede first IdOB; schedulers reading glossary will place CTP on the wrong side of IdOB | owner=human | write=no
T-004 | 20.700_master_glossary.md, 20.700.010–.050, glossary_term_registry.json, 20.12.010_inv_m0.md, 20.116.030_name_separations.md | HLR-20.12.010-001/002; INV-M0 Φ/B/E/cut; 20.116.030 utterance≠stand-in M | missing row: no 20.700 entries for INV-M0 / meaning-birth / stand-in M / Φ (`selected_group_id`, `meaning_semantics`) / “the cut” / CIE; zero hits for birth, stand-in, INV-M0, CIE across 20.700* | Law birth vocabulary and cue≠birth separations have no glossary home, so Terms cannot convict cue-as-birth from the glossary alone | owner=human | write=no
T-005 | 20.700.010 (OuBA/SSRGn/IE freeze wording), 20.145_ctp_prim.md, 20.116.020, 20.116.030 | HLR-20.145-008, HLR-20.145-031; 20.116.030 ready_for_ouba≠OuBA freeze; 20.116.020 CTP owns `cognitive_history[]` | missing row: glossary never names CTP “policy freeze” nor separates it from OuBA/SSRGn meaning freeze; also no row for CTP-owned `TP.metadata.cognitive_history[]` | Freeze token is taught as OuBA/SSRGn commit freeze only; law’s CTP policy-freeze vs OuBA freeze (and flag≠exit) lack glossary anchors | owner=human | write=no
T-006 | 20.700_master_glossary.md, 20.12.010_inv_m0.md, 20.116.020 | HLR-20.12.010-001; HLR-20.116.020-003; INV-M0 SmOB∈cues; Helm M-017 still live in text | cue named as birth: invariant “Pre-Semantic Boundaries: No semantic interpretation before SmOB” | Positions SmOB as the semantic-interpretation threshold; INV-M0/20.116: SmOB is cue, birth/Φ write is IdOB-prm only — glossary still invites treating SmOB (or post-SmOB cue hops) as meaning birth | owner=human | write=no
T-007 | 20.700.050_ts_level_concepts_glossary.md (OB class), 20.12.010_inv_m0.md, 20.116.020 | HLR-20.12.010-001; HLR-20.116.020-003; INV-M0 IdOB-only B | cue named as birth: OB class lists “(SOB, SROB, CnOB, SmOB, IdOB)” that “emit … cues … without performing semantic interpretation” and “Is not: … an identity-conditioned primitive” | Lumps IdOB (sole birth writer) into the cue/structure OB class and denies the identity-conditioned/semantic job INV-M0 assigns only to IdOB — cue class named as if it covered birth | owner=human | write=no
T-008 | 20.700.050_ts_level_concepts_glossary.md (FFTM), 20.12.010_inv_m0.md, 20.116.030 | INV-M0 E≠Φ / richness≠birth; 20.116.030 utterance≠stand-in M | cue named as birth: FFTM “Canonical Path-A meaning representation” / “meaning construction before any basin” / “ensures Path-A meaning is structurally complete prior to downstream processing” | Treats pre-basin token structure as completed meaning; law says carrier/structure occupancy is E, not birth of stand-in M on Φ | owner=human | write=no
T-009 | 20.700_master_glossary.md, 20.700.010 (CTP/TPU wording), 20.116.020_ownership_rw.md | HLR-20.116.020-003; 20.116.020 table (IdOB `TP.idob`; CTP `cognitive_history[]`; MCB `next_context`) | token collision: master “Single-Writer Rule: TPU is the only primitive allowed to modify TP in Path A” (also A/B “TPU is sole writer”; CTP entry “TPU is sole writer”) | Field-name authority 20.116.020 authorizes IdOB/CTP/MCB envelope writes; glossary sole-writer token erases those walls and contradicts ownership law the Terms charter must track | owner=human | write=no

needs human:
S1 S2 S3 S4 E1 E2 M-001–M-017 M-705-001–M-705-012 R-001–R-017 MX-001–MX-046 (no stamp; owner=human; write=no)
next recommendation: not yet
