"""A polar question claims its question. The declarative does not."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    polar = _claim("Is the book is on the table?")
    plain = _claim("The book is on the table.")
    print("polar", polar)
    print("plain", plain)
    assert polar == "is the book is on the table", polar
    assert plain == "the book is on the table"
    print("polar-claim replay passed")


if __name__ == "__main__":
    main()
