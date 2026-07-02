# TS Plan Going Forwart 7/2/2026

**TS Going Forward Plan**  
*Version 0.3 – July 02, 2026*  
*Prepared by Grok with CP review*  
*CuriousOne23 – Living document – review weekly*

### 1. Project Architecture
- **Main Repo** (`WhenMathPrays`): Core architecture, documentation, starter kit, and specifications. **Core repo stability is a hard constraint** — extensions must never modify core semantics.
- **Starter Kit**: Minimal, immediately usable foundation for users.
- **Extensions**: User-contributed dictionary, KnDt, and RSG modules (loaded dynamically).
- **External Data Packs**: Large-scale RSG mappings and analysis data (outside main repo).
- **Future Multi-Repo Strategy**: Split implementation, tools, and heavy data as needed.

### 2. Directory Structure (Explicit)
```
WhenMathPrays/
├── docs/
│   ├── papers/
│   ├── guides/
│   ├── requirements/          # 20-series HLRs
│   └── planning/              # This plan + lifecycle doc
├── specs/
│   ├── core/                  # Dictionary, KnDt schemas
│   ├── manifold/              # Engineered geometric manifold specification (central)
│   ├── rsg/                   # Relational Semantic Geometry specs
│   ├── testbenches/           # Logical equivalence testbenches
│   └── interfaces/            # Contracts between subsystems
├── starter-kit/
│   ├── dictionary/
│   ├── kndt/
│   ├── rsg/
│   ├── inputs/
│   └── examples/
├── data/                      # Local development data (gitignore large files)
│   ├── core/
│   └── external/              # Large packs (not in repo)
├── tools/                     # Refactoring, validation, hygiene scripts
├── tests/
│   ├── logical/               # Pre-coding testbenches
│   └── simulation/            # Future runtime tests
├── src/                       # Implementation (populated later)
└── extensions/                # User-contributed modules (gitignore or separate)
```

### 3. Reference File Strategy
- **Core Files** (in repo, KB–low MB): Minimal dictionary, KnDt seed, basic RSG mappings (**JSON / JSONL**).
- **External Packs** (outside repo, GB scale): Full RSG mappings, analysis results (**Parquet / Arrow**).
- **Manifests**: **YAML**.
- **Management**:
  - Chunking and partitioning by domain or date.
  - Versioned manifests for compatibility.
  - Lazy/streaming loaders (never load everything).
  - Compression and indexing.
- **Growth Rules**: Extensions go in user-controlled directories; core changes require review.

### 4. Support Programs Architecture
- **Loaders**: Memory-safe, lazy loading for dictionary/KnDt/RSG.
- **Validators**: Schema + logical consistency checks against testbenches.
- **Schema Compiler**: Validates and compiles dictionary/KnDt/RSG schemas into internal structures.
- **Growth Engines**: Tools to merge extensions, detect conflicts, and version data.
- **Analytics Modules**: Query interface for trajectory analysis, basin stability, etc.
- **Diff/Merge Tools**: For reference file changes.
- **Streaming Handlers**: For working with large external packs.

### 5. TS Data & Workflow Lifecycle (with Rules)
- **Entry**: Must conform to defined schema.
- **Validation**: Must pass relevant testbenches and consistency checks.
- **Integration**: Must produce diff for review; versioned merge.
- **Growth**: Must follow explicit growth rules (G1–G4); core changes require review.
- **Modification**: Extensions preferred; core changes require 2-reviewer approval.
- **Analytics**: Must be streaming-safe and incremental.
- **Feedback**: Must produce structured change proposals linked to testbenches.

### 6. AI Agent Workflow
- Use agents primarily for: generating testbenches, refining specs, creating loaders/validators, and targeted code **after** testbenches are complete.
- Agents must work against explicit testbenches and specs.
- **Agents may not modify core reference files directly**; they must propose changes via testbench-validated diffs.
- Limit open-ended code generation to reduce token burn.
- Human review required for core changes.

### 7. Open Development Strategy
- **Contribution Boundaries**: Clear guidelines (extensions easy, core protected).
- **Versioning & Stability**: Semantic versioning + compatibility guarantees.
- **Repo Checks**: CI validation, testbench runs, size limits.
- **Extensions must declare compatibility** with core version X.Y.
- **Governance**: CuriousOne23 as primary maintainer; expand as community grows.
- **Multi-Repo Readiness**: Prepare for splitting when appropriate.

### 8. Next Actions (Specific & Measurable)
1. Finalize and commit this plan (today).
2. Create explicit directory skeleton in repo.
3. Draft minimal dictionary + KnDt seed + basic RSG mapping (this week).
4. Create logical testbench template and first 2 examples.
5. Write full TS Data & Workflow Lifecycle document (with detailed rules).
6. Define AI agent usage guidelines.
7. Draft CONTRIBUTING.md with open development rules.

---
