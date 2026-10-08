"""Falsify the six structure IDs against the floor. Write no ID value."""

from typing import Dict, List

from idob.crossing import crossing_from_packet
from pathA_short_simulator import run_pathA_short


IDS = (
    "semantic_field_id",
    "semantic_role_id",
    "semantic_object_id",
    "gradient_id",
    "universe_id",
    "subfield_id",
)

QUESTIONS = {
    "semantic_field_id": "different field?",
    "semantic_role_id": "different hat?",
    "semantic_object_id": "different object?",
    "gradient_id": "",
    "universe_id": "",
    "subfield_id": "",
}

UNPLACED = (
    ("speaker against theme", "She said the book is on the table.", "The book is on the table."),
    ("query against statement", "Where is the book?", "The book is on the table."),
)


def _verdict(name: str) -> str:
    if not QUESTIONS[name]:
        return "missing_dimension"
    return "unsupported"


def _floor_differs(left: str, right: str) -> bool:
    a = run_pathA_short(left)["final_tp"]
    b = run_pathA_short(right)["final_tp"]
    return list(a.get("struct_roles") or []) != list(b.get("struct_roles") or [])


def evaluate() -> Dict[str, object]:
    sample = crossing_from_packet(run_pathA_short("The sky is blue.")["final_tp"])
    rows: List[Dict[str, str]] = []
    for name in IDS:
        rows.append({
            "id": name,
            "question": QUESTIONS[name] or "none stated",
            "source": "none",
            "value": "null" if sample.get(name) is None else "present",
            "verdict": _verdict(name),
        })
    unplaced = []
    for label, left, right in UNPLACED:
        if _floor_differs(left, right):
            unplaced.append({"difference": label, "verdict": "unplaced"})
    return {
        "rows": rows,
        "unplaced": unplaced,
        "structural_key": sample.get("structural_key"),
        "meaning_semantics": sample.get("meaning_semantics"),
    }


def main() -> None:
    report = evaluate()
    for row in report["rows"]:
        print(row["id"], row["verdict"], row["question"])
    for item in report["unplaced"]:
        print("unplaced", item["difference"])
    print("key", report["structural_key"], "M", report["meaning_semantics"])


if __name__ == "__main__":
    main()
