"""Replay query-focus fill. A declarative must not grow one."""

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
    where = _run("Where is the book?")
    why = _run("Why is the sky blue?")
    plain = _run("The sky is blue.")
    polar = _run("Is the book on the table?")
    unknown = _run("LLhfds pw Ppen qqoubx&")
    print("where", where["roles"], where["core"].get("query_focus"), where["core"].get("theme"))
    print("why", why["core"].get("query_focus"), why["core"].get("theme"), why["core"].get("state"))
    print("plain", plain["core"].get("query_focus"))
    print("polar", polar["core"].get("query_focus"), polar["core"].get("location"))
    print("unknown", unknown["meaning"]["status"])
    assert where["core"].get("query_focus") == "where", where
    assert where["core"].get("theme") == "the book"
    assert why["core"].get("query_focus") == "why"
    assert why["core"].get("state") == "blue"
    assert not str(plain["core"].get("query_focus") or "").strip()
    assert not str(polar["core"].get("query_focus") or "").strip()
    assert polar["core"].get("location") == "on the table"
    assert unknown["meaning"]["status"] == "claim_empty"
    print("query-core replay passed")


if __name__ == "__main__":
    main()
