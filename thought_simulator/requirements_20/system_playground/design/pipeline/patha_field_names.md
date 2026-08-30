# patha_field_names.md — Derived Field-Name Working Index for Path-A

**Document ID:** patha_field_names  
**Version:** 0.4 (CST-Mux envelope lock)  
**Status:** Draft — derived exclusively from the listed normative and playground documents  
**Scope:** Entire Path-A pipeline field surface for structural programs, testbenches, and dual-mode validation  
**Location:** `thought_simulator/requirements_20/system_playground/design/pipeline/`  

> **Field catalog authority (20.116).** Canonical paths, envelope owners, and name-separations: [`../../../20.116_field_catalog.md`](../../../20.116_field_catalog.md) · [`../../../20.116.010_tp_envelope_index.md`](../../../20.116.010_tp_envelope_index.md) · [`../../../20.116.020_ownership_rw.md`](../../../20.116.020_ownership_rw.md) · [`../../../20.116.030_name_separations.md`](../../../20.116.030_name_separations.md). Collision: 20.116 wins names/paths/owners; primitive files win behavior (`HLR-20.116-001`–`004`).
> This file is a **derived working index**. It must match 20.116. It does not override 20.116.

**Source documents (authoritative order):**  
1. 20.32_cob_requirements.md  
2. system_playground/primitives/cob/cob_requirements.md  
3. system_playground/testbenches/progressive_lineup_testing.md  
4. system_playground/design/pipeline/primitive_transfer_table1.md  
5. system_playground/design/pipeline/primitive_transfer_table2.md  
6. 20.107.020_cex-ccr_primitive.md  
7. 20.40.055_mcb_prim.md  
8. 20.15_ts_architecture_scaffold.md  
9. 20.105_tp_requirements.md  
10. 20.105.010_tp_meta_fields.md  
11. 20.105.020_tp_meta_provenance.md  
12. 20.105.030_tp_meta_usage.md  
13. 20.32.010.010_cst-core.md  
14. system_playground/primitives/cst_core/cst_core_py_struc_pgm.md (v0.1 CP-approved path map)  
15. system_playground/primitives/cil/cil_py_struc_pgm.md / 20.33 (CIL intake path)  
16. 20.32.010.020_cst-ms.md  
17. system_playground/primitives/cst_ms/cst_ms_py_struc_pgm.md (v0.1 CP-approved path map)  
18. 20.32.010.030_cst-mux.md  
19. system_playground/primitives/cst_mux/cst_mux_py_struc_pgm.md (v0.1 CP-approved path map)  

**Rules applied:**  
- No invented field names.  
- Exact spelling and casing preserved.  
- Collisions resolved by preferring global normative documents (20.32, 20.105 series, 20.15) unless playground explicitly overrides.  
- Synonyms are not merged unless documents state they are identical.  
- Paths are shown with the conventional `TP.` prefix used in architecture documents; runtime resolvers treat paths relative to the TP root (progressive_lineup_testing.md).  
- This dictionary is a derived working index for structural programs (`*_py_struc_pgm.md`) and testbenches. 20.116 is canonical for names, paths, and owners.
