# Debugger Documentation (pathA_short_sim/debug)

The `debug/` directory contains all human‑readable documentation and reference materials used by the `pathA_dbug.py` debugger. These files support **debugging**, **training**, and **teaching** by providing structured explanations of the simulator’s geometry, fields, primitives, and example outputs.

This directory is intentionally modular and mirrors the internal structure of the simulator’s reasoning pipeline.

---

## 1. Purpose

The debugger and its documentation serve three main purposes:

### **Debugging**
- Provide clear, structured insight into how primitives (SOB, SROB, CnOB, SmOB, IdOB) fired.
- Show segment, role, constraint, smoothing, identity, and meaning geometries.
- Surface interpreted blocks in a readable Markdown format.

### **Training**
- Help developers understand how the simulator processes structural and semantic information.
- Provide consistent reference definitions for geometry dimensions and fields.
- Enable new contributors to learn the simulator’s architecture quickly.

### **Teaching**
- Offer symbolic examples of how primitives interact.
- Demonstrate how structural and semantic cues propagate.
- Provide a conceptual map of the simulator’s reasoning pipeline.

---

## 2. Directory Structure

The `debug/` directory is organized into four main subdirectories:

```
debug/
  dimensions/
  fields/
  primitives/
  examples/
  setup/
```

### **dimensions/**
Contains documentation for geometry dimensions used by the simulator:

- `segment_geometry.md` — structural form and segment class membership  
- `role_geometry.md` — functional roles (head, modifier, predicate, argument)  
- `constraint_geometry.md` — adjacency, compatibility, structural rules  
- `smoothing_geometry.md` — continuity and reconciliation of partial matches  
- `identity_geometry.md` — referential and structural identity  
- `meaning_geometry.md` — semantic cue propagation and meaning-bearing structures  

Each file includes:
- definition  
- allowed_values  
- effects  
- debugger-style examples  

---

### **fields/**
Contains documentation for fields produced during interpretation:

- `struct_segments.md` — recognized segment structures  
- `struct_roles.md` — assigned functional roles  
- `constraints_matched.md` — satisfied structural/adjacency constraints  
- `semantic_adjacent_cues.md` — meaning-bearing adjacency cues  
- `idob_packet.md` — identity packet formation  
- `residue.md` — leftover structural/semantic material  

Each file mirrors the same structure as dimensions.

---

### **primitives/**
Documentation for the five core primitives:

- `SOB.md` — Segment Observation Block  
- `SROB.md` — Segment Role Observation Block  
- `CnOB.md` — Constraint Observation Block  
- `SmOB.md` — Smoothing Observation Block  
- `IdOB.md` — Identity Observation Block  

Each primitive file explains:
- what the primitive does  
- what values it may produce  
- how it affects interpretation  
- symbolic debugger-style examples  

---

### **examples/**
Contains symbolic examples of interpreted output:

- `placeholder.md` — debugger-style examples showing interactions between geometry, fields, and primitives  

---

### **setup/**
Contains configuration files used by the debugger:

- `debug_setup.yaml` — lists all documentation files to load  
- `links.yaml` — maps documentation names to relative paths  

These files allow the debugger to generate clickable links in `debug_out.log`.

---

## 3. How to Use the Debugger

### **Running the debugger**

From the simulator root:

```bash
python pathA_dbug.py path/to/run.log --base-dir .
```

This produces:

```
debug_out.log
```

in the base directory.

### **What the debugger does**

- Loads `debug_setup.yaml` to determine which documentation files to include.
- Loads `links.yaml` to generate clickable links in the output.
- Parses the run log into primitive blocks.
- Interprets each block using semantic placeholders.
- Generates a structured Markdown report.

### **Example output snippet**

```
## Interpreted Blocks
- SOB: Primitive SOB fired with 3 lines.
- SROB: Primitive SROB fired with 2 lines.
- CnOB: Primitive CnOB fired with 1 line.
```

### **Use cases**

#### **Debugging**
- Inspect why a primitive fired.
- Understand segment/role/constraint interactions.
- Diagnose structural or semantic residue.

#### **Training**
- Learn how primitives interact.
- Understand geometry and field definitions.
- Explore symbolic examples.

#### **Teaching**
- Demonstrate the simulator’s reasoning pipeline.
- Show how structural and semantic cues propagate.
- Provide conceptual explanations for each primitive.

### 3.1 Links Provided Inside `debug_out.log`

The debugger automatically embeds clickable links inside `debug_out.log` to help you navigate the documentation for each geometry dimension, field, and primitive. These links are generated from `links.yaml` and point to the Markdown files located in the `debug/` directory.

Each link serves as a quick reference, allowing you to jump directly to the relevant explanation for any structure the debugger reports.

#### **Types of Links Included**

The following categories of links appear in `debug_out.log`:

- **Dimension links**  
  These point to files under `debug/dimensions/` and explain:
  - segment geometry  
  - role geometry  
  - constraint geometry  
  - smoothing geometry  
  - identity geometry  
  - meaning geometry  

- **Field links**  
  These point to files under `debug/fields/` and explain:
  - struct_segments  
  - struct_roles  
  - constraints_matched  
  - semantic_adjacent_cues  
  - idob_packet  
  - residue  

- **Primitive links**  
  These point to files under `debug/primitives/` and explain:
  - SOB  
  - SROB  
  - CnOB  
  - SmOB  
  - IdOB  

- **Example links**  
  These point to symbolic examples under `debug/examples/`.

#### **How These Links Help**

- They provide **instant access** to definitions, allowed values, effects, and symbolic examples.
- They help you **interpret each primitive block** reported in the log.
- They allow you to **cross‑reference geometry and fields** without searching manually.
- They make the debugger output **self‑documenting**, ideal for:
  - debugging  
  - training  
  - teaching  
  - onboarding new contributors  

#### **VS Code Compatibility**

Even though `debug_out.log` is a `.log` file, **VS Code treats all Markdown‑style links as clickable**, including:

[Looks like the result wasn't safe to show. Let's switch things up and try something else!]

Clicking these links in VS Code on Windows will open the corresponding `.md` file immediately. No special configuration is required.

---

## 4. Notes

- All documentation files are symbolic and conceptual.
- They do not contain runtime values or simulator logic.
- They are designed to support human understanding of the system.

---

## 5. Contact

For questions or contributions, see the main project repository.

