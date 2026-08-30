# primitives/idob — production hop

> **Field catalog authority (20.116).** Canonical paths, envelope owners, and name-separations: [`../../../20.116_field_catalog.md`](../../../20.116_field_catalog.md) · [`../../../20.116.010_tp_envelope_index.md`](../../../20.116.010_tp_envelope_index.md) · [`../../../20.116.020_ownership_rw.md`](../../../20.116.020_ownership_rw.md) · [`../../../20.116.030_name_separations.md`](../../../20.116.030_name_separations.md). Collision: 20.116 wins names/paths/owners; this hop wins behavior.

`idob.py` is a **separate file** from `11_idob_core/idob.py`. Same algorithm. No import of 11.

YAML this module opens (all in this directory):

| File | Role |
|------|------|
| `structure_card.examples.yaml` | Cards |
| `meaning_groups.yaml` | Prototypes |
| `struct_to_meaning_map.yaml` | Door |
| `ranking_weights.yaml` | Rank among legal ids |
| `cie.examples.yaml` | Stance |
| `residue_next.examples.yaml` | Expand hint |
| `pack_base_en.yaml` | 09 phrases (`packs_loaded: [base_en]`) |
| `semantic_*.yaml` | Structure id inventories |
| `idob_s2m_packet.yaml` | Packet contract |

Lifecycle enums live in `papers/lifecycle/idob_schema.yaml`, not here.
Path A runner: `testbenches/path_a/identity/idob_testbench.py`.
