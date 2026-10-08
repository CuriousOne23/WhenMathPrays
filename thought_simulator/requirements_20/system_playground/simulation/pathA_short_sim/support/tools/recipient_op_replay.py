"""A recipient hat writes a recipient op. A bare command does not."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    give = _ops("Give me the book.")
    command = _ops("Close the door.")
    print("give", give)
    print("command", command)
    assert "recipient" in give, give
    assert "recipient" not in command, command
    assert "bare_command" in command
    print("recipient-op replay passed")


if __name__ == "__main__":
    main()
