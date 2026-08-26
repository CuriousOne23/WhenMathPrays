# Slide 02 — Meaning groups and six fields

## Objective

See meaning as groups that already carry six floats.

A group is not a sentence and not a dictionary of words.
It is a named prototype in the current layout:

- physicality
- sociality
- temporality
- intentionality
- materiality
- spatiality

Each value is in [0, 1] in this revision. Values may be hand-set.

## This slide must do

- List group_id, group_name, primitive, six floats.

## This slide must not do

- Look up a structure key.
- Apply CIE.
- Parse utterances into scores (no word-to-score formula required).

## Boundary to feel

Groups do not contain semantic_field_id.
If two groups have almost the same six numbers, later slides will fail to split senses. That is useful evidence, not a bug to hide.

## Run (when implemented)

    python run_02_inspect_groups.py
