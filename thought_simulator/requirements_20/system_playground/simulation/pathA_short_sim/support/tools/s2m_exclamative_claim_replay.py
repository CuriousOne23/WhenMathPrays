"""An exclamation claims its theme. A wh-question does not use that wording."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    excl = _claim("What a beautiful lamp!")
    what = _claim("What is the book?")
    print("excl", excl)
    print("what", what)
    assert excl == "exclamative a beautiful lamp", excl
    assert what == "what is the book"
    print("exclamative-claim replay passed")


if __name__ == "__main__":
    main()
