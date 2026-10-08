"""A locative sentence writes a location op. A copular sentence does not."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    loc = _ops("The book is on the table.")
    plain = _ops("The sky is blue.")
    print("loc", loc)
    print("plain", plain)
    assert "location" in loc, loc
    assert "location" not in plain, plain
    print("location-op replay passed")


if __name__ == "__main__":
    main()
