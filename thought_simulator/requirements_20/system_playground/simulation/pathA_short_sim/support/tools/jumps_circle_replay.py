"""Replay the fox verb circle. Prenominal adjectives stay with the noun."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    return {
        "segments": list(tp.get("struct_segments") or []),
        "chunks": list(tp.get("segment_tokens") or []),
    }


def main() -> None:
    fox = _view("The quick brown fox jumps over the lazy dog.")
    why = _view("Why is the sky blue?")
    print("fox", fox)
    print("why", why["chunks"])
    assert ["jumps"] in fox["chunks"], fox
    assert "VP" in fox["segments"], fox
    assert any(chunk[:4] == ["the", "quick", "brown", "fox"] for chunk in fox["chunks"]), fox
    assert ["the", "sky"] in why["chunks"]
    assert ["blue"] in why["chunks"] or ["blue?"] in why["chunks"]
    print("jumps-circle replay passed")


if __name__ == "__main__":
    main()
