"""YAML activation trees are read. Empty trees still fall back.

from pathA_short_simulator import run_pathA_short


def _active(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("activation_set") or [])


def main() -> None:
    plain = _active("The sky is blue.")
    action = _active("The cat chased the mouse.")
    command = _active("Close the door.")
    polar = _active("Is the book on the table?")
    excl = _active("What a beautiful lamp!")
    print("plain", plain)
    print("action", action)
    print("command", command)
    print("polar", polar)
    print("excl", excl)
    assert "copular_state" in plain
    assert "agent_action" not in plain
    assert "agent_action" in action
    assert "imperative" in command
    assert "agent_action" not in command
    assert "interrogative_polar" in polar
    assert "exclamative" in excl
    assert "interrogative_polar" not in excl
    print("activation-tree replay passed")


if __name__ == "__main__":
    main()
