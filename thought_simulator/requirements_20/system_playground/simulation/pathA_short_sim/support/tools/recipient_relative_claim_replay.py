"""Recipient and relative-subject claims use hats already in the packet."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    give = _claim("Give me the book.")
    rel = _claim("The book that John bought.")
    command = _claim("Close the door.")
    print("give", give)
    print("rel", rel)
    print("command", command)
    assert give == "give me the book", give
    assert rel == "john bought the book", rel
    assert command == "close the door"
    print("recipient-relative claim replay passed")


if __name__ == "__main__":
    main()
