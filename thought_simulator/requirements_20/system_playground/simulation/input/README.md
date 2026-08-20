# Simulation Input Directory
This directory contains the *canonical conversation inputs* used for
pipeline-level simulation within the Thought Simulator (TS) Path A system.

Each canonical conversation is stored in its own subdirectory:

simulation/input/
    conv_01/
    conv_02/
    conv_03/
    ...

This structure ensures that every conversation is self-contained, easy to
navigate, and easy for an AI to consume during simulation, debugging, and
pipeline refinement.

---

## Purpose of This Directory

The files in this directory serve as the **ground truth inputs** for
pipeline simulations. They provide:

- A set of **TP snapshots** (`canonical_msgX_tp.yaml`) using the field
  definitions from **20.40.060.700 — OuBA Field Reference**
- A **semantic narrative** (`canonical_tp.md`) describing the meaning,
  identity geometry evolution, continuity evolution, next_context evolution,
  provenance, and routing interpretation across the entire multi-turn arc
- A place to store **pipeline segment inputs** and **pipeline segment outputs**
  generated during simulation
- A place to store **debugging notes**, lineage logs, and multi-turn simulation
  results

This directory is the foundation for deterministic, reproducible, and
scalable Path A simulation.

---

## Directory Structure for Each Conversation

Each canonical conversation lives in its own directory:

conv_XX/
    idob_10_conversations_ex.md
    canonical_msg1_tp.yaml
    canonical_msg2_tp.yaml
    ...
    canonical_msg10_tp.yaml
    canonical_tp.md
    pipeline_inputs/
    pipeline_outputs/
    notes.md

### `idob_10_conversations_ex.md`
The *source document* containing all 10 messages of the conversation.
Each message corresponds to one IdOB case (Case #1 → Case #10).

### `canonical_msgX_tp.yaml`
A TP snapshot for message X, representing the **IdOB output** after IdOB
processes that message. Each file contains **all fields** defined in
20.40.060.700 and is used directly by the simulation runner.

These snapshots represent the TP *before* any downstream primitives
(MCB, RBU, TR, CTP, CEX, COB, CIL, CST, OuBA) have run.

### `canonical_tp.md`
A human-readable semantic explanation of the **entire 10-message arc**, including:
- topic, stance, intent, register, importance evolution  
- identity geometry evolution (formation → refinement → correction → drift → conflict → bifurcation → stabilization → continuation → reinforcement → closure)  
- continuity evolution  
- next_context evolution  
- provenance and routing narrative  
- freeze boundary interpretation  
- semantic_core evolution  

This file provides the semantic context needed to interpret simulation results.

### `pipeline_inputs/`
AI-generated input YAMLs for arbitrary Path A pipeline segments.
These are derived from:
- the TP snapshot for the relevant message  
- the first primitive in the pipeline segment  

### `pipeline_outputs/`
AI-generated output YAMLs for pipeline segments.
These are derived from:
- running the pipeline segment  
- the last primitive’s TPSnS rules  

These outputs include downstream TP transformations and, when the segment
includes OuBA, the **SSR (frozen meaning snapshot)**.

### `notes.md`
Optional debugging notes, lineage logs, anomalies, and insights discovered
during simulation.

---

## Why Each Conversation Has Its Own Directory

As the system grows, we will have many canonical conversations:
- conv_01 (full 10-message IdOB arc #1)
- conv_02 (another 10-message arc)
- …
- conv_10, conv_11, conv_12, …

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
- a TP snapshot (e.g., `conv_01/canonical_msg4_tp.yaml`)
- a pipeline segment definition (e.g., `sob → srob → cnob → smob → idob`)

The AI can deterministically derive:
- the **input YAML** for that segment  
- the **output YAML** after running the segment  

This works because:
- each TP snapshot contains *all* fields defined in 20.40.060.700  
- the first primitive defines the input contract  
- the last primitive defines the output contract  

This directory is therefore the foundation for all higher-level simulation.

---

## Summary

This directory provides:
- a clean, scalable structure for canonical conversations  
- a complete set of TP snapshots for each message  
- a single semantic narrative describing the entire arc  
- a consistent foundation for pipeline simulation  
- a reproducible environment for debugging and refinement  
- a structure optimized for AI consumption and future automation  

As new conversations are added, simply create:

simulation/input/conv_XX/

and populate it with the canonical files.
