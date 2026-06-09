**Architectural comments on the full set of file types to scan for the directory rename (comments only).**

### 1. Besides `.md`, should the rename/update scan include the following file types?

**Yes.** All of the listed categories must be scanned for references to the old directory name (`10_system_architecture`), its sub-paths, prefix patterns (e.g., `10.10.10`, `10.10.50`), or related cross-layer references. A narrow scan limited to `.md` would leave the repository in a partially consistent state and undermine the goal of intentional architecture.

- **`.py` (Python scripts, loaders, validators, promotion utilities)**: Yes. These files are critical. The repo already contains Python-based rename/migration utilities, validators (e.g., `validate_30_10_50_pairing.py`), path walkers, documentation generators, and module harnesses/prototypes. Any script that constructs paths, hard-codes directory references, performs identity renames, or validates cross-tier mappings must be examined. Leaving Python references stale would break both manual and automated maintenance paths.

- **`.yaml` / `.yml` (schemas, config, requirement maps, design‑contract metadata)**: Yes. Even if surface area is currently limited, any configuration, schema, or metadata that declares paths, prefixes, or layer relationships must be included. These often serve as machine-readable complements to the `.md` governance layer.

- **`.json` (schema definitions, requirement maps, design‑contract metadata)**: Yes. This is a high-impact category. The repository already uses `.json` for artifact manifests, name tables, glossary registries, and requirement/design-contract maps. These files frequently embed directory or prefix references and are consumed by both human review and tooling.

- **`.toml` (tooling or build configuration, if present)**: Yes. Any `.toml` files (e.g., `pyproject.toml` or similar) that reference directory structures, script entry points, or validation configurations should be scanned.

- **`.sh`, `.ps1`, `.bat` (scripts that may contain hard‑coded paths)**: Yes. Shell and PowerShell scripts (including any git-sync, environment, or migration helpers) commonly embed relative paths. These must be covered to protect development workflows and CI.

- **README files in any tier**: Yes. READMEs at tier roots and inside modules routinely contain directory trees, navigation links, or descriptive references to architecture layers. They are human-facing documentation that must remain aligned.

- **wave notes**: Yes. The W1/W2/W3 coverage notes are `.md` files but are explicitly critical because they document HLR mappings, contract checks, and references to the 10.10 architecture layer as part of the 30-normalize record.

- **promotion rules**: Yes. This covers `promotion_protocol.md` and related sections in 40.05/40.510. These codify cross-layer obligations and contain both path and semantic references.

- **flow‑down documents**: Yes. This includes the 05.20 flow-down protocol and 40.07 guide (once relocated), plus any supporting text describing 50 → 10.50 or 40 → 10.50 mechanics. These were created to articulate the new layering and will contain references that must be realigned.

- **any file containing prefix patterns** (e.g., `10.10.10`, `10.10.50`): Yes. Prefix patterns function as semantic identifiers independent of full directory paths. They appear in indexes, logs, and narrative text and must be updated for consistency.

- **any file containing directory paths**: Yes. This is the broadest practical category and overlaps with most others. It captures both literal paths and constructed references.

- **any file containing cross‑layer references**: Yes. Cross-layer references (narrative or structural) are the backbone of the intentional model. They appear across governance documents, indexes, logs, and tier overviews.

- **any file containing architecture or requirement indexes**: Yes. This covers 50.00_design_traceability_index.md, 30.01_verification_inventory_index.md, name tables, and any other mapping that links tiers through the 10.10 architecture layer.

**All of the above categories must be included in the search.** Limiting the scan would risk leaving the new 05/10 semantic boundary (meta-governance vs. requirement-level architecture) incompletely enforced in the actual repository content.

### 2. Are there *any other* file types or patterns that must be scanned?

Yes, a small number of additional patterns should be considered for completeness:

- `.txt` files (e.g., debug logs, output traces, or plain-text requirement summaries that may embed paths or prefixes).
- `.ini` files (e.g., `pytest.ini` or other tooling configuration that may reference directory structures for test discovery or validation).
- `requirements.txt` and similar plain-text dependency/environment files (if they contain comments or paths pointing to architecture documentation).
- Any files inside `archive/` or historical subdirectories (to prevent stale references from resurfacing during future audits).
- Generated or derived artifacts (e.g., any `.json` or `.md` produced by scripts). The generators themselves must be scanned; the generated files should ideally be regenerated after the rename rather than manually patched.

These secondary types are lower-density but still part of a thorough blast-radius assessment.

### 3. Alignment Check

Yes — all of the categories listed in section 1 (plus the additional patterns noted in section 2) must be scanned for a complete and safe rename.

**We are aligned.**

This confirms the full blast radius across formats and tiers. A rename/update mechanism scoped only to `.md` would be insufficient to preserve link integrity, cross-reference consistency, traceability preservation, and correct propagation across the 05/10/20/30/40/50 model. The scope must be defined against this expanded surface before any implementation begins.

These are the architectural comments on file-type coverage. No script is being generated.