"""Replay for optional S2M seed without mutating tp.idob."""

from pprint import pformat
from pathlib import Path
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

    assert control.idob == seeded.idob, "tp.idob changed when S2M seed flag enabled"
    assert not hasattr(control, "s2m_seed"), "control run unexpectedly created s2m_seed"

    seed = getattr(seeded, "s2m_seed", None)
    assert isinstance(seed, dict), "seed run did not create tp.s2m_seed"
    assert seed.get("utterance") == utterance
    assert seed.get("seed_complete") is True

    written_relations = seed.get("written_relations")
    assert isinstance(written_relations, list)
    assert len(written_relations) == 1
    assert written_relations[0] == {
        "from": "sky",
        "relation": "is",
        "to": "blue",
        "source": "floor",
    }

    null_relations = seed.get("null_relations")
    assert isinstance(null_relations, list) and null_relations
    assert isinstance(null_relations[0], dict)

    crossing_fields = seed.get("crossing_fields")
    assert isinstance(crossing_fields, dict)
    assert set(crossing_fields.keys()) == {
        "structure_ids",
        "structural_key",
        "rank",
        "meaning_semantics",
        "cie_id",
        "meaning_delta_h",
    }
    assert all(value is None for value in crossing_fields.values())

    print("s2m_seed:")
    print(pformat(seed, width=100))
    print("seed replay passed")


if __name__ == "__main__":
    main()
