# EVENT template

EVENT: doc-change
when:
files:
what:
why:
expect:
kind: law | view
stamp: human

---

EVENT: policy

when: 2026-08-30

files: thought_simulator/requirements_20/20.705_patha_pathb_flow.md (§2, §3.6 only)

what: Human declares 20.705 Section 2 the Path A primitive-flow tracker and Section 3.6 the conversation-layer tracker (OuBA/COB/CST/CIL). All other 20.705 sections are historical; do not score against them; do not clean them.

why: We use those two sections to keep Path A / conversation integration in view while requirements catch up.

expect:

  - Spine, Meaning, Route, Matrix: report distance of controlled shalls to 20.705 §2 (Path A hops) or §3.6 (OuBA→COB/CST/CIL/CEx only). Cite shall ids vs the specific hop in §2 or §3.6.

  - Ignore 20.705 §1 claim of “reference-only” for scoring. Ignore §3.1–3.5, §4+, chat residue in 20.705.

  - write=no. Do not edit 20.705, 20.15, 20.31, 20.40.*, 20.32, or any shall to “make them agree.”

  - Do not treat Meaning preambles or 20.705 §3.3–3.5 as the pipeline.

  - Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “flow-tracker = 20.705 §2 and §3.6.” Do not create Bots. Do not start a cleanup of 20.705.

kind: law-tracker

stamp: human

---

EVENT: decision

when: 2026-08-30

files: 20.40_ob_requirements.md (HLR-20.40-017 and any CTP wording); 20.145; 20.705 §2

what: CTP means only the 20.145 primitive (Path A hop in 20.705 §2). HLR-20.40-017 is NA. Strip CTP from 20.40 family text. OuBA commit is not called CTP.

why: Same name, two functions. Tracker and 20.145 keep the hop; umbrella used the acronym for freeze.

expect:

  - Meaning: mark M-010 decided in this direction; remaining work is 20.40 wording, write=no until human edits.

  - Route: R-002 stays a hop-order issue (CTP before vs after RB), not a “CTP is dead” issue.

  - Matrix: 20.145 stays a live module; do not retire the row.

  - Helm: note in LATEST.md. Do not edit 20.40. Do not create writers.

kind: law

stamp: human

---

EVENT: doc-change

when: 2026-08-30

files:

  thought_simulator/requirements_20/20.116_field_catalog.md

  thought_simulator/requirements_20/20.116.010_tp_envelope_index.md

  thought_simulator/requirements_20/20.116.020_ownership_rw.md

  thought_simulator/requirements_20/20.116.030_name_separations.md

  thought_simulator/requirements_20/system_playground/design/pipeline/00_field_catalog_authority.md

  thought_simulator/requirements_20/20.705_field_catalog_authority.md

  thought_simulator/requirements_20/system_playground/primitives/idob/

  thought_simulator/requirements_20/system_playground/testbenches/path_a/identity/

what: 20.116 series is now the Path A authority for field names, paths, and owners. Primitive files still own behavior. patha_field_names.md and the transfer tables are derived working indexes; sidecars state that. Live IdOB hop/testbench files carry a 20.116 authority note. 20.705 body was not rewritten.

why: Stop name/path drift. Playground dictionaries must not override 20.116.

expect:

  - Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “field-name authority = 20.116 series.”

  - write=no on 20.116 unless the human opens a catalog amendment.

  - Do not treat patha_field_names.md as the winner on a name collision.

  - Do not create Bots. Do not start a rewrite of 20.705 or patha_field_names.md.

kind: law

stamp: human

---

EVENT: decision

when: 2026-08-30

files: 20.40.050_idob_prim.md; 20.40_ob_requirements.md; 20.51_rbu_prim.md; 20.50_rb_requirements.md; 20.145_ctp_prim.md; 20.705 §2

what: Cluster 1 — IdOB invoke and stretch. Winner is HLR-20.40.050-062 and 20.705 §2. Live identity-conditioned Path A stretch is WrdNm → ISc → RTU → TR → CTP → RB → IdOB → MCB → RBU. HLR-20.40.050-011 (invoke only after RB→RTU) is NA. 20.40 umbrella SOB→SROB→CnOB→SmOB is the structural OB chain, not the S2M schedule. IdOB is the post-RB hop when RB selects S2M. RB→OuBA is a legal OR-exit and may skip IdOB. Isolation fixtures stay legal. GB→IdOB is not Path A. IdOB→TR→OuBA is not the successor; successor is IdOB→MCB→RBU. 20.51 TR→RB→CTP and TR→RB→IdOB yield to 20.145 + §2 (TR→CTP→RB then RB→IdOB). Typed RB destinations remain later 20.50 wording.

why: One invoke hop. Stop scoring IdOB as an optional SOB peer and as a post-RB hop at the same time.

expect:

  - Meaning: mark M-009, M-011, M-015, M-016, M-705-008 decided in this direction. write=no until human edits 20.40.050-011 wording.

  - Route: mark R-002, R-005 through R-011 decided as hop-order (20.145 +§2 win). R-009 through R-011, R-016, R-017 remain open only as missing typed RB destinations in 20.50.

  - Helm: note in LATEST.md. Do not edit 20.40, 20.50, 20.51, or 20.705. Do not create writers or Bots.

kind: law

stamp: human

---

EVENT: decision

when: 2026-08-30

files: 20.40_ob_requirements.md; 20.40.050_idob_prim.md; 20.105_tp.md; 20.116.020_ownership_rw.md

what: Cluster 2 — meaning-write law. Winner is 20.116.020-003, HLR-20.105-116, and IdOB-prm. Only IdOB-prm may birth stand-in M, TP.idob, and TP.semantic.meaning_delta_h (plus listed root flags). 20.40 umbrella “no semantic interpretation” on 20.40.010–.060 does not apply to IdOB-prm. It means SOB/SROB/CnOB/SmOB must not produce M. Child MAY-read of CE/CIL/discourse is cues only, not a second meaning writer. TP write wall stands; exceptions remain TPU, OuBA freeze, and listed IdOB paths.

why: Umbrella and IdOB cannot both be the meaning writer. Read is not write.

expect:

  - Meaning: mark M-001 decided. Mark M-002 narrowed (read ≠ write). Remaining work is 20.40 umbrella wording. write=no until human edits.

  - Helm: note in LATEST.md. Do not edit 20.40 or 20.105. Do not create writers or Bots.

kind: law

stamp: human

---

EVENT: decision

when: 2026-08-30

files: 20.15_ts_architecture_scaffold.md; 20.32_cob_requirements.md; 20.105_tp.md; 20.206; 20.705 §2 and §3.6; 20.116.020_ownership_rw.md

what: Cluster 3 — OuBA door and conversation polarity. Winner is 20.15 §2.14 and 20.116: OuBA freeze is the sole COB meaning-ingest door. COB long-horizon meaning and importance arrive only from that freeze (slim TP.idob, flags, pack_ids, utterance), not from mid-lineup SmOB→COB or IdOB→COB. CST-Core/MS → COB are stability command / freeze-thaw paths, not meaning ingest. USP remains CIL-only. Path A CEx after IE and CIL→CEx are two jobs: extract vs conversation-layer on the COB snapshot. CIL→CEx selects conversation. COB does not select. COB projects after freeze, not from live CEx-CCR on the same Path A beat. Path B still starts OuBA → B.

why: One meaning door into COB. Do not score Path A extract and conversation CEx as one reversed hop.

expect:

  - Spine: mark E2 decided (command vs ingest). Leave S1 and S3 open as 20.206 wording, not as a new door.

  - Meaning: mark M-005, M-705-002, M-705-003 decided (no mid-lineup COB meaning write). Mark E1 / M-008 / M-705-001 / M-705-004 / M-705-005 decided as two CEx jobs.

  - Helm: note in LATEST.md. Do not edit 20.15, 20.32, 20.105, 20.206, or 20.705. Do not create writers or Bots.

kind: law

stamp: human

---

EVENT: doc-change

when: 2026-08-30

files: thought_simulator/requirements_20/20.40_ob_requirements.md

what: Human landed 20.40 v1.3. HLR-20.40-017R is gone. Freeze SHALL is HLR-20.40-019 (previous max was 018). HLR-20.40-017 stays NA. HLR-20.40-003 / 007 / 008 now bind SOB, SROB, CnOB, and SmOB only. IdOB-prm may read CE/CIL/discourse as cues and write the 20.116.020 / 20.40.050 envelopes. Informative §3 / §5 / §6 have no SHALL and no HLR numbers. Score the live file, not the pre-correction pass.

why: Cluster 2 remaining umbrella wording is on main. Bots must not keep scoring 017R or family-wide 003/007/008.

expect:

  - Meaning: mark M-001 and M-002 decided against 20.40 v1.3. Cluster 2 “remaining 20.40 wording” is done.

  - Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “20.40 v1.3; freeze = HLR-20.40-019; 003/007/008 = SOB–SmOB only.”

  - write=no on 20.40 unless the human opens another edit.

  - Do not restore 017R. Do not create Bots or writers.

kind: law

stamp: human
