# PathA Short Simulation User Guide

## Run the Simulator

Run the examples script from this directory:

```powershell
python run_examples.py
or to log:
python run_examples.py > run.log
```

See [pathA_supported_sentences.md](notes/pathA_supported_sentences.md) to see current sentences run_examples.py supports.

## Modify the Input Raw Sentence

Open run_examples.py and change the raw input sentence passed into run_pathA_short(...), then rerun the script.

## Interpret the Final TP

The final TP is the end-state substrate after all primitives run. Focus on:

- tokens and normalized_text for intake output
- struct_segments and segment_tokens for OB-Set output
- struct_roles and role_segments for role assignment output
- constraints_matched, constraints_unmatched, and constraint_residue for CnOB output
- smoothing_operations, semantic_adjacent_cues, and basin_residue for SmOB output
- routing_metadata and routing_decision for routing behavior
- semantic_core for extracted agent/action/patient/modifiers
- commit_flags for macro completion checkpoints

## Interpret the Trace Output

Each trace item includes:

- primitive: primitive name executed
- input: TP snapshot before primitive
- output: TP snapshot after primitive
- notes: human-readable observation

Read input/output deltas to see exactly what each primitive changed.

## Follow TP Evolution Macro-by-Macro

1. Intake Macro: InB, IIInB, IE
2. Correction Macro: CEx, CE, ISc, TPU
3. Structural Geometry Macro: SOB, SROB, CnOB, SmOB, SSG
4. Routing Macro: RBU, RB, TR, TRU, RTU, CTP
5. Semantic Macro: IdOB
6. Final Commit Macro: OuBA

## Debug Odd Outputs

- Confirm token normalization in IE.
- Verify YAML dictionaries contain expected entries.
- Check SOB segment_tokens alignment with token classes.
- Check SROB role assignment progression for repeated segment types.
- Confirm CnOB role transition pairs are present in constraint_rules.yaml.
- Confirm IdOB semantic rules and extracted fields match segment/role traces.

## Modify Dictionaries

Edit files under support/dictionaries:

- token_classes.yaml
- segment_patterns.yaml
- role_patterns.yaml
- constraint_rules.yaml
- semantic_rules.yaml

Then rerun run_examples.py and compare trace deltas.

## Extend Primitives

Edit primitives_pathA_short.py to add or refine primitive logic. Keep mutations explicit and trace-visible so TP evolution remains easy to inspect.
