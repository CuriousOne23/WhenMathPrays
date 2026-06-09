#!/usr/bin/env python3
"""Canonical document address extraction per 00.00.42 prefix convention."""

from __future__ import annotations

import re

# Module directory: 40.160_tp_lifecycle, 30.150_tp_lifecycle
MODULE_DIR_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")
# Numbered markdown file: 50.130.010_foo.md, 20.105_tp_requirements.md
FILE_ADDRESS_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)\.md$")
DOCUMENT_ID_RE = re.compile(
    r"Document\s+ID:\s*\*?\*?\s*(\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

TIER_ROOTS = {
    "00": "00_program_governance",
    "10": "10_thought_simulator_req",
    "20": "20_requirements",
    "30": "30_verification",
    "40": "40_thought_simulator_playground",
    "50": "50_thought_simulator_design",
}

# Organizational folders — not module bands (00.00.42 addressing applies inside them, not to folder name).
ORGANIZATIONAL_DIRS: dict[str, frozenset[str]] = {
    "00_program_governance": frozenset(
        {"00_foundations", "00_identity", "10_architecture", "30_philosophical"}
    ),
    "10_thought_simulator_req": frozenset(
        {
            "10_system_architecture",
            "50_design",
            "20_requirements",
            "30_verification",
            "40_playground",
            "60_review",
            "70_measurement",
            "80_safety",
            "90_validation",
            "docs",
            "adrs",
        }
    ),
    "40_thought_simulator_playground": frozenset({"archive", "shared"}),
}

# 10_thought_simulator_req subsystem → expected file band prefix (startswith).
TEN_SUBSYSTEM_BAND_PREFIX = {
    "10_system_architecture": "10.10",
    "50_design": "10.50",
}

# Paths exempt from "missing frontmatter" (identity = path; guides/meta/coverage).
FRONTMATTER_EXEMPT_SUFFIXES = (
    "/Grok_review_in_20.md",
    "/30.00_verification_user_guide.md",
    "/30.01_verification_inventory_index.md",
    "/30.30_verification_glossary.md",
    "/W1_track_h_wave_coverage_note.md",
    "/W2_conversation_layer_wave_coverage_note.md",
    "/50.00_design_traceability_index.md",
    "/50.01_50_series_glossary.md",
    "/50.05_software_spec_construction_guide.md",
    "/30.tb/README.md",
)

FRONTMATTER_EXEMPT_PREFIXES = (
    "20_requirements/20.190_",
    "20_requirements/20.200_",
    "20_requirements/20.500_",
    "20_requirements/20.510_",
)

ID_BAND_IN_TOKEN_RE = re.compile(
    r"^(?:HLR|LLR)-((?:20|10\.50|30|50)\.(?:\d+\.)*\d+)"
)


def is_organizational_dir(tier_dir_name: str, subdir_name: str) -> bool:
    return subdir_name in ORGANIZATIONAL_DIRS.get(tier_dir_name, frozenset())


def is_frontmatter_exempt(rel_path: str) -> bool:
    if any(rel_path.endswith(suffix) for suffix in FRONTMATTER_EXEMPT_SUFFIXES):
        return True
    if any(rel_path.startswith(prefix) for prefix in FRONTMATTER_EXEMPT_PREFIXES):
        return True
    if "Grok_comment" in rel_path or rel_path.endswith("/README.md"):
        return True
    return False


def is_normative_spec_path(rel_path: str) -> bool:
    """Normative docs where YAML frontmatter is expected (warning if absent)."""
    if is_frontmatter_exempt(rel_path):
        return False
    if rel_path.startswith("20_requirements/") and FILE_ADDRESS_RE.match(rel_path.rsplit("/", 1)[-1]):
        return True
    if rel_path.startswith("50_thought_simulator_design/"):
        name = rel_path.rsplit("/", 1)[-1]
        match = FILE_ADDRESS_RE.match(name)
        if match and not match.group(1).startswith("50.0") and int(match.group(1).split(".")[1]) >= 10:
            # 50.10+ module/governance bands that are specs; 50.00-50.09 are meta guides (exempt above)
            band_parts = match.group(1).split(".")
            if len(band_parts) >= 2:
                try:
                    primary = int(band_parts[1])
                except ValueError:
                    return True
                if primary < 10:
                    return False
        if match:
            return True
    if rel_path.startswith("30_verification/"):
        parts = rel_path.split("/")
        if len(parts) >= 2:
            module_match = MODULE_DIR_RE.match(parts[1])
            if module_match:
                try:
                    band_primary = int(module_match.group(1).split(".")[1])
                except (IndexError, ValueError):
                    return True
                return band_primary >= 10
    return False


def canonical_address_from_path(rel_path: str) -> str | None:
    """Return dotted canonical address for alignment checks (warnings only)."""
    if rel_path.startswith("40_thought_simulator_playground/"):
        return _address_40_subdirectory(rel_path)
    if rel_path.startswith("00_program_governance/"):
        return _address_from_filename(rel_path.rsplit("/", 1)[-1])
    if rel_path.startswith("10_thought_simulator_req/50_design/"):
        return _address_from_filename(rel_path.rsplit("/", 1)[-1])
    if rel_path.startswith("20_requirements/"):
        return _address_from_filename(rel_path.rsplit("/", 1)[-1])
    if rel_path.startswith("50_thought_simulator_design/"):
        return _address_from_filename(rel_path.rsplit("/", 1)[-1])
    if rel_path.startswith("30_verification/"):
        return _address_30(rel_path)
    return None


def _address_40_subdirectory(rel_path: str) -> str | None:
    """40 tier: module band from immediate playground submodule directory only."""
    parts = rel_path.split("/")
    if len(parts) < 2:
        return None
    for part in parts[1:]:
        if part in ORGANIZATIONAL_DIRS.get("40_thought_simulator_playground", frozenset()):
            continue
        match = MODULE_DIR_RE.match(part)
        if match and match.group(1).startswith("40."):
            return match.group(1)
    return None


def _address_30(rel_path: str) -> str | None:
    parts = rel_path.split("/")
    if len(parts) < 2:
        return None
    module_match = MODULE_DIR_RE.match(parts[1])
    if module_match and module_match.group(1).startswith("30."):
        file_match = FILE_ADDRESS_RE.match(parts[-1])
        if file_match and file_match.group(1).startswith("30."):
            return file_match.group(1)
        return module_match.group(1)
    return _address_from_filename(parts[-1])


def _address_from_filename(filename: str) -> str | None:
    match = FILE_ADDRESS_RE.match(filename)
    if match:
        return match.group(1)
    return None


def parse_document_id(text: str) -> str | None:
    for line in text.splitlines()[:40]:
        match = DOCUMENT_ID_RE.search(line)
        if match:
            return match.group(1)
    return None


def normalize_address(addr: str) -> str:
    """Collapse zero-padded numeric segments (20.010 ≡ 20.10 per legacy bands)."""
    return ".".join(str(int(part)) if part.isdigit() else part for part in addr.split("."))


def address_prefixes_compatible(canonical: str, claimed: str) -> bool:
    """True when claimed ID band equals or extends canonical path band."""
    if canonical == claimed:
        return True
    norm_canonical = normalize_address(canonical)
    norm_claimed = normalize_address(claimed)
    if norm_canonical == norm_claimed:
        return True
    return (
        norm_canonical.startswith(norm_claimed + ".")
        or norm_claimed.startswith(norm_canonical + ".")
        or canonical.startswith(claimed + ".")
        or claimed.startswith(canonical + ".")
    )


def address_bands_related(canonical: str, band: str) -> bool:
    """True when an inline ID band plausibly belongs to this document (not a cross-ref)."""
    if not canonical or not band:
        return False
    norm_c = normalize_address(canonical)
    norm_b = normalize_address(band)
    if norm_c == norm_b:
        return True
    return norm_c.startswith(norm_b + ".") or norm_b.startswith(norm_c + ".")


def is_tier40_path(rel_path: str) -> bool:
    return rel_path.startswith("40_thought_simulator_playground/")


def is_alignment_only_path(rel_path: str) -> bool:
    """Paths where only path/Document-ID alignment applies (not strict inline ID shape)."""
    return is_tier40_path(rel_path) or rel_path.startswith("00_program_governance/")


def id_token_band(token: str) -> str | None:
    match = ID_BAND_IN_TOKEN_RE.match(token)
    if match:
        return match.group(1)
    return None


def id_band_aligns_with_address(token: str, canonical: str | None) -> bool:
    if canonical is None:
        return True
    band = id_token_band(token)
    if band is None:
        return True
    if not address_bands_related(canonical, band):
        return True
    return address_prefixes_compatible(canonical, band)


def expected_id_families(rel_path: str) -> frozenset[str]:
    if rel_path.startswith("20_requirements/"):
        return frozenset({"HLR-20"})
    if rel_path.startswith("10_thought_simulator_req/50_design/"):
        return frozenset({"HLR-10.50"})
    if rel_path.startswith("30_verification/"):
        return frozenset({"LLR-30"})
    if rel_path.startswith("50_thought_simulator_design/"):
        return frozenset({"LLR-50", "HLR-10.50", "HLR-20"})
    if rel_path.startswith("40_thought_simulator_playground/"):
        return frozenset()
    return frozenset()