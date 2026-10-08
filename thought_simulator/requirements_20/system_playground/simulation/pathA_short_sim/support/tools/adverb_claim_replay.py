"""An adverb stays an adverb and enters the claim."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    core = (tp.get("idob") or {}).get("semantic_core") or {}
    return {"roles": list(tp.get("struct_roles") or []), "adverb": core.get("adverb", ""), "claim": claim_from_packet(tp)["claim"]}


def main() -> None:
    rain = _view("The rain in Spain stays mainly in the plain.")
    plain = _view("The sky is blue.")
    print("rain", rain)
    print("plain", plain["adverb"], plain["claim"])
    assert rain["adverb"] == "mainly", rain
    assert "adverb" in rain["roles"]
    assert rain["claim"] == "the rain stays mainly in spain in the plain", rain
    assert not str(plain["adverb"]).strip()
    assert plain["claim"] == "the sky is blue"
    print("adverb-claim replay passed")


if __name__ == "__main__":
    main()
