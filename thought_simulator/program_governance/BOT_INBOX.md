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

files: 20.40_ob_requirements.md, 20.51_rbu_prim.md

what: Hop order aligned to 20.705 §2. CTP (20.145) sits immediately before RB. IdOB after that RB. OuBA is the alternate RB exit.

expect: Route close R-002 toward §2. Meaning close M-009 toward 20.40-001/016. M-011 still open until 20.40.050-011 is NA’d. write=no on further files.

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
