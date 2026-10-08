# Six structure IDs

**Date:** 2026-10-08
**Status:** named and absent. No key. No invention.

Front door: [README.md](README.md). Source of the six names: `primitives/idob/idob_s2m_packet.yaml`. Rule: `HLR-20.40.050-056`. A structural key is formed only from all six.

| ID | Floor source in the short sim | State |
|---|---|---|
| `semantic_field_id` | none | absent |
| `semantic_role_id` | none | absent |
| `semantic_object_id` | none | absent |
| `gradient_id` | none | absent |
| `universe_id` | none | absent |
| `subfield_id` | none | absent |

SOB, SROB, CnOB, and SmOB emit segments, roles, constraints, and smoothing. They do not emit these IDs. The shell writes each as null. `structural_key` stays null. A later pass may source an ID only from a floor field that already exists, with a replay. It may not invent one.
