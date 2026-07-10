# TS Dictionary (System Playground)
This directory contains the *experimental* Thought Simulator (TS) dictionary used during the
architecture, requirements, and simulation phase. It is **not** a final reference dictionary and
does **not** represent the formal specification layer. Instead, it provides structured, schema‑aligned
concept entries for testing Path A meaning construction, KnB boundary interpretation, and Path B
expression‑manifold mapping.

The dictionary here is intentionally small, simple, and easy to modify. It exists to support:
- manifold geometry experiments  
- SSR construction tests  
- RSG clause‑shape and surface‑mapping tests  
- early relational‑graph behavior  
- simulation runs in `system_simulation/`  
- validation of the starter schema  

As TS moves toward implementation, the dictionary will migrate into a dedicated **ts-specs**
repository where it will become versioned, validated, and governed.

---

## Files in This Directory

### **kn_dt_schema.json**
Starter schema defining the structure of dictionary entries:
- required fields (`id`, `name`, `type`, `description`, `schema_version`)
- relations
- constraints
- manifold metadata
- expression surfaces
- examples

This schema ensures consistency across all dictionary files during early testing.

### **kn_dt_seed.json**
Minimal seed dictionary containing only the most primitive conceptual anchors:
- entity  
- relation  
- property  

Used for the smallest possible manifold and RSG tests.

### **kn_dt_test.json**
A richer test dictionary containing multiple concept types:
- agents  
- objects  
- actions  
- properties  
- states  

Used for more realistic Path A/B simulations and manifold experiments.

### **kn_dt_examples.md**
Human‑readable examples showing how dictionary entries behave across:
- Path A (meaning construction)  
- KnB (boundary interpretation)  
- Path B (expression mapping)  

Useful for reviewers and contributors.

---

## Purpose of the Dictionary (Current Phase)
The dictionary in this directory is **experimental** and supports:
- testing the starter schema  
- validating relational structures  
- exercising manifold coordinates  
- verifying RSG surface mappings  
- enabling early SSR construction  
- providing examples for simulation runs  

It is not yet:
- a full semantic dictionary  
- a governed reference file  
- part of the formal TS specification  

Those will come later.

---

## Future Migration
When TS enters the implementation phase, this dictionary will move to a separate repository:

```
ts-specs/dictionary/
```

There it will become:
- versioned  
- validated  
- governed  
- extended  
- used by loaders, validators, coprocessors, and the TS kernel  

---

## Contribution Notes
During the architecture/simulation phase:
- entries may change frequently  
- schema may evolve  
- examples may expand  
- test dictionaries may be replaced  

All changes should remain **simple, readable, and aligned with the starter schema**.

```
This directory is for experimentation, learning, and simulation — not final specification.
```
```

---

