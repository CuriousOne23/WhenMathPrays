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
