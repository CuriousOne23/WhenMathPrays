from __future__ import annotations

import json
from pathlib import Path

from probe_log import probe, tally

MEANING_AXIS_NAMES = {
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
}


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def test_probe_writes_four_lines_for_three_gold_plus_unseen(tmp_path: Path) -> None:
    log_path = tmp_path / "probe.jsonl"

    probe("The rock burst open.", log_path=log_path)
    probe("The project deadline is Friday.", log_path=log_path)
    probe("I can't keep doing this.", log_path=log_path)
    probe("asdf qwer 123", log_path=log_path)

    rows = _read_jsonl(log_path)
    assert len(rows) == 4


def test_tally_counts_gold_and_unseen(tmp_path: Path) -> None:
    log_path = tmp_path / "probe.jsonl"

    probe("The rock burst open.", log_path=log_path)
    probe("The project deadline is Friday.", log_path=log_path)
    probe("I can't keep doing this.", log_path=log_path)
    probe("asdf qwer 123", log_path=log_path)

    counts = tally(log_path)
    assert counts["n"] == 4
    assert counts["n_gold"] == 3
    assert counts["n_unseen"] == 1


def test_probe_keeps_u03_no_card(tmp_path: Path) -> None:
    log_path = tmp_path / "probe.jsonl"
    placement, holes = probe("I can't keep doing this.", log_path=log_path)
    assert placement["card_id"] is None
    assert len(holes) >= 1


def test_probe_logs_every_call_even_same_gold(tmp_path: Path) -> None:
    log_path = tmp_path / "probe.jsonl"

    probe("The rock burst open.", log_path=log_path)
    probe("The rock burst open.", log_path=log_path)

    rows = _read_jsonl(log_path)
    assert len(rows) == 2


def test_no_meaning_axis_names_in_logged_about_or_family(tmp_path: Path) -> None:
    log_path = tmp_path / "probe.jsonl"

    probe("The rock burst open.", log_path=log_path)
    probe("The project deadline is Friday.", log_path=log_path)
    probe("I can't keep doing this.", log_path=log_path)
    probe("asdf qwer 123", log_path=log_path)

    rows = _read_jsonl(log_path)
    for row in rows:
        about_id = row.get("about_id")
        family_id = row.get("family_id")
        if about_id is not None:
            assert str(about_id) not in MEANING_AXIS_NAMES
        if family_id is not None:
            assert str(family_id) not in MEANING_AXIS_NAMES
