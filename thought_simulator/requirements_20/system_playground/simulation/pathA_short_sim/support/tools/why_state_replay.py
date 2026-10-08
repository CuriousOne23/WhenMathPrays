"""Replay the glued why-question split. Prenominal adjectives stay in the noun circle."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "segments": list(tp.get("struct_segments") or []),
        "chunks": list(tp.get("segment_tokens") or []),
        "core": packet.get("semantic_core") or {},
    }


def main() -> None:
    why = _view("Why is the sky blue?")
    plain = _view("The sky is blue.")
    fox = _view("The quick brown fox jumps over the lazy dog.")
    print("why", why["segments"], why["chunks"], why["core"].get("query_focus"), why["core"].get("theme"), why["core"].get("state"))
    print("plain", plain["chunks"], plain["core"].get("theme"), plain["core"].get("state"))
    print("fox", fox["chunks"])
    assert why["core"].get("query_focus") == "why"
    assert ["the", "sky"] in why["chunks"] or ["the", "sky", "blue?"] not in why["chunks"]
    assert any(chunk[0].lower().strip("?.!") == "blue" and len(chunk) == 1 for chunk in why["chunks"]), why
    assert why["core"].get("state") == "blue", why
    assert why["core"].get("theme") == "the sky", why
    assert plain["core"].get("theme") == "the sky"
    assert plain["core"].get("state") == "blue"
    assert any(chunk[:3] == ["the", "quick", "brown"] for chunk in fox["chunks"]), fox
    print("why-state replay passed")


if __name__ == "__main__":
    main()
