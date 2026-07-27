"""
IE primitive (Intake Engine) – deterministic, pre-semantic normalization and repair application.

Design goals (to align with 20.15 / 20.101 / 20.109 style requirements):

- Deterministic:
    - Same input + same repair set => same output, independent of runtime environment.
    - Repairs applied in a stable, well-defined order.

- Pre-semantic:
    - No semantic inference, no meaning injection.
    - Only structural / lexical normalization and repair application.

- Replayable:
    - Output includes enough metadata to reconstruct:
        - which repairs were applied,
        - in what order,
        - on which spans.

- Structurally explicit:
    - Token boundaries are preserved and exposed.
    - Normalization is transparent and documented in metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid
import re


# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RepairProposal:
    """
    A single deterministic repair proposal, typically produced by IIInB.

    Fields are intentionally explicit so that IE can:
    - sort deterministically,
    - apply repairs without ambiguity,
    - expose replay metadata.
    """
    id: str
    kind: str          # e.g., "whitespace", "punctuation", "token_rewrite"
    start: int         # inclusive character index in the original text
    end: int           # exclusive character index in the original text
    replacement: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Anomaly:
    """
    Structural anomaly detected upstream (or alongside repairs).
    IE does not fix anomalies semantically; it only preserves and reports them.
    """
    id: str
    kind: str          # e.g., "unexpected_token", "unbalanced_bracket"
    start: int
    end: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReplayMetadata:
    """
    Metadata sufficient to replay IE behavior deterministically.
    """
    engine_id: str
    run_id: str
    timestamp_iso: str
    repair_count: int
    anomaly_count: int
    source: str = "ie_primitive"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IEOutput:
    """
    Structured output of IE.

    - normalized_text: the post-repair, normalized intake string.
    - token_boundaries: list of (start, end) spans in normalized_text.
    - repairs_applied: ordered list of RepairProposal actually applied.
    - anomalies: anomalies passed through (not semantically fixed).
    - replay_metadata: deterministic replay information.
    """
    normalized_text: str
    token_boundaries: List[Tuple[int, int]]
    repairs_applied: List[RepairProposal]
    anomalies: List[Anomaly]
    replay_metadata: ReplayMetadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "normalized_text": self.normalized_text,
            "token_boundaries": self.token_boundaries,
            "repairs_applied": [asdict(r) for r in self.repairs_applied],
            "anomalies": [asdict(a) for a in self.anomalies],
            "replay_metadata": self.replay_metadata.to_dict(),
        }


# ---------------------------------------------------------------------------
# Deterministic repair ordering
# ---------------------------------------------------------------------------

def _sort_repairs_deterministically(repairs: List[RepairProposal]) -> List[RepairProposal]:
    """
    Sort repairs in a stable, deterministic order.

    Primary keys:
    - start index
    - end index
    - kind
    - id

    This ensures that:
    - overlapping repairs are applied in a predictable way,
    - replay is stable across environments.
    """
    return sorted(
        repairs,
        key=lambda r: (r.start, r.end, r.kind, r.id),
    )


# ---------------------------------------------------------------------------
# Repair application
# ---------------------------------------------------------------------------

def _apply_repairs_to_text(text: str, repairs: List[RepairProposal]) -> str:
    """
    Apply a sorted list of repairs to the original text.

    Assumptions:
    - repairs are already sorted deterministically.
    - indices refer to the original text; we apply them left-to-right,
      building a new string.

    Overlapping repairs:
    - If a repair overlaps with a previously applied region, we skip it.
      (You can change this policy if your spec requires something else.)
    """
    if not repairs:
        return text

    result_parts: List[str] = []
    cursor = 0
    last_end = -1

    for r in repairs:
        # Skip invalid or overlapping repairs
        if r.start < cursor or r.start < 0 or r.end > len(text) or r.start >= r.end:
            continue

        # Append untouched text before this repair
        if cursor < r.start:
            result_parts.append(text[cursor:r.start])

        # Append replacement
        result_parts.append(r.replacement)
        cursor = r.end
        last_end = r.end

    # Append any remaining text after the last repair
    if cursor < len(text):
        result_parts.append(text[cursor:])

    return "".join(result_parts)


# ---------------------------------------------------------------------------
# Normalization (pre-semantic)
# ---------------------------------------------------------------------------

_WHITESPACE_RE = re.compile(r"[ \t]+")


def _normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in a pre-semantic way:

    - Collapse runs of spaces/tabs into a single space.
    - Preserve newlines (so structural line boundaries remain visible).
    """
    # First, normalize spaces/tabs within lines
    lines = text.split("\n")
    normalized_lines = [_WHITESPACE_RE.sub(" ", line).strip() for line in lines]
    # Preserve line structure
    return "\n".join(normalized_lines)


_TOKEN_RE = re.compile(r"\S+")


def _compute_token_boundaries(text: str) -> List[Tuple[int, int]]:
    """
    Compute token boundaries as (start, end) spans in the normalized text.

    Tokens are defined as maximal runs of non-whitespace characters.
    """
    boundaries: List[Tuple[int, int]] = []
    for match in _TOKEN_RE.finditer(text):
        boundaries.append((match.start(), match.end()))
    return boundaries


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_ie(
    intake_text: str,
    repair_proposals: List[Dict[str, Any]],
    anomalies: Optional[List[Dict[str, Any]]] = None,
    engine_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main entry point for the IE primitive.

    Parameters
    ----------
    intake_text:
        Raw intake string from upstream (pre-semantic).
    repair_proposals:
        List of dicts describing repairs, typically produced by IIInB.
        Each dict should contain:
            - id (str)
            - kind (str)
            - start (int)
            - end (int)
            - replacement (str)
            - metadata (optional dict)
    anomalies:
        Optional list of dicts describing anomalies.
    engine_id:
        Optional identifier for this IE instance; if None, a UUID is generated.

    Returns
    -------
    dict:
        A structured dict representation of IEOutput, suitable for YAML/JSON
        serialization and testbench consumption.
    """
    # Convert repair proposals to dataclasses
    repairs: List[RepairProposal] = []
    for rp in repair_proposals:
        repairs.append(
            RepairProposal(
                id=str(rp.get("id", uuid.uuid4().hex)),
                kind=str(rp.get("kind", "unspecified")),
                start=int(rp.get("start", 0)),
                end=int(rp.get("end", 0)),
                replacement=str(rp.get("replacement", "")),
                metadata=dict(rp.get("metadata", {})),
            )
        )

    # Convert anomalies to dataclasses
    anomaly_objs: List[Anomaly] = []
    if anomalies:
        for a in anomalies:
            anomaly_objs.append(
                Anomaly(
                    id=str(a.get("id", uuid.uuid4().hex)),
                    kind=str(a.get("kind", "unspecified")),
                    start=int(a.get("start", 0)),
                    end=int(a.get("end", 0)),
                    metadata=dict(a.get("metadata", {})),
                )
            )

    # Deterministic repair ordering
    sorted_repairs = _sort_repairs_deterministically(repairs)

    # Apply repairs
    repaired_text = _apply_repairs_to_text(intake_text, sorted_repairs)

    # Normalize (pre-semantic)
    normalized_text = _normalize_whitespace(repaired_text)

    # Token boundaries
    token_boundaries = _compute_token_boundaries(normalized_text)

    # Replay metadata
    replay = ReplayMetadata(
        engine_id=engine_id or uuid.uuid4().hex,
        run_id=uuid.uuid4().hex,
        timestamp_iso=datetime.utcnow().isoformat() + "Z",
        repair_count=len(sorted_repairs),
        anomaly_count=len(anomaly_objs),
    )

    output = IEOutput(
        normalized_text=normalized_text,
        token_boundaries=token_boundaries,
        repairs_applied=sorted_repairs,
        anomalies=anomaly_objs,
        replay_metadata=replay,
    )

    return output.to_dict()


# ---------------------------------------------------------------------------
# Convenience CLI-style hook (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import sys

    if sys.stdin.isatty():
        print("IE primitive: expecting JSON on stdin.", file=sys.stderr)
        sys.exit(1)

    payload = json.load(sys.stdin)
    intake = payload.get("intake_text", "")
    repairs = payload.get("repair_proposals", [])
    anomalies = payload.get("anomalies", [])
    engine_id = payload.get("engine_id")

    result = run_ie(intake, repairs, anomalies, engine_id)
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
