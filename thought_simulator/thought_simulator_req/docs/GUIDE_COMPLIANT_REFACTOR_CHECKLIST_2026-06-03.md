# Guide-Compliant Refactor Checklist (TP-Centric TR Dirty-Flag Migration)

Status: Draft execution checklist
Date: 2026-06-03
Scope: 10_req, 30_verification, 40_playground, 50_design
Primary guides:
- 40.05 master program guide
- 50.05 software spec construction guide

## 0. Objective
Use this checklist to execute major refactoring slowly, deterministically, and with full traceability while preserving legacy evidence.

## 1. Governance Gates (Must Pass Before Edits)
- [ ] Confirm flow direction explicitly: backward
- [ ] Confirm initiating canonical source set in 10_thought_simulator_req
- [ ] Confirm impacted targets in 30_verification, 40_playground, 50_design
- [ ] Create execution log entry in 10_req/docs (or update existing transaction log)
- [ ] Freeze scope: no out-of-scope file edits

Required record in execution log:
- selected direction
- initiating source docs
- impacted target docs/folders
- approver and timestamp

## 2. Baseline Snapshot (Read-Only)
- [ ] Inventory current 40_playground module folders and capsule files
- [ ] Inventory corresponding 30_verification promoted capsules
- [ ] Inventory 10.50 requirement anchors
- [ ] Inventory 50.00 traceability mappings
- [ ] Identify stale references to archive or superseded anchors

Output artifacts:
- baseline inventory table
- stale reference list
- terminology drift list (example: ThoughtPoint vs TP)

## 3. Naming and Structure Decision Gate
- [ ] Keep top-level 40.xx module folder names unless explicit migration approval exists
- [ ] Define v2 subfolder strategy inside impacted modules (if needed)
- [ ] Define legacy containment strategy (legacy_pre_tr_dirty_flag)
- [ ] Define unchanged modules explicitly to prevent accidental churn

Decision record must include:
- folder keep/rename/create list
- rationale per decision
- risk and rollback notes

## 4. Canonical Alignment Plan (No Edits Yet)
- [ ] Map each affected 40 module to 10.50 anchor(s)
- [ ] Map each affected 30 capsule to its 40 source and 10.50 anchor
- [ ] Map each affected 50 design file and 50.00 row
- [ ] Define exact terminology normalization rules

Minimum required mappings:
- TP lifecycle and TR dirty-flag behavior
- RB iff-gate behavior
- TR clear-on-success and retain-on-failure behavior
- initialization semantics

## 5. Controlled Edit Sequence
Perform in this order only.

### 5.1 Canonical Source Layer (10)
- [ ] Update required 10.50 anchors first
- [ ] Keep normative language explicit and testable
- [ ] Record updated HLR links in execution log

### 5.2 Verification Layer (30)
- [ ] Update capsule and delta references to current canonical anchors
- [ ] Preserve legacy evidence files and hashes
- [ ] Add lineage notes for migrated terminology and links

### 5.3 Playground Layer (40)
- [ ] Apply naming cleanup and v2 subfolder setup
- [ ] Update software_description, requirements_delta, verification_capsule references
- [ ] Preserve capsule structure per module

### 5.4 Design Layer (50)
- [ ] Update affected subsystem design docs for anchor/link consistency
- [ ] Synchronize 50.00 traceability index in same transaction
- [ ] Confirm no stale 20 archive references remain in active mappings

## 6. Integrity Checks (Mandatory)
- [ ] Stale-reference scan across 30/40/50
- [ ] Glossary consistency check against 30.30_verification_glossary
- [ ] HLR/LLR mapping completeness check
- [ ] 50.00 index consistency check (all rows valid)
- [ ] Link/path validity check for renamed or moved files

## 7. Evidence Preservation Rules
- [ ] Do not delete historical evidence artifacts without explicit approval
- [ ] If deprecating old paths, mark as legacy and keep immutable snapshots
- [ ] Record all moves/renames with old->new mapping table

## 8. Completion Gate
- [ ] All four layers synchronized: 10, 30, 40, 50
- [ ] No stale canonical references in active docs
- [ ] No unresolved terminology drift in active flow docs
- [ ] Execution log includes final assertion: Forward-Equivalence State: YES
- [ ] Human review sign-off captured

## 9. Suggested Working Rhythm
- [ ] Work module-by-module, not all-at-once
- [ ] Finish one module through all layers before starting the next
- [ ] Run integrity checks after each module closes
- [ ] Keep change sets small and auditable

## 10. Module Batch Template
Use this for each module (40.05, 40.260, 40.270, etc.).

Module:
- Canonical anchor(s):
- Verification capsule(s):
- Design file(s):

Planned changes:
- Naming:
- Reference updates:
- Terminology updates:

Checks:
- stale refs passed:
- glossary sync passed:
- traceability row updated:

Decision:
- promote / hold / revise
