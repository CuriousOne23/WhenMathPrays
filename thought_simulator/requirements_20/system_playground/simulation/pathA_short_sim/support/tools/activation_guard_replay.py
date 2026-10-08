"""A card does not activate without its circle."""

from pathA_short_simulator import run_pathA_short


def _active(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("activation_set") or [])


def main() -> None:
    plain = _active("The sky is blue.")
    action = _active("The cat chased the mouse.")
    unknown = _active("LLhfds pw Ppen qqoubx&")
    print("plain", plain)
    print("action", action)
    print("unknown", unknown)
    assert "copular_state" in plain
    assert "agent_action" not in plain
    assert "modifier_resolution" not in plain
    assert "agent_action" in action
    assert "copular_state" not in action
    assert "agent_action" not in unknown
    assert "copular_state" not in unknown
    print("activation-guard replay passed")


if __name__ == "__main__":
    main()
