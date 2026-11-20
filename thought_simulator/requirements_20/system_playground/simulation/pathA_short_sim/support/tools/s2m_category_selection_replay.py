"""Replay for category-cue scoring and S2M selection boundaries."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pathA_short_simulator import run_pathA_short


def _committed_category(result: dict) -> dict:
    final_tp = result.get("final_tp", {})
    semantic = final_tp.get("semantic", {}) if isinstance(final_tp, dict) else {}
    return semantic.get("isc_category_result", {}) if isinstance(semantic, dict) else {}


def main() -> None:
    baseline = run_pathA_short("The book is on the table.", enable_s2m_seed=True, enable_category_selection=False)
    baseline_meaning = baseline.get("s2m_meaning", {})
    assert baseline_meaning.get("meaning_relations") == [], "baseline no-cue must keep meaning_relations empty"

    sentence_cue = run_pathA_short("Where is the book?", enable_s2m_seed=True, enable_category_selection=True)
    sentence_category = _committed_category(sentence_cue)
    assert sentence_category.get("category_cue") == ["perspectival"], "sentence cue should commit perspectival cue"
    assert sentence_category.get("top_category") == "perspectival", "sentence cue top category mismatch"
    sentence_meaning = sentence_cue.get("s2m_meaning", {})
    sentence_relations = sentence_meaning.get("meaning_relations", [])
    assert sentence_relations == [], "query cue should not force an extension without legitimation"

    prior_cue = run_pathA_short(
        "The book is on the table.",
        enable_s2m_seed=True,
        enable_category_selection=True,
        prior_context=["That location needs support for the object."],
    )
    prior_category = _committed_category(prior_cue)
    prior_cues = prior_category.get("category_cue", [])
    assert isinstance(prior_cues, list) and "physical" in prior_cues, "prior cue should include physical"
    prior_meaning = prior_cue.get("s2m_meaning", {})
    prior_relations = prior_meaning.get("meaning_relations", [])
    prior_keys = {
        (
            str(item.get("from", "")),
            str(item.get("relation", "")),
            str(item.get("to", "")),
            str(item.get("major", "")),
        )
        for item in prior_relations
        if isinstance(item, dict)
    }
    assert ("table", "provides", "support", "physical") in prior_keys
    assert ("book", "is", "object", "physical") in prior_keys

    no_usable_prior = run_pathA_short(
        "The book is on the table.",
        enable_s2m_seed=True,
        enable_category_selection=True,
        prior_context=["This carries no category marker."],
    )
    no_usable_category = _committed_category(no_usable_prior)
    assert no_usable_category.get("category_cue") == [], "no usable prior cue should commit empty cue"
    assert no_usable_category.get("top_category") is None, "empty cue should commit top_category null"
    assert no_usable_prior.get("s2m_meaning", {}).get("meaning_relations") == []

    refusal_case = run_pathA_short("Where is the book?", enable_s2m_seed=True, enable_category_selection=True)
    refusal_meaning = refusal_case.get("s2m_meaning", {})
    assert refusal_meaning.get("meaning_relations") == [], "query case should keep default-only composite"
    refusal_candidates = refusal_meaning.get("candidate_interpretations", [])
    assert any(
        isinstance(item, dict) and item.get("selection_state") == "refused"
        for item in refusal_candidates
    ), "refusal state should be visible for category-supported but unlicensed candidates"

    deterministic_a = run_pathA_short(
        "The book is on the table.",
        enable_s2m_seed=True,
        enable_category_selection=True,
        prior_context=["cold signal in prior context"],
    )
    deterministic_b = run_pathA_short(
        "The book is on the table.",
        enable_s2m_seed=True,
        enable_category_selection=True,
        prior_context=["cold signal in prior context"],
    )
    a_category = _committed_category(deterministic_a)
    b_category = _committed_category(deterministic_b)
    assert a_category == b_category, "category envelope should be deterministic"
    a_dump = json.dumps(a_category, sort_keys=False)
    b_dump = json.dumps(b_category, sort_keys=False)
    assert a_dump == b_dump, "category serialization order should be deterministic"

    print("s2m category selection replay passed")


if __name__ == "__main__":
    main()
