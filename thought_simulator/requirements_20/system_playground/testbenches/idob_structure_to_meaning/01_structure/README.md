# Slide 01 — Structure

## Objective

Gain a body-sense for **structure**: meaning-blind geometry.

Structure is the six IDs plus fingerprints. It is finished before meaning is allowed to begin.

## Description (this revision)

A structure card holds:
- semantic_field_id
- semantic_role_id
- semantic_object_id
- gradient_id
- universe_id
- subfield_id
- optional residue_code (tension, still not a meaning score)
- optional feature tags (ranking signals only)

make_structural_key.py turns the six IDs into a deterministic structural_key.
Toy hash is legal here. Official hash width can wait.

## Boundary conditions

- Structure must not contain the six meaning floats.
- Structure must not encode conversational identity into the key.
- Same six IDs -> same key, always (replay).
- Changing CIE later must not require a new structural key.

## How structure will touch meaning (later slides)

Structure only decides which meaning groups are legal.
It does not assign physicality.

## This slide must print

- The card IDs
- The structural_key
- Optional residue / features

## This slide must not print

- physicality ... spatiality
- group_id
- meaning_delta_h or stop reasons

## Run (when implemented)

    python run_01_inspect_structure.py
