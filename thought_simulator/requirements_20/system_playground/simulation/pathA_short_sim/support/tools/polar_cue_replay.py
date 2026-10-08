"""Replay the polar cue. A wh-question and a declarative do not grow it."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "cues": list(tp.get("semantic_adjacent_cues") or []),
        "ops": list(packet.get("selected_ops") or []),
        "core": packet.get("semantic_core") or {},
    }


def main() -> None:
    polar = _view("Is the book on the table?")
    where = _view("Where is the book?")
    plain = _view("The book is on the table.")
    print("polar", polar["cues"], polar["ops"], polar["core"].get("location"))
    print("where", where["cues"], where["core"].get("query_focus"))
    print("plain", plain["cues"], plain["ops"])
    assert "polar_question" in polar["cues"], polar
    assert "polar_question" in polar["ops"], polar
    assert polar["core"].get("location") == "on the table"
    assert "polar_question" not in where["cues"]
    assert where["core"].get("query_focus") == "where"
    assert "polar_question" not in plain["cues"]
    assert "polar_question" not in plain["ops"]
    print("polar-cue replay passed")


if __name__ == "__main__":
    main()
