from __future__ import annotations

from pathlib import Path

import pytest

from suggest_tags import ALLOWED_ABOUT, ALLOWED_FAMILY, suggest

MEANING_AXIS_NAMES = {
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
}


@pytest.fixture
def slog(tmp_path: Path) -> Path:
    return tmp_path / "suggest.jsonl"


def test_gold_rock_echoes_seed_tags(slog: Path) -> None:
    row = suggest("The rock burst open.", log_path=slog)
    assert row["kind"] == "gold"
    assert row["suggested_about_id"] == "material_event_anchor"
    assert row["suggested_family_id"] == "event_talk"
    assert row["card_id"] is None
    assert row["place_card_id"] == "S_rock_burst"


def test_gold_friday_echoes_state_talk(slog: Path) -> None:
    row = suggest("The project deadline is Friday.", log_path=slog)
    assert row["suggested_family_id"] == "state_talk"
    assert row["suggested_about_id"] == "timed_obligation_anchor"
    assert row["card_id"] is None


def test_u03_stays_no_live_card(slog: Path) -> None:
    row = suggest("I can't keep doing this.", log_path=slog)
    assert row["kind"] == "gold"
    assert row["place_card_id"] is None
    assert row["card_id"] is None
    assert row["needs_review"] is True


def test_unseen_needs_review_and_no_card(slog: Path) -> None:
    row = suggest("Why is the sky dark?", log_path=slog)
    assert row["kind"] == "unseen"
    assert row["needs_review"] is True
    assert row["card_id"] is None
    assert row["suggested_family_id"] in {None, "ask_talk"}
    if row["suggested_about_id"] is not None:
        assert row["suggested_about_id"] in ALLOWED_ABOUT
    if row["suggested_family_id"] is not None:
        assert row["suggested_family_id"] in ALLOWED_FAMILY


def test_unseen_does_not_invent_ids(slog: Path) -> None:
    row = suggest("Hello there.", log_path=slog)
    assert row["card_id"] is None
    assert row["needs_review"] is True
    if row["suggested_about_id"] is not None:
        assert row["suggested_about_id"] in ALLOWED_ABOUT
    if row["suggested_family_id"] is not None:
        assert row["suggested_family_id"] in ALLOWED_FAMILY


def test_no_meaning_axis_names(slog: Path) -> None:
    for text in [
        "The rock burst open.",
        "Hello there.",
        "Why is the sky dark?",
    ]:
        row = suggest(text, log_path=slog)
        for key in ("suggested_about_id", "suggested_family_id"):
            val = row[key]
            if val is not None:
                assert str(val) not in MEANING_AXIS_NAMES


def test_optional_log_does_not_touch_seed(slog: Path) -> None:
    suggest("Hello there.", log_path=slog)
    assert slog.exists()
    seed = Path(__file__).parent / "seed" / "placements.yaml"
    text = seed.read_text(encoding="utf-8")
    assert "Hello there." not in text
