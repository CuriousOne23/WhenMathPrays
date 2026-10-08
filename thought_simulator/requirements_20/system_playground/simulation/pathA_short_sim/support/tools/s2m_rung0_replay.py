"""Replay the first mapping rung. Structure must be unchanged."""

from idob.mapping import map_packet
from pathA_short_simulator import run_pathA_short


def _run(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    before = list(tp.get("struct_segments") or [])
    meaning = map_packet(tp)
    after = list(tp.get("struct_segments") or [])
    return {"before": before, "after": after, "meaning": meaning}


def main() -> None:
    plain = _run("The sky is blue.")
    action = _run("The cat chased the mouse.")
    unknown = _run("LLhfds pw Ppen qqoubx&")
    print("plain", plain["meaning"]["status"], plain["before"])
    print("action", action["meaning"]["status"], action["meaning"]["selected_ops"])
    print("unknown", unknown["meaning"]["status"], unknown["before"])
    for row in (plain, action, unknown):
        assert row["before"] == row["after"], row
        assert row["meaning"]["structure_reopened"] is False
        assert "M" not in row["meaning"]
    assert plain["meaning"]["status"] == "mapped"
    assert plain["meaning"]["semantic_core"].get("theme") == "the sky"
    assert plain["meaning"]["semantic_core"].get("state") == "blue"
    assert plain["meaning"]["truth_relation"] == "declarative"
    assert "agent_action" in action["meaning"]["selected_ops"]
    assert action["meaning"]["status"] == "mapped"
    assert unknown["meaning"]["status"] == "claim_empty"
    print("s2m rung0 replay passed")


if __name__ == "__main__":
    main()
