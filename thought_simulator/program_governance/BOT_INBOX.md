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

---

EVENT: decision

when: 2026-08-31

files: 20.31_patha_meaning_spec.md; 20.40.010_sob_prim.md; 20.40.020_srob_prim.md; 20.40.030_cnob_prim.md; 20.40.040_smob_prim.md; 20.40.050_idob_prim.md; 20.105_tp.md; 20.116.020_ownership_rw.md

what: IdOB-prm is the sole producer of TP.semantic.importance. SOB / SROB / SmOB / CnOB may compute local envelope importance for their own structural envelopes. They shall not write TP.semantic.importance. Routing uses structure fields only, not global importance. This is new stamped law. It does not invent hops, fields, or primitives. It does not reopen 20.40 v1.3 or HLR-20.40-019. Path B stays active.

why: Global importance and local envelope importance were being scored as if SOB/SROB owned the TP field. One writer. Local envelope math stays local.

expect:

  - Meaning: mark global-importance ownership as IdOB-prm only. Local envelope importance on SOB/SROB/SmOB/CnOB is not a write of TP.semantic.importance.

  - Route: do not route on TP.semantic.importance. Score structure fields only.

  - Matrix: do not add a new hop row for importance. Inventory only when the wording PR lands.

  - Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “TP.semantic.importance writer = IdOB-prm only; routing = structure fields.” Do not edit requirement files. Do not create Bots or writers.

kind: law

stamp: human

---

EVENT: doc-change

when: 2026-08-31

files:

  thought_simulator/requirements_20/20.31_patha_meaning_spec.md

  thought_simulator/requirements_20/20.40.010_sob_prim.md

  thought_simulator/requirements_20/20.40.020_srob_prim.md

  thought_simulator/requirements_20/20.40.030_cnob_prim.md

  thought_simulator/requirements_20/20.40.040_smob_prim.md

  thought_simulator/requirements_20/20.40.050_idob_prim.md

  thought_simulator/requirements_20/20.50_rb_requirements.md

  thought_simulator/requirements_20/20.51_rbu_prim.md

  thought_simulator/requirements_20/20.32_cob_requirements.md

  thought_simulator/requirements_20/20.105_tp.md

  thought_simulator/requirements_20/20.116_field_catalog.md

  thought_simulator/requirements_20/20.145_ctp_prim.md

  thought_simulator/requirements_20/20.200_traceability_matrix.md

  thought_simulator/requirements_20/20.206_pipeline_a_b_synchronization_contract.md

what: Human opened a single wording-only alignment pass. Work is off main, one branch / one PR. Live files must be made to say the same hops, writers, and ingest-door semantics already stated by 20.15, 20.705 §2 (verbatim, not shortened), 08-30 / 08-31 stamped winners, and the 08-31 importance decision. Constraints for that PR: no new hops; no new primitives; no §2 shortening; no reopen of 20.40 v1.3 or HLR-20.40-019; no Path-B deletion or “inactive” declaration; do not rewrite 20.200 hop rows MX-001–046 (inventory / stale filenames / missing modules only). Informative statements receive neither SHALL nor an HLR number. Do not remove information; correct, rearrange, reword, or add. Every new SHALL receives an HLR of the live per-document series, next = max existing + 1.

why: Score live wording against already-stamped law. Keep main untouched until the human accepts the PR.

expect:

  - Helm: add this EVENT to CHANGE_LOG. In LATEST.md note “Path-A wording alignment in one off-main PR; write=no on main requirement files until merge.”

  - write=no on main copies of the files listed above. Do not land edits on main from bots.

  - Score 20.705 §2 verbatim. Do not treat a shortened chain (e.g. CTP→RB→RTU→IdOB→OuBA→COB/CST) as law.

  - Do not create Bots. Do not start a 20.705 cleanup. Do not declare Path B inactive.

kind: view

stamp: human
---

EVENT: policy

when: 2026-09-02

files:

  thought_simulator/requirements_20/20.700_master_glossary.md

  thought_simulator/requirements_20/20.700.010_primitives_glossary.md

  thought_simulator/requirements_20/20.700.020_processes_glossary.md

  thought_simulator/requirements_20/20.700.030_reference_objects_glossary.md

  thought_simulator/requirements_20/20.700.040_governance_glossary.md

  thought_simulator/requirements_20/20.700.050_ts_level_concepts_glossary.md

  thought_simulator/program_governance/BOT_REPORTS/LATEST.md

  thought_simulator/program_governance/CHANGE_LOG.md

what: Amend the live Terms charter. Do not create a new bot. Do not create Catalog or Flow. Do not change Harness.

Terms remains: Glossary / 20.700 family only. GitHub label ts-terms. write=no. Suggest-only T-*. Empty terms: block.

Terms has two jobs on every run.

Job 1 — discrepancy vs associated requirements
For each 20.700.xxx entry, compare Purpose / Focus / When / Why / Is not / Example / Normative home to the live home named in that entry. Also compare to stamped law: 20.116 series, 20.12.010 INV-M0, 20.145 CTP-prm only, 20.40 v1.3, Clusters 1–3, 20.705 §2 / §3.6 as hop trackers only.
Emit T-* when glossary and home disagree. Classes: token collision; missing row; stale freeze/CTP; cue named as birth; sole-writer text that erases 20.116.020 envelope walls; When/hop order mismatch vs home shall or 20.705 §2; Normative home pointing at non-live filename. Suggested edit only.

Job 2 — obsolete glossary terms
Obsolescence is first-class. Statuses: stale | NA/superseded | empty. Keep-in-place default; do not recommend deleting headings. Do not mark NA only because Path A is unused this week.

Row format: T-nnn | 20.700.xxx file(s) | home file + live winner or none | class=discrepancy|stale|NA|superseded|empty|missing|collision|cue-as-birth | keep-in-place=yes|n/a | issue=<one line> | suggested Purpose/When/home line only | owner=human | write=no
If nothing new after T-001–T-009: T-000 | none.

why: Glossary is a restatement of live homes, not a second source of truth. Charter must score every entry against its home document and keep obsolete names visible as NA/superseded.

expect:
  - Helm: CHANGE_LOG line as specified; LATEST terms: amended charter; keep T-001–T-009; jobs line; run Terms once from T-010 or T-000 | none
  - write=no. Do not edit 20.700, 20.190, 20.116, 20.705, playground, fixtures, or shalls
  - Do not create Catalog, Flow, hop-bots, or writers
  - Human stamp only for glossary patches off main via PR

kind: law

stamp: human

---

EVENT: policy

when: 2026-09-03

files: thought_simulator/program_governance/ (Helm bot roster); 20.705_patha_pathb_flow.md

what: Create Grokbot Flow. Then run Flow once.

why: Terms owns 20.700. Nothing currently emits suggested edits to the hop tracker itself.

expect:
  - Create agent=Flow | label=Hop tracker / 20.705 | GitHub label=ts-flow | write=no
  - Scope ONLY: 20.705 §2 (Path A string), §3.6 (A→B + conversation), §5 (OpBeh→OBG→XlateR→XP). Ignore §1 “reference-only”, §3.1–3.5, §4+, chat residue.
  - Job: for each hop in those sections, compare to the live primitive file named on that hop (basename must exist under requirements_20/). Classes: hop-order ≠ live When | dead basename | OuB≠OuBB | CTP≠20.145 | Path B start ≠ TPTB | KnC skips SSRGn | CST as one family not three hops unless 20.705 lists Core/MS/Mux | cue named as Φ birth.
  - Emit F-001… or F-000 | none. Row: F-nnn | 20.705 section | live home file | class=… | issue=<one line> | suggested hop-line only | owner=human | write=no
  - Do NOT edit 20.705, 20.700, 20.40, 20.116, playground, or shalls. Do NOT create Catalog/Terms/Harness work. Do NOT invent HLRs.
  - After create, RUN Flow once. Append F-* to BOT_REPORTS/LATEST.md and today’s dated file. Stamp CHANGE_LOG “Flow created + first scan 2026-09-03”.
  - Cadence later: on EVENT that touches 20.705 or human ask; else weekly F-000 | none. Do not schedule a second run from this EVENT.

kind: law-tracker

stamp: human

---

EVENT: policy

when: 2026-09-03

files: thought_simulator/program_governance/; 20.116.020_ownership_rw.md; 20.116.030_name_separations.md; 20.700.010–.050

what: Create Grokbot Catalog. Then run Catalog once.

why: Need a 20.116-wall scorer so Terms is not the only reader of sole-writer / cue≠Φ.

expect:
  - Create agent=Catalog | label=Field catalog walls / 20.116 | GitHub label=ts-catalog | write=no
  - Scope: 20.116.020 ownership table + 20.116.030 name separations, scored against 20.700.010/.020/.030/.050 entries that name those fields. Also 20.12.010 INV-M0 cut (Φ vs E) as a named law, not a new paper.
  - Job: emit C-* when glossary or a cited home: (1) names a non-IdOB writer for TP.semantic.importance or Φ/stand-in M (2) treats IE/utterance/FFTM/richness as meaning-birth (3) treats ready_for_ouba as OuBA freeze (4) assigns USP to COB (CST-Mux wall) (5) token collision with 20.116 path. Keep-in-place=yes. Do not delete headings.
  - Emit C-001… or C-000 | none. Row: C-nnn | 20.700.xxx or home file | 20.116 shall or INV-M0 id | class=sole-writer|cue-as-birth|name-collision|freeze-token | issue=<one line> | suggested Purpose/When/home line only | owner=human | write=no
  - Do NOT edit any requirement or glossary file. Do NOT create Flow work. Do NOT add missing glossary rows (T-004–T-009 stay human).
  - After create, RUN Catalog once. Append C-* to LATEST.md and today’s dated file. Stamp CHANGE_LOG “Catalog created + first scan 2026-09-03”.
  - Cadence later: on EVENT that touches 20.116 / INV-M0 / 20.700 or human ask; else weekly C-000 | none. Do not schedule a second run from this EVENT.

kind: law-tracker

stamp: human

---

EVENT: policy

when: 2026-09-03

files: 20.700 family on main (post T-028–T-041 merge)

what: Run Terms once. Do not create a new bot.

why: Glossary punch list is on main; need T-000 | none or leftovers only.

expect:
  - Do not re-emit T-001–T-041 unless the live heading still mismatches the already-applied When/home/Purpose.
  - Prefer T-000 | none. New ids start at T-042.
  - write=no. Do not edit files. Do not run Flow or Catalog from this EVENT.

kind: view

stamp: human

---

EVENT: doc-change

when: 2026-09-03

files: thought_simulator/requirements_20/20.705_patha_pathb_flow.md

what: Human applied Flow F-001–F-003 on main. §3.6 validation links use 20.32.010.010_cst-core.md and 20.32.010.020_cst-ms.md (no parent 20.32.010_cst_requirements.md). §5.2 is XP → LI → REx → RPlan → RPU → ReB → OuBB.

why: Tracker now matches live CST files and RPU→ReB→OuBB When.

expect:
  - Helm: CHANGE_LOG + LATEST.md note “F-001–F-003 applied 2026-09-03 stamp=human.”
  - Flow: mark F-001 F-002 F-003 closed. Do not re-emit them. Next Flow emit starts at F-004 or F-000 | none.
  - Do not run Flow, Catalog, or Terms from this EVENT.
  - write=no. Do not edit 20.705 again.

kind: law

stamp: human

