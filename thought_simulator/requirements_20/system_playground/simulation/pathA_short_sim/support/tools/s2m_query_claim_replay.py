"""A wh-question claims its focus and theme. A declarative does not gain a query."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    tp = run_pathA_short(raw)["final_tp"]
    return claim_from_packet(tp)["claim"]


def main() -> None:
    where = _claim("Where is the book?")
    plain = _claim("The sky is blue.")
    print("where", where)
    print("plain", plain)
    assert where == "where is the book", where
    assert plain == "the sky is blue"
    print("query-claim replay passed")


if __name__ == "__main__":
    main()
