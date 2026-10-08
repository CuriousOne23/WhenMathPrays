"""A command is not an action card. An exclamation is not a polar card."""

from pathA_short_simulator import run_pathA_short


def _active(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("activation_set") or [])


def main() -> None:
    command = _active("Close the door.")
    excl = _active("What a beautiful lamp!")
    polar = _active("Is the book on the table?")
    action = _active("The cat chased the mouse.")
    print("command", command)
    print("excl", excl)
    print("polar", polar)
    print("action", action)
    assert "imperative" in command
    assert "agent_action" not in command
    assert "exclamative" in excl
    assert "interrogative_polar" not in excl
    assert "interrogative_polar" in polar
    assert "agent_action" in action
    print("activation-guard-2 replay passed")


if __name__ == "__main__":
    main()
