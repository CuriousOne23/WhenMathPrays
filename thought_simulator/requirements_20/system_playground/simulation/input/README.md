# 📄 **README.md for `simulation/input/`**

# Simulation Input Directory
This directory contains the *canonical conversation inputs* used for
pipeline-level simulation within the Thought Simulator (TS) Path A system.

Each canonical conversation is stored in its own subdirectory:

```
simulation/input/
    conv_01/
    conv_02/
    conv_03/
    ...
```

This structure ensures that every conversation is self-contained, easy to
navigate, and easy for an AI to consume during simulation, debugging, and
pipeline refinement.

---

## Purpose of This Directory

The files in this directory serve as the **ground truth inputs** for
pipeline simulations. They provide:

- A **full TP snapshot** (YAML) using the field definitions from  
  **20.40.060.700 — OuBA Field Reference**
- A **semantic narrative** (MD) describing the meaning, identity geometry,
  continuity, next_context, provenance, and routing interpretation
- A place to store **pipeline segment inputs** and **pipeline segment outputs**
  generated during simulation
- A place to store **debugging notes**, lineage logs, and multi-turn simulation
  results

This directory is the foundation for deterministic, reproducible, and
scalable Path A simulation.

---

## Directory Structure for Each Conversation

Each canonical conversation lives in its own directory:

```
conv_XX/
    canonical_tp.yaml
    canonical_tp.md
    pipeline_inputs/
    pipeline_outputs/
    notes.md
```

### `canonical_tp.yaml`
A full TP snapshot containing **all fields** defined in  
20.40.060.700.  
This file is machine-readable and is used directly by the simulation runner.

### `canonical_tp.md`
A human-readable semantic explanation of the conversation, including:
- topic, stance, intent, register, importance  
- identity geometry (alignment, collapse, drift, correction, continuation)  
- continuity interpretation  
- next_context reasoning  
- provenance and routing narrative  
- freeze boundary and semantic_core interpretation  

This file provides the semantic context needed to interpret simulation results.

### `pipeline_inputs/`
AI-generated input YAMLs for arbitrary Path A pipeline segments.
These are derived from:
- the canonical TP  
- the first primitive in the pipeline segment  

### `pipeline_outputs/`
AI-generated output YAMLs for pipeline segments.
These are derived from:
- running the pipeline segment  
- the last primitive’s TPSnS rules  

### `notes.md`
Optional debugging notes, lineage logs, anomalies, and insights discovered
during simulation.

---

## Why Each Conversation Has Its Own Directory

As the system grows, we will have many canonical conversations:
- conv_01 (IdOB Case #1)
- conv_02 (IdOB Case #2)
- …
- conv_10 (IdOB Case #10)
- conv_11, conv_12, …

Each conversation may accumulate:
- multiple pipeline segment simulations  
- multi-turn simulations  
- debugging notes  
- lineage logs  
- provenance logs  
- stability analyses  

A directory-per-conversation keeps the system clean, scalable, and easy for
both humans and AI to navigate.

---

## How Pipeline Simulation Uses These Files

Given:
- a canonical TP (from `conv_XX/canonical_tp.yaml`)
- a pipeline segment definition (e.g., `sob → srob → cnob → smob → idob`)

The AI can deterministically derive:
- the **input YAML** for that segment  
- the **output YAML** after running the segment  

This works because:
- the canonical TP contains *all* fields defined in 20.40.060.700  
- the first primitive defines the input contract  
- the last primitive defines the output contract  

This directory is therefore the foundation for all higher-level simulation.

---

## Summary

This directory provides:
- a clean, scalable structure for canonical conversations  
- paired YAML + MD files for each conversation  
- a consistent foundation for pipeline simulation  
- a reproducible environment for debugging and refinement  
- a structure optimized for AI consumption and future automation  

As new conversations are added, simply create:
```
simulation/input/conv_XX/
```
and populate it with the canonical files.

```

---
