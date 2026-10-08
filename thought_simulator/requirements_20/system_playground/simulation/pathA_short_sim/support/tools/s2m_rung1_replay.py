"""Replay the readable claim. Structure is unchanged. M is not computed."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _run(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    before = list(tp.get("struct_segments") or [])
    claim = claim_from_packet(tp)
    after = list(tp.get("struct_segments") or [])
    return {"before": before, "after": after, "claim": claim}


def main() -> None:
    plain = _run("The sky is blue.")
    loc = _run("The book is on the table.")
    action = _run("The cat chased the mouse.")
    unknown = _run("LLhfds pw Ppen qqoubx&")
    print("plain", plain["claim"])
    print("loc", loc["claim"])
    print("action", action["claim"])
    print("unknown", unknown["claim"])
    for row in (plain, loc, action, unknown):
        assert row["before"] == row["after"]
        assert "M" not in row["claim"]
    assert plain["claim"]["claim"] == "the sky is blue"
    assert loc["claim"]["claim"] == "the book is on the table"
    assert action["claim"]["claim"] == "the cat chased the mouse"
    assert unknown["claim"]["status"] == "claim_empty"
    assert unknown["claim"]["claim"] == ""
    print("s2m rung1 replay passed")


if __name__ == "__main__":
    main()
