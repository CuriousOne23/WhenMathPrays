"""The connection writer does not reopen the cut or invent a winner."""

import json
from pathlib import Path

import yaml

from idob.connections import connections_from_packet
from pathA_short_simulator import run_pathA_short


ROWS = [
    "The sky is blue.",
    "The book is on the table.",
    "The cat chased the mouse.",
    "The quick brown fox jumps over the lazy dog.",
    "The rain in Spain stays mainly in the plain.",
    "Where is the book?",
    "Why is the sky blue?",
    "Is the book on the table?",
    "Close the door.",
    "Please close the door.",
    "Give me the book.",
    "She said the book is on the table.",
    "The book that John bought.",
    "What a beautiful lamp!",
    "LLhfds pw Ppen qqoubx&",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "idob_schemas/s2m_connection.v1.schema.json").read_text())
    allowed = set(yaml.safe_load((root / "s2m/relations.yaml").read_text())["relations"])
    status_enum = set(schema["$defs"]["connection"]["properties"]["status"]["enum"])
    for raw in ROWS:
        tp = run_pathA_short(raw)["final_tp"]
        before = list(tp.get("struct_segments") or [])
        record = connections_from_packet(tp)
        after = list(tp.get("struct_segments") or [])
        print(raw, len(record["connections"]), len(record["holes"]))
        assert before == after
        assert set(record) == {"utterance", "connections", "holes", "notices"}
        assert "ambiguous" not in record["notices"]
        for item in record["connections"] + record["holes"]:
            assert item["status"] in status_enum
            assert "likelihood" not in item
            if item["status"] == "supported":
                assert item["relation"] in allowed
                assert item["left"]
    unknown = connections_from_packet(run_pathA_short("LLhfds pw Ppen qqoubx&")["final_tp"])
    assert unknown["connections"] == []
    assert len(unknown["holes"]) == 1
    said = connections_from_packet(run_pathA_short("She said the book is on the table.")["final_tp"])
    assert any(item["relation"] == "speaker" and item["left"] == "she" for item in said["connections"])
    print("s2m-connection replay passed")


if __name__ == "__main__":
    main()
