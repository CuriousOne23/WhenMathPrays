"""An asked empty end is a hole. A locative sentence does not invent a state hole."""

from idob.connections import connections_from_packet
from pathA_short_simulator import run_pathA_short


def _holes(raw: str) -> list:
    return connections_from_packet(run_pathA_short(raw)["final_tp"])["holes"]


def main() -> None:
    unknown_state = _holes("The sky is zyzzyx.")
    loc = _holes("The book is on the table.")
    plain = _holes("The sky is blue.")
    print("unknown_state", unknown_state)
    print("loc", loc)
    print("plain", plain)
    assert any(item["relation"] == "state" and item["status"] == "missing" for item in unknown_state)
    assert all(item["relation"] != "state" for item in loc)
    assert plain == []
    print("s2m-missing-hole replay passed")


if __name__ == "__main__":
    main()
