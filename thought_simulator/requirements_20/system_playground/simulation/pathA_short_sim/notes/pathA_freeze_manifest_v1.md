# Path-A Short Simulator - Version 1.0 (Frozen)

Freeze Gate: R9
Date: 2026-09-23

## Frozen Pipeline

CTP -> IdOB -> PSC -> MCB -> OuBA -> R7 -> R8

## Frozen Packet Schema

identity_geometry: str
truth_relation: str
truth_relation_family: str
semantic_core: dict
selected_ops: list
claimed_fields: list
contributors: list
contributions: list[dict]
activation_set: list
inactive_objects: list
residual_activated: bool
overlap_events: list
meaning_delta: dict
psc_violations: list
registry_digest: str
complete: bool
tru_hint: str

## Frozen Debugger Contract

- Debugger is observer only.
- Values in logs remain literal-eval safe.
- Debugger output includes IdOB Space Summary only for IdOB packet introspection.
- Debugger does not consume MCB, OuBA, R7, or R8 blocks.

## Frozen IdOB Families

- copular_state
- locative
- mixed_descriptive
- interrogative_wh
- interrogative_polar
- residual_identity
- agent_action
- modifier_resolution

## Frozen Supported Sentence Families

- Copular / State
- Locative
- Mixed Descriptive
- Interrogative
- Mixed Interrogative

## Recovery Instructions

To recover Version 1.0:
1. Checkout the freeze tag: git checkout pathA_v1_freeze
2. Restore notes/pathA_freeze_manifest_v1.md
3. Restore all files listed in the manifest
4. Re-run run_examples.py and pathA_dbug.py to confirm stability

## Freeze File List

- run_examples.py
- pathA_dbug.py
- tp_substrate.py
- idob/*
- psc.py
- mcb/seam.py
- ouba/assembly.py
- support/idob_objects.yaml
- support/idob_packet.v1.schema.json
- notes/pathA_supported_sentences.md
- support/tools/ouba_stability_check.py
- support/tools/pipeline_readiness_check.py

## Notes

- The file list above preserves the requested freeze references verbatim.
- In this repository layout, IdOB object specs are stored as support/idob_objects/*.yaml and schema files are under support/idob_schemas/.
