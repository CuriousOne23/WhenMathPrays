"""Replay the three form holes. The plain locative must not grow them."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    return {
        "segments": list(tp.get("struct_segments") or []),
        "segment_tokens": list(tp.get("segment_tokens") or []),
        "roles": list(tp.get("struct_roles") or []),
    }


def main() -> None:
    plain = _view("The book is on the table.")
    reporting = _view("She said the book is on the table.")
    recipient = _view("Give me the book.")
    relative = _view("The book that John bought.")
    print("plain", plain)
    print("reporting", reporting)
    print("recipient", recipient)
    print("relative", relative)

    assert "REPORT" not in plain["segments"], plain
    assert "RECIP" not in plain["segments"], plain
    assert "relative_subject" not in plain["roles"], plain
    assert "recipient" not in plain["roles"], plain

    assert "REPORT" in reporting["segments"], reporting
    book_at = reporting["segment_tokens"].index(["the", "book"])
    report_at = reporting["segments"].index("REPORT")
    assert report_at != book_at, reporting

    assert "RECIP" in recipient["segments"], recipient
    recip_at = recipient["segments"].index("RECIP")
    assert recipient["roles"][recip_at] == "recipient", recipient
    book_at = recipient["segment_tokens"].index(["the", "book"])
    assert recipient["roles"][book_at] != "recipient", recipient

    john_at = relative["segment_tokens"].index(["john"])
    book_at = relative["segment_tokens"].index(["the", "book"])
    assert relative["roles"][john_at] == "relative_subject", relative
    assert relative["roles"][book_at] != "relative_subject", relative
    print("form-hole replay passed")


if __name__ == "__main__":
    main()
