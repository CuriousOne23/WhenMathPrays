"""Replay for S2M Part I + Part II without mutating tp.idob."""

from pathlib import Path
from pprint import pformat
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pathA_short_simulator import PRIMITIVES
from tp_substrate import TP, init_tp


def _run(raw_text: str, enable_seed: bool) -> TP:
    tp = init_tp(raw_text)
    if enable_seed:
        tp.enable_s2m_seed = True
    for primitive in PRIMITIVES:
        tp = primitive(tp)
    return tp


def main() -> None:
    utterance = "The sky is blue."
    control = _run(utterance, enable_seed=False)
    seeded = _run(utterance, enable_seed=True)

    assert control.idob == seeded.idob, "tp.idob changed when S2M flag enabled"
    assert not hasattr(control, "s2m_seed"), "control run unexpectedly created tp.s2m_seed"
    assert not hasattr(control, "s2m_meaning"), "control run unexpectedly created tp.s2m_meaning"

    seed = getattr(seeded, "s2m_seed", None)
    assert isinstance(seed, dict), "seed run did not create tp.s2m_seed"
    assert seed.get("seed_complete") is True

    meaning = getattr(seeded, "s2m_meaning", None)
    assert isinstance(meaning, dict), "seed run did not create tp.s2m_meaning"
    assert meaning.get("extendable") is True
    assert meaning.get("story_id") == "sky-blue-001"
    assert meaning.get("active_space") == ["affective", "perceptual", "mental", "spiritual"]

    meaning_relations = meaning.get("meaning_relations")
    assert isinstance(meaning_relations, list)
    relation_keys = {
        (
            str(item.get("from", "")),
            str(item.get("relation", "")),
            str(item.get("to", "")),
            str(item.get("major", "")),
            bool(item.get("legitimized", False)),
        )
        for item in meaning_relations
        if isinstance(item, dict)
    }
    assert ("blue", "evokes", "cold", "affective", True) in relation_keys
    assert ("sky", "affords", "openness", "mental", True) in relation_keys

    print("s2m_seed:")
    print(pformat(seed, width=100))
    print("s2m_meaning:")
    print(pformat(meaning, width=100))
    print("s2m meaning replay passed")


if __name__ == "__main__":
    main()

