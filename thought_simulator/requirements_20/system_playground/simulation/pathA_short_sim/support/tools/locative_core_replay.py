"""Replay locative core fill. Unknown string must stay claim-empty."""

from idob.mapping import map_packet
from pathA_short_simulator import run_pathA_short


def _run(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "roles": list(tp.get("struct_roles") or []),
        "core": packet.get("semantic_core") or {},
        "meaning": map_packet(tp),
    }


def main() -> None:
    loc = _run("The book is on the table.")
    plain = _run("The sky is blue.")
    unknown = _run("LLhfds pw Ppen qqoubx&")
    print("loc", loc["roles"], loc["core"].get("theme"), loc["core"].get("location"), loc["meaning"]["status"])
    print("plain", plain["core"].get("theme"), plain["core"].get("state"), plain["core"].get("location"))
    print("unknown", unknown["meaning"]["status"], unknown["core"].get("location"))
    assert loc["core"].get("theme") == "the book", loc
    assert loc["core"].get("location") == "on the table", loc
    assert "location" in loc["roles"], loc
    assert loc["meaning"]["status"] == "mapped"
    assert plain["core"].get("state") == "blue"
    assert not str(plain["core"].get("location") or "").strip()
    assert unknown["meaning"]["status"] == "claim_empty"
    print("locative-core replay passed")


if __name__ == "__main__":
    main()
