"""Replay the please circle. A bare command does not grow it."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "segments": list(tp.get("struct_segments") or []),
        "chunks": list(tp.get("segment_tokens") or []),
        "ops": list(packet.get("selected_ops") or []),
    }


def main() -> None:
    request = _view("Please close the door.")
    command = _view("Close the door.")
    print("request", request)
    print("command", command["segments"], command["ops"])
    assert ["please"] in request["chunks"], request
    assert "REQ" in request["segments"]
    assert ["close"] in request["chunks"]
    assert "polite_request" in request["ops"]
    assert "REQ" not in command["segments"]
    assert "bare_command" in command["ops"]
    print("please-circle replay passed")


if __name__ == "__main__":
    main()
