"""Reporting and request claims use packet ops. They do not invent a speaker."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    said = _claim("She said the book is on the table.")
    please = _claim("Please close the door.")
    command = _claim("Close the door.")
    print("said", said)
    print("please", please)
    print("command", command)
    assert said == "she said the book on the table", said
    assert please == "please close", please
    assert command == "close"
    print("report-request claim replay passed")


if __name__ == "__main__":
    main()
