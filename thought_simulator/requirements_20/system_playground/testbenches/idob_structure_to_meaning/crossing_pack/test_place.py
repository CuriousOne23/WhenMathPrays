from __future__ import annotations

from place import place

MEANING_AXIS_NAMES = {
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
}


def test_gold_rock_burst_matches_seed_fields() -> None:
    placement, holes = place("The rock burst open.")
    assert placement["about_id"] == "material_event_anchor"
    assert placement["family_id"] == "event_talk"
    assert placement["card_id"] == "S_rock_burst"
    assert placement["hole_ids"] == []
    assert holes == []


def test_gold_deadline_friday_matches_seed_fields() -> None:
    placement, holes = place("The project deadline is Friday.")
    assert placement["about_id"] == "timed_obligation_anchor"
    assert placement["family_id"] == "state_talk"
    assert placement["card_id"] == "S_deadline_friday"
    assert placement["hole_ids"] == []
    assert holes == []


def test_u03_stays_hole_and_no_card() -> None:
    placement, holes = place("I can't keep doing this.")
    assert placement["card_id"] is None
    assert len(placement["hole_ids"]) >= 1
    assert len(holes) >= 1
    assert holes[0]["status"] == "open"


def test_replay_same_input_same_output_fields() -> None:
    p1, h1 = place("The project deadline is Friday.")
    p2, h2 = place("The project deadline is Friday.")
    assert p1 == p2
    assert h1 == h2


def test_unseen_utterance_null_tags_and_open_hole() -> None:
    placement, holes = place("asdf qwer 123")
    assert placement["about_id"] is None
    assert placement["family_id"] is None
    assert placement["pattern_id"] is None
    assert placement["card_id"] is None
    assert len(placement["hole_ids"]) == 1
    assert len(holes) == 1
    assert holes[0]["status"] == "open"
    assert holes[0]["found_in"] == "utterance"
    assert holes[0]["card_id"] is None


def test_no_meaning_axis_names_in_about_or_family() -> None:
    utterances = [
        "The rock burst open.",
        "The project deadline is Friday.",
        "I can't keep doing this.",
        "asdf qwer 123",
    ]
    for text in utterances:
        placement, _holes = place(text)
        about_id = placement["about_id"]
        family_id = placement["family_id"]
        if about_id is not None:
            assert str(about_id) not in MEANING_AXIS_NAMES
        if family_id is not None:
            assert str(family_id) not in MEANING_AXIS_NAMES
