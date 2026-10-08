"""Replay the action-row floor. Does not change the example runner."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "segments": list(tp.get("struct_segments") or []),
        "cues": list(tp.get("semantic_adjacent_cues") or []),
        "ops": list(packet.get("selected_ops") or []),
    }


def main() -> None:
    action = _view("The cat chased the mouse.")
    plain = _view("The sky is blue.")
    command = _view("Close the door.")
    print("action", action)
    print("plain", plain)
    print("command", command)
    assert action["segments"] == ["NP", "VP", "NP"], action
    assert "action_clause" in action["cues"], action
    assert "agent_action" in action["ops"], action
    assert "agent_action" not in plain["ops"], plain
    assert "action_clause" not in plain["cues"], plain
    assert "bare_command" in command["ops"], command
    print("action-row replay passed")


if __name__ == "__main__":
    main()
