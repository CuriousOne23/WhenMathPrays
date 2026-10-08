"""A copular state writes a state op. A locative sentence does not invent one."""

from pathA_short_simulator import run_pathA_short


def _ops(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("selected_ops") or [])


def main() -> None:
    plain = _ops("The sky is blue.")
    loc = _ops("The book is on the table.")
    print("plain", plain)
    print("loc", loc)
    assert "state" in plain, plain
    assert "state" not in loc, loc
    assert "location" in loc
    print("state-op replay passed")


if __name__ == "__main__":
    main()
