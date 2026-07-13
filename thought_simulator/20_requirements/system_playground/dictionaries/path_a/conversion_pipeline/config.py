"""
config.py
---------

Central configuration for the TS Path A dictionary conversion pipeline.

This file defines:
    • chunking parameters
    • directory locations
    • WordNet input paths
    • future growth limits

All modules import from config.py to ensure deterministic, centralized
configuration across the entire pipeline.
"""

from pathlib import Path


# ============================================================
# Directory Configuration
# ============================================================

# Base directory for this pipeline (directory containing this file)
BASE_DIR = Path(__file__).parent.resolve()

# Raw WordNet input directory
WORDNET_DIR = BASE_DIR / "wordnet_raw"

# Developer dictionary output directory
DEV_OUTPUT_DIR = BASE_DIR / "dictionaries_dev"

# Runtime dictionary output directory
RUNTIME_OUTPUT_DIR = BASE_DIR / "dictionaries_runtime"


# ============================================================
# Chunking Configuration
# ============================================================

# Number of chunks to produce (developer + runtime)
CHUNK_COUNT = 6

# Target compressed size per chunk (in MB)
# ~1.7–1.8MB compressed is typical for WordNet → TS Path A
CHUNK_TARGET_SIZE_MB = 2.0

# Maximum allowed future growth per chunk (in MB)
# Allows expansion to 2.5MB → 3MB without re-chunking
CHUNK_GROWTH_LIMIT_MB = 3.0


# ============================================================
# Word Density Profile (WDP)
# ============================================================

# Whether to compute WDP (always True for chunking)
ENABLE_WDP = True


# ============================================================
# Runtime Stripping Configuration
# ============================================================

# Fields to keep in runtime dictionary
RUNTIME_KEEP_FIELDS = {
    "lemma",
    "alternates",
    "primitive",
    "invariants",
    "cue_envelope",
    "routing_signature",
    "identity_anchor",
}


# ============================================================
# Manifest Configuration
# ============================================================

# Manifest filename (same for dev and runtime)
MANIFEST_FILENAME = "manifest.json"


# ============================================================
# YAML Writer (legacy)
# ============================================================

# YAML writer is supported but not recommended
ENABLE_YAML_WRITER = False
