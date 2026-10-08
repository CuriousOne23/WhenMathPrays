"""Locative and wh trees are read. An exclamation does not activate wh."""

from pathA_short_simulator import run_pathA_short


def _active(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("activation_set") or [])


def main() -> None:
    loc = _active("The book is on the table.")
    where = _active("Where is the book?")
    excl = _active("What a beautiful lamp!")
    plain = _active("The sky is blue.")
    print("loc", loc)
    print("where", where)
    print("excl", excl)
    print("plain", plain)
    assert "locative" in loc
    assert "locative" not in plain
    assert "interrogative_wh" in where
    assert "interrogative_wh" not in excl
    print("activation-tree-2 replay passed")


if __name__ == "__main__":
    main()
