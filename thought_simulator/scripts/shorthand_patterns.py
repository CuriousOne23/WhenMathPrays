#!/usr/bin/env python3
"""Governed band-prefix shorthand: allowed contexts, validation, and Class B replacements."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Iterable

from identity_tables import (
    IDENTITY_DIR,
    ROOT,
    TABLE_10_50,
    TABLE_30,
    TABLE_40,
    TABLE_50,
    IdentityEntry,
    entries_by_id,
    load_table,
)

SHORTHAND_REGISTRY = IDENTITY_DIR / "shorthand_registry.json"
SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})

# Tier governance doc IDs — never treat as module band shorthand in validation
GOVERNANCE_DOC_TOKENS = frozenset(
    {
        "40.20",
        "40.510",
        "30.00",
        "30.01",
        "30.30",
        "50.00",
        "50.01",
        "50.05",
    }
)

# Shorthand band token ends here: not followed by . digit or _ (underscore => canonical slug)
_STRICT_TAIL = r"(?![.\d_])"
# After band in ID/path patterns (hyphen for HLR/LLR, underscore for slug)
_AFTER_TAIL = r"(?=[\-_])"
# Bare token must not be a substring of a longer tier address (e.g. 50.100 inside 10.50.100)
_TOKEN_LOOKBEHIND = r"(?<![.\d])"


@dataclass(frozen=True)
class ShorthandContext:
    id: str
    template: str
    tier: str
    boundary: str


@dataclass(frozen=True)
class FileRule:
    id: str
    paths: tuple[str, ...]
    path_glob: str | None
    exclude_globs: tuple[str, ...]
    contexts: tuple[ShorthandContext, ...]


@dataclass(frozen=True)
class BandRef:
    tier: str
    band: str
    entry_id: str
    shorthand_eligible: bool

    @property
    def token(self) -> str:
        if self.tier == "10.50":
            return f"10.50.{self.band}"
        return f"{self.tier}.{self.band}"


def load_registry() -> dict[str, Any]:
    with SHORTHAND_REGISTRY.open(encoding="utf-8") as fh:
        return json.load(fh)


def parse_file_rules(registry: dict[str, Any]) -> list[FileRule]:
    rules: list[FileRule] = []
    for raw in registry.get("file_rules", []):
        rules.append(
            FileRule(
                id=raw["id"],
                paths=tuple(raw.get("paths", [])),
                path_glob=raw.get("path_glob"),
                exclude_globs=tuple(raw.get("exclude_globs", [])),
                contexts=tuple(
                    ShorthandContext(
                        id=c["id"],
                        template=c["template"],
                        tier=c["tier"],
                        boundary=c.get("boundary", "strict"),
                    )
                    for c in raw.get("contexts", [])
                ),
            )
        )
    return rules


def _path_matches_rule(rel_posix: str, rule: FileRule) -> bool:
    for ex in rule.exclude_globs:
        if fnmatch(rel_posix, ex):
            return False
    if rule.paths and rel_posix in rule.paths:
        return True
    if rule.path_glob and fnmatch(rel_posix, rule.path_glob):
        return True
    return False


def rules_for_file(rel_posix: str, rules: list[FileRule]) -> list[FileRule]:
    return [r for r in rules if _path_matches_rule(rel_posix, r)]


def _boundary_suffix(boundary: str) -> str:
    if boundary == "after":
        return _AFTER_TAIL
    if boundary == "exact":
        return r"(?=\b)"
    return _STRICT_TAIL


def _template_to_regex(template: str, band: str, boundary: str) -> re.Pattern[str]:
    escaped_band = re.escape(band)
    body = template.replace("{band}", escaped_band)
    if boundary == "exact":
        pattern = re.escape(body)
    else:
        # split around band token for boundary insert
        parts = template.split("{band}")
        if len(parts) == 2:
            pattern = re.escape(parts[0]) + escaped_band + re.escape(parts[1]) + _boundary_suffix(boundary)
        else:
            pattern = re.escape(body) + _boundary_suffix(boundary)
    return re.compile(pattern)


def _tier_in_context(context: ShorthandContext, tier: str) -> bool:
    return context.tier == tier or context.tier == "multi"


def render_template(template: str, band: str) -> str:
    return template.replace("{band}", band)


def collect_band_refs() -> list[BandRef]:
    """All bands from name tables with shorthand eligibility (unique band per tier)."""
    refs: list[BandRef] = []
    tier_tables = [
        ("40", TABLE_40),
        ("30", TABLE_30),
        ("10.50", TABLE_10_50),
        ("50", TABLE_50),
    ]
    for tier, path in tier_tables:
        if not path.is_file():
            continue
        table = load_table(path)
        band_counts: dict[str, int] = {}
        for entry in table.get("entries", []):
            band_counts[entry["band"]] = band_counts.get(entry["band"], 0) + 1
        for entry in table.get("entries", []):
            band = entry["band"]
            eligible = entry.get("shorthand_eligible", band_counts[band] == 1)
            refs.append(
                BandRef(
                    tier=tier,
                    band=band,
                    entry_id=entry["entry_id"],
                    shorthand_eligible=bool(eligible),
                )
            )
    return refs


def shorthand_replacement_pairs(
    old_band: str,
    new_band: str,
    tier: str,
    *,
    rel_path: str | None = None,
) -> list[tuple[str, str]]:
    """Build allowlisted shorthand old->new pairs for Class B band migration."""
    if old_band == new_band:
        return []
    registry = load_registry()
    rules = parse_file_rules(registry)
    pairs: list[tuple[str, str]] = []

    applicable_rules = rules if rel_path is None else rules_for_file(rel_path, rules)

    for rule in applicable_rules:
        for ctx in rule.contexts:
            if not _tier_in_context(ctx, tier):
                continue
            if ctx.tier == "multi":
                # multi-tier templates include several prefixes; replace each tier segment
                old_text = render_template(ctx.template, old_band)
                new_text = render_template(ctx.template, new_band)
                if old_text != new_text:
                    pairs.append((old_text, new_text))
            else:
                old_text = render_template(ctx.template, old_band)
                new_text = render_template(ctx.template, new_band)
                if old_text != new_text:
                    pairs.append((old_text, new_text))

    # Dedupe longest first
    pairs = list(dict.fromkeys(pairs))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def _bare_token_regex(band_ref: BandRef) -> re.Pattern[str]:
    return re.compile(_TOKEN_LOOKBEHIND + re.escape(band_ref.token) + _STRICT_TAIL)


def all_shorthand_occurrence_spans(text: str, band_ref: BandRef) -> list[tuple[int, int]]:
    """Find spans of bare shorthand token in text."""
    spans: list[tuple[int, int]] = []
    for match in _bare_token_regex(band_ref).finditer(text):
        spans.append(match.span())
    return spans


def covered_spans(text: str, band_ref: BandRef, file_rules: list[FileRule]) -> list[tuple[int, int]]:
    covered: list[tuple[int, int]] = []
    for rule in file_rules:
        for ctx in rule.contexts:
            if not _tier_in_context(ctx, band_ref.tier):
                continue
            if ctx.tier == "multi":
                regex = re.compile(re.escape(render_template(ctx.template, band_ref.band)))
            else:
                regex = _template_to_regex(ctx.template, band_ref.band, ctx.boundary)
            for match in regex.finditer(text):
                covered.append(match.span())
    return _merge_spans(covered)


def _merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not spans:
        return []
    spans = sorted(spans)
    merged = [spans[0]]
    for start, end in spans[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def _span_covered(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in spans)


def find_ungoverned_shorthand(
    rel_posix: str,
    text: str,
    band_refs: list[BandRef],
    all_rules: list[FileRule],
) -> list[tuple[str, int, str]]:
    """Return list of (token, line_no, context_snippet) for violations."""
    if any(fnmatch(rel_posix, ex.replace("**", "*")) for ex in ("archive/**",)):
        return []
    file_rules = rules_for_file(rel_posix, all_rules)
    if not file_rules:
        return []

    violations: list[tuple[str, int, str]] = []
    lines = text.splitlines()

    for band_ref in band_refs:
        if not band_ref.shorthand_eligible:
            continue
        if band_ref.token in GOVERNANCE_DOC_TOKENS:
            continue
        covered = covered_spans(text, band_ref, file_rules)
        for match in _bare_token_regex(band_ref).finditer(text):
            if not _span_covered(match.start(), covered):
                line_no = text[: match.start()].count("\n") + 1
                snippet = lines[line_no - 1].strip()[:120]
                violations.append((band_ref.token, line_no, snippet))

    return violations


def iter_md_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.md"):
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        yield path


def apply_shorthand_replacements_to_file(
    path: Path,
    replacements: list[tuple[str, str]],
) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False