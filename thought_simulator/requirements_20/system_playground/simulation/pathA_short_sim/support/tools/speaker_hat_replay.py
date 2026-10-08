"""The speaker hat comes from the packet. A plain locative does not grow one."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    core = (tp.get("idob") or {}).get("semantic_core") or {}
    return {"roles": list(tp.get("struct_roles") or []), "speaker": core.get("speaker", ""), "claim": claim_from_packet(tp)["claim"]}


def main() -> None:
    said = _view("She said the book is on the table.")
    plain = _view("The book is on the table.")
    print("said", said)
    print("plain", plain["speaker"], plain["claim"])
    assert said["speaker"] == "she", said
    assert said["claim"] == "she said the book is on the table", said
    assert not str(plain["speaker"]).strip()
    assert plain["claim"] == "the book is on the table"
    print("speaker-hat replay passed")


if __name__ == "__main__":
    main()
