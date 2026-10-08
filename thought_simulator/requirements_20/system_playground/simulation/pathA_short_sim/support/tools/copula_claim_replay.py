"""A locative claim keeps the copula the packet already wrote."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    loc = _claim("The book is on the table.")
    polar = _claim("Is the book on the table?")
    plain = _claim("The sky is blue.")
    print("loc", loc)
    print("polar", polar)
    print("plain", plain)
    assert loc == "the book is on the table", loc
    assert polar == "is the book on the table"
    assert plain == "the sky is blue"
    print("copula-claim replay passed")


if __name__ == "__main__":
    main()
