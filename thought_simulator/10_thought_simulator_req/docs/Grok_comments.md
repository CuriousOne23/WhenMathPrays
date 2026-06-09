**Architectural comments on the full set of file types to scan for the directory rename (comments only).**

### 1. Besides `.md`, should the rename/update scan include the following file types?

**Yes.** All of the listed categories must be scanned for references to the old directory name (`10_system_architecture`), its sub-paths, prefix patterns (e.g., `10.10.10`, `10.10.50`), or related cross-layer references. Here is the explicit confirmation per category:

- **`.py`** (Python scripts, generators, validators, promotion utilities): Yes. These files frequently embed or construct paths, perform directory walks, maintain name tables, run validators (e.g., pairing checks between 10.50/30), or generate documentation. Any script that touches the 10-series structure, cross-tier flows, or identity renames must be examined to avoid broken logic or stale references after the rename.

- **`.yaml` / `.yml`** (schemas, config, requirement maps, design-contract metadata): Yes. Even if usage is light in the current tree, any configuration, schema, or metadata file that declares paths, prefixes, or cross-layer mappings must be scanned. Missing these would leave silent inconsistencies in tooling or validation layers.

- **`.json`** (schema definitions, requirement maps, design-contract metadata): Yes. This category is high-impact. The repo already contains multiple `.json` files that function as name tables, artifact manifests, glossary registries, and requirement/design-contract maps. These are often machine-readable companions to the `.md` governance documents and must be updated for traceability and automation to remain intact.

- **`.toml`** (tooling or build configuration, if present): Yes. Any `.toml` files (e.g., pyproject.toml or similar) that reference directory structures, scripts, or validation entry points should be included in the scan, even if the current surface area is small.

- **`.sh`, `.ps1`, `.bat`** (scripts that may contain hard-coded paths): Yes. Shell and PowerShell scripts (including any git-sync, migration, or environment scripts) commonly hard-code relative paths for builds, tests, or renames. These must be checked to prevent breakage in development or CI workflows.

- **README files in any tier**: Yes. READMEs at the root of tiers (00, 10, 20, 30, 40, 50, etc.) and inside modules routinely include directory trees, navigation links, or descriptive references to architecture layers. They are human-facing but still part of the cross-layer documentation surface.

- **wave notes**: Yes. The W1/W2/W3 wave coverage notes are `.md` but are explicitly called out here because they contain HLR mappings, contract checks, and 10.10/10.50 references that document the 30-normalize step. They are critical for preserving the wave protocol record.

- **promotion rules**: Yes. This primarily covers `promotion_protocol.md` and related sections in 40.05 and 40.510, but any file that codifies promotion or backward-flow rules must be scanned.

- **flow-down documents**: Yes. This includes the 05.20 flow-down protocol and the 40.07 guide (once relocated), plus any supporting text that describes 50 → 10.50 or 40 → 10.50 flows. These documents were created precisely to articulate cross-layer obligations and will contain references that must be realigned.

- **any file containing prefix patterns** (e.g., `10.10.10`, `10.10.50`): Yes. Prefix patterns are semantic identifiers that often appear independently of full directory paths. Updating only full paths while leaving prefix references would leave the repository in a partially consistent state.

- **any file containing directory paths**: Yes. This is the broadest practical category and overlaps with the others. It captures hard-coded or constructed paths in code, config, logs, and documentation.

- **any file containing cross-layer references**: Yes. Cross-layer references (narrative or structural) are the heart of the intentional architecture model. They appear in governance documents, indexes, logs, and tier-overviews and must be treated as first-class update targets.

- **any file containing architecture or requirement indexes**: Yes. This covers 50.00_design_traceability_index.md, 30.01_verification_inventory_index.md, name tables, and any other index or mapping that links tiers through the 10.10 architecture layer.

**All of the above categories must be included in the search.** Limiting the scan to only `.md` would leave the rename incomplete relative to the cross-tier governance model.

### 2. Are there *any other* file types or patterns that must be scanned?

Yes, a small number of additional patterns should be considered for completeness, even if their current density is lower:

- `.txt` files (e.g., debug logs, output traces, or plain-text requirement summaries that may embed paths or prefixes).
- `.ini` / `pytest.ini` / configuration files (tooling configs that may reference directory structures for test discovery or validation).
- `requirements.txt` and similar dependency or environment files (if they contain comments or paths pointing to architecture documentation).
- Any `.md` files inside `archive/` or historical subdirectories (to prevent stale references from resurfacing during audits).
- Generated or derived files (e.g., any `.json` or `.md` produced by scripts in `scripts/` or `thought_simulator/scripts/`) — these should be regenerated post-rename rather than manually edited, but the generators themselves must be scanned.

These are secondary but should be included in a comprehensive manifest so the rename does not leave “ghost” references in less-visible corners of the tree.

### 3. Alignment Check

Yes — scanning all of the categories listed in section 1 (and the additional patterns in section 2) is required for a complete, safe, and architecturally coherent rename.

This produces the verdict:

> **We are aligned.**

The full blast radius must be treated as multi-format and multi-tier. A rename/update mechanism that only touched `.md` files would be insufficient to preserve link integrity, cross-reference consistency, traceability preservation, and correct propagation across the 05/10/20/30/40/50 model. The script scope must therefore be defined against this expanded surface before any implementation begins.

These are the architectural comments on file-type coverage. No script is being generated.