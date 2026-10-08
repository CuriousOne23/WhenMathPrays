"""The old helper op is not a claim."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    polar = _ops("Is the book on the table?")
    action = _ops("The cat chased the mouse.")
    plain = _ops("The sky is blue.")
    print("polar", polar)
    print("action", action)
    print("plain", plain)
    assert "polar_question" in polar
    assert "modifier_resolution" not in polar
    assert "agent_action" in action
    assert "modifier_resolution" not in action
    assert "modifier_resolution" not in plain
    print("helper-op replay passed")


if __name__ == "__main__":
    main()
