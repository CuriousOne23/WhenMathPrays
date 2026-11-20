"""Replay for the canonical three-sentence S2M default-meaning contract."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pathA_short_simulator import run_pathA_short


def _assert_no_cue_default_only(
    sentence: str,
    relation: str,
    source: str,
    target: str,
    expected_description_fragment: str,
    expected_candidates: set[tuple[str, str, str, str]],
) -> None:
    result = run_pathA_short(sentence, enable_s2m_seed=True)
    seed = result.get("s2m_seed")
    meaning = result.get("s2m_meaning")

    assert isinstance(seed, dict), f"missing seed for: {sentence}"
    assert isinstance(meaning, dict), f"missing meaning for: {sentence}"

    written_relations = seed.get("written_relations")
    assert isinstance(written_relations, list) and written_relations, f"missing structure for: {sentence}"
    first = written_relations[0]
    assert isinstance(first, dict)
    assert first.get("from") == source, sentence
    assert first.get("relation") == relation, sentence
    assert first.get("to") == target, sentence

    default_meaning = meaning.get("default_meaning")
    assert isinstance(default_meaning, dict), sentence
    assert default_meaning.get("from") == source, sentence
    assert default_meaning.get("relation") == relation, sentence
    assert default_meaning.get("to") == target, sentence
    assert expected_description_fragment in str(default_meaning.get("description", "")), sentence

    assert meaning.get("meaning_relations") == [], f"no-cue run selected meaning for: {sentence}"

    candidates = meaning.get("candidate_interpretations")
    assert isinstance(candidates, list), sentence
    actual_candidates = {
        (
            str(item.get("from", "")),
            str(item.get("relation", "")),
            str(item.get("to", "")),
            str(item.get("major", "")),
        )
        for item in candidates
        if isinstance(item, dict)
    }
    assert expected_candidates.issubset(actual_candidates), sentence


def main() -> None:
    _assert_no_cue_default_only(
        sentence="The sky is blue.",
        relation="is",
        source="sky",
        target="blue",
        expected_description_fragment="state/property blue",
        expected_candidates={
            ("sky", "affords", "openness", "mental"),
            ("blue", "evokes", "cold", "affective"),
        },
    )
    _assert_no_cue_default_only(
        sentence="The book is on the table.",
        relation="is_on",
        source="book",
        target="table",
        expected_description_fragment="located on the entity table",
        expected_candidates={
            ("book", "is", "object", "physical"),
            ("table", "provides", "support", "physical"),
        },
    )
    _assert_no_cue_default_only(
        sentence="Where is the book?",
        relation="queries_location_of",
        source="query_location",
        target="book",
        expected_description_fragment="requested locative continuation remains unresolved/potential",
        expected_candidates={
            ("book", "is", "object", "physical"),
            ("query_location", "requests", "information-request", "mental"),
            ("query_location", "carries", "unresolved-location", "perspectival"),
        },
    )
    print("s2m canonical sentences replay passed")


if __name__ == "__main__":
    main()
