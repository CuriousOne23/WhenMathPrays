"""A reporting hat writes a reporting op. A plain locative does not."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    said = _ops("She said the book is on the table.")
    plain = _ops("The book is on the table.")
    print("said", said)
    print("plain", plain)
    assert "reporting" in said, said
    assert "location" in said
    assert "reporting" not in plain, plain
    print("reporting-op replay passed")


if __name__ == "__main__":
    main()
