"""An unknown string is not a noun circle."""

from idob.mapping import map_packet
from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    return {
        "segments": list(tp.get("struct_segments") or []),
        "chunks": list(tp.get("segment_tokens") or []),
        "meaning": map_packet(tp),
    }


def main() -> None:
    unknown = _view("LLhfds pw Ppen qqoubx&")
    plain = _view("The sky is blue.")
    print("unknown", unknown["segments"], unknown["chunks"], unknown["meaning"]["status"])
    print("plain", plain["segments"])
    assert unknown["segments"] == [], unknown
    assert unknown["meaning"]["status"] == "claim_empty"
    assert plain["segments"] == ["NP", "CP", "AP"], plain
    print("unknown-not-np replay passed")


if __name__ == "__main__":
    main()
