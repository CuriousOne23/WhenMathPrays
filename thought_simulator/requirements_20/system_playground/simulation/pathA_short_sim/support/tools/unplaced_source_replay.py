"""Unplaced differences have floor sources. They are not structure IDs."""

from idob.crossing import crossing_from_packet
from pathA_short_simulator import run_pathA_short


def main() -> None:
    said = run_pathA_short("She said the book is on the table.")["final_tp"]
    book = run_pathA_short("The book is on the table.")["final_tp"]
    where = run_pathA_short("Where is the book?")["final_tp"]
    shell = crossing_from_packet(said)
    print("said roles", said.get("struct_roles"))
    print("book roles", book.get("struct_roles"))
    print("where roles", where.get("struct_roles"))
    assert "speaker" in (said.get("struct_roles") or [])
    assert "speaker" not in (book.get("struct_roles") or [])
    assert "query_focus" in (where.get("struct_roles") or [])
    assert "query_focus" not in (book.get("struct_roles") or [])
    assert shell.get("speaker_id", "absent") == "absent"
    assert shell.get("query_id", "absent") == "absent"
    assert shell.get("structural_key") is None
    print("unplaced-source replay passed")


if __name__ == "__main__":
    main()
