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


def _trace_entry(result: dict, primitive: str) -> dict:
    trace = result.get("trace", [])
    if not isinstance(trace, list):
        return {}
    for entry in trace:
        if isinstance(entry, dict) and entry.get("primitive") == primitive:
            return entry
    return {}


def _assert_qualification_observation(result: dict) -> None:
    ce = _trace_entry(result, "CE").get("ce_output", {})
    cex = _trace_entry(result, "CEx").get("cex_output", {})
    isc = _trace_entry(result, "ISc")
    qobs = isc.get("qualification_observation", {}) if isinstance(isc, dict) else {}

    assert isinstance(ce, dict), "CE trace output missing for qualification observation check"
    assert isinstance(cex, dict), "CEx trace output missing for qualification observation check"
    assert isinstance(qobs, dict), "qualification observation missing from ISc trace"
    assert qobs.get("qualification_evaluation_status") == "not_evaluated_predicate_open"

    candidate_set = ce.get("category_candidate_set", [])
    cue_values = ce.get("category_cue", [])
    cue_provenance = ce.get("cue_provenance", [])
    cex_provenance = cex.get("provenance", {})
    observed = qobs.get("candidates", [])
    assert isinstance(candidate_set, list), "CE candidate set must be a list"
    assert isinstance(observed, list), "qualification candidate observations must be a list"
    assert len(observed) == len(candidate_set), "qualification observation must include every CE candidate"

    cue_set = {str(value).strip().lower() for value in cue_values if str(value).strip()}
    for idx, candidate in enumerate(candidate_set):
        assert isinstance(candidate, dict), "CE candidate rows must be dictionaries"
        entry = observed[idx]
        assert isinstance(entry, dict), "qualification observation row must be a dictionary"
        major = str(candidate.get("major", "")).strip().lower()
        identity = entry.get("candidate_identity", {})
        evidence = entry.get("existing_evidence", {})
        provenance = entry.get("existing_evidence_provenance", {})

        assert isinstance(identity, dict), "candidate_identity must be a dictionary"
        assert isinstance(evidence, dict), "existing_evidence must be a dictionary"
        assert isinstance(provenance, dict), "existing_evidence_provenance must be a dictionary"

        assert identity.get("major") == major, "qualification observation candidate identity mismatch"
        assert evidence.get("f_s") == float(candidate.get("f_s", 0.0))
        assert evidence.get("f_b") == float(candidate.get("f_b", 0.0))
        assert evidence.get("f_e") == float(candidate.get("f_e", 0.0))
        assert evidence.get("f_i") == float(candidate.get("f_i", 0.0))
        assert evidence.get("in_current_category_cue") == (major in cue_set)
        assert provenance.get("ce_cue_provenance") == cue_provenance
        assert provenance.get("cex_provenance") == cex_provenance
        assert entry.get("qualification_evaluation_status") == "not_evaluated_predicate_open"
        assert entry.get("qualification_state") is None
        assert entry.get("qualification_rationale") is None


def main() -> None:
    baseline = run_pathA_short("The book is on the table.", enable_s2m_seed=True, enable_category_selection=False)
    baseline_meaning = baseline.get("s2m_meaning", {})
    assert baseline_meaning.get("meaning_relations") == [], "baseline no-cue must keep meaning_relations empty"
    _assert_qualification_observation(baseline)

    sentence_cue = run_pathA_short("Where is the book?", enable_s2m_seed=True, enable_category_selection=True)
    sentence_category = _committed_category(sentence_cue)
    assert sentence_category.get("category_cue") == ["perspectival"], "sentence cue should commit perspectival cue"
    assert sentence_category.get("top_category") == "perspectival", "sentence cue top category mismatch"
    sentence_meaning = sentence_cue.get("s2m_meaning", {})
    sentence_relations = sentence_meaning.get("meaning_relations", [])
    assert sentence_relations == [], "query cue should not force an extension without legitimation"
    _assert_qualification_observation(sentence_cue)

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
    _assert_qualification_observation(prior_cue)

    no_usable_cue = run_pathA_short(
        "The sky is blue.",
        enable_s2m_seed=True,
        enable_category_selection=True,
        prior_context=["This carries no category marker."],
    )
    no_usable_category = _committed_category(no_usable_cue)
    assert no_usable_category.get("category_cue") == [], "no usable cue should commit empty cue"
    assert no_usable_category.get("top_category") is None, "empty cue should commit top_category null"
    assert no_usable_category.get("provenance", {}).get("source") == [], "no usable cue should preserve empty provenance source"
    assert no_usable_cue.get("s2m_meaning", {}).get("meaning_relations") == []
    _assert_qualification_observation(no_usable_cue)

    refusal_case = run_pathA_short("Where is the book?", enable_s2m_seed=True, enable_category_selection=True)
    refusal_meaning = refusal_case.get("s2m_meaning", {})
    assert refusal_meaning.get("meaning_relations") == [], "query case should keep default-only composite"
    refusal_candidates = refusal_meaning.get("candidate_interpretations", [])
    assert any(
        isinstance(item, dict) and item.get("selection_state") == "refused"
        for item in refusal_candidates
    ), "refusal state should be visible for category-supported but unlicensed candidates"
    _assert_qualification_observation(refusal_case)

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
    a_qobs = _trace_entry(deterministic_a, "ISc").get("qualification_observation", {})
    b_qobs = _trace_entry(deterministic_b, "ISc").get("qualification_observation", {})
    assert a_qobs == b_qobs, "qualification observation must be deterministic"

    print("s2m category selection replay passed")


if __name__ == "__main__":
    main()
