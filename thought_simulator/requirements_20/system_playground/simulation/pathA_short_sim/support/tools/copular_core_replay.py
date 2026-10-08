"""Replay copular core fill. Unknown string must stay claim-empty."""

from idob.mapping import map_packet
from pathA_short_simulator import run_pathA_short


def _run(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    core = packet.get("semantic_core") or {}
    return {
        "segments": list(tp.get("struct_segments") or []),
        "roles": list(tp.get("struct_roles") or []),
        "core": core,
        "meaning": map_packet(tp),
    }


def main() -> None:
    plain = _run("The sky is blue.")
    unknown = _run("LLhfds pw Ppen qqoubx&")
    print("plain", plain["roles"], plain["core"].get("theme"), plain["core"].get("state"), plain["meaning"]["status"])
    print("unknown", unknown["roles"], unknown["core"].get("theme"), unknown["meaning"]["status"])
    assert plain["core"].get("theme") == "the sky", plain
    assert plain["core"].get("state") == "blue", plain
    assert plain["meaning"]["status"] == "mapped"
    assert unknown["meaning"]["status"] == "claim_empty"
    assert not str(unknown["core"].get("theme") or "").strip()
    print("copular-core replay passed")


if __name__ == "__main__":
    main()
