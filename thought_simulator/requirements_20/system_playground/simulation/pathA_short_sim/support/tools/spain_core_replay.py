"""Replay the mixed descriptive core. mainly is not a state."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "chunks": list(tp.get("segment_tokens") or []),
        "roles": list(tp.get("struct_roles") or []),
        "core": packet.get("semantic_core") or {},
    }


def main() -> None:
    mixed = _view("The rain in Spain stays mainly in the plain.")
    plain = _view("The sky is blue.")
    print("mixed", mixed["chunks"], mixed["roles"], mixed["core"].get("theme"), mixed["core"].get("location"), mixed["core"].get("state"))
    print("plain", plain["core"].get("state"))
    assert mixed["core"].get("theme") == "the rain", mixed
    assert "in spain" in str(mixed["core"].get("location"))
    assert "in the plain" in str(mixed["core"].get("location"))
    assert mixed["core"].get("state") == "stays", mixed
    assert "mainly" not in str(mixed["core"].get("state"))
    assert plain["core"].get("state") == "blue"
    print("spain-core replay passed")


if __name__ == "__main__":
    main()
