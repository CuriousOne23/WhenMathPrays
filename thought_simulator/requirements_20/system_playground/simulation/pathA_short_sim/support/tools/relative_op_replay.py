"""A relative-subject hat writes its op. The head noun sentence does not."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    rel = _ops("The book that John bought.")
    plain = _ops("The book is on the table.")
    print("rel", rel)
    print("plain", plain)
    assert "relative_subject" in rel, rel
    assert "agent_action" in rel
    assert "relative_subject" not in plain, plain
    print("relative-op replay passed")


if __name__ == "__main__":
    main()
