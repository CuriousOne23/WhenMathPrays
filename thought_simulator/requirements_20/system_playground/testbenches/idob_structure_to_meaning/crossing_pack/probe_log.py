from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from place import place

DEFAULT_LOG_PATH = Path(__file__).parent / "logs" / "probe.jsonl"
GOLD_UTTERANCES = {
    "The rock burst open.",
    "The project deadline is Friday.",
    "I can't keep doing this.",
}


def probe(utterance: str, source: str = "probe", log_path: Path | None = None) -> tuple[dict, list[dict]]:
    """Call place(); append one JSONL row; return the same tuple as place()."""
    placement, hole_rows = place(utterance=utterance, source=source)

    target = log_path or DEFAULT_LOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "utterance": utterance,
        "placement_id": placement.get("placement_id"),
        "about_id": placement.get("about_id"),
        "family_id": placement.get("family_id"),
        "pattern_id": placement.get("pattern_id"),
        "card_id": placement.get("card_id"),
        "hole_ids": list(placement.get("hole_ids") or []),
        "source": placement.get("source"),
        "n_holes": len(hole_rows),
        "kind": "gold" if utterance in GOLD_UTTERANCES else "unseen",
    }

    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")

    return placement, hole_rows


def tally(log_path: Path) -> dict:
    """Return counts: n, n_gold, n_unseen, unseen_rate."""
    n = 0
    n_gold = 0
    n_unseen = 0

    if not log_path.exists():
        return {"n": 0, "n_gold": 0, "n_unseen": 0, "unseen_rate": 0.0}

    with log_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n += 1
            row: dict[str, Any] = json.loads(line)
            if row.get("kind") == "gold":
                n_gold += 1
            else:
                n_unseen += 1

    unseen_rate = (n_unseen / n) if n > 0 else 0.0
    return {"n": n, "n_gold": n_gold, "n_unseen": n_unseen, "unseen_rate": unseen_rate}
