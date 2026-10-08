"""A wh-question writes its own op. A polar question does not steal it."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    where = _ops("Where is the book?")
    polar = _ops("Is the book on the table?")
    plain = _ops("The sky is blue.")
    print("where", where)
    print("polar", polar)
    print("plain", plain)
    assert "query_focus" in where, where
    assert "query_focus" not in polar, polar
    assert "polar_question" in polar
    assert "query_focus" not in plain
    print("wh-op replay passed")


if __name__ == "__main__":
    main()
