"""Replay the command verb circle. The bare-command op stays."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "segments": list(tp.get("struct_segments") or []),
        "chunks": list(tp.get("segment_tokens") or []),
        "roles": list(tp.get("struct_roles") or []),
        "ops": list(packet.get("selected_ops") or []),
    }


def main() -> None:
    command = _view("Close the door.")
    plain = _view("The sky is blue.")
    print("command", command)
    print("plain", plain["segments"])
    assert command["chunks"][0] == ["close"], command
    assert "VP" in command["segments"]
    assert ["the", "door"] in command["chunks"]
    assert "bare_command" in command["ops"]
    assert plain["segments"] == ["NP", "CP", "AP"]
    print("command-circle replay passed")


if __name__ == "__main__":
    main()
