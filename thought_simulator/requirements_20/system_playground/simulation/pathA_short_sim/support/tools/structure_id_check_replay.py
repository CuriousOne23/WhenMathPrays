"""Guardrail. No invented ID, no key, no missing verdict."""

from structure_id_eval import IDS, evaluate


def main() -> None:
    report = evaluate()
    print("rows", [(row["id"], row["verdict"]) for row in report["rows"]])
    print("unplaced", report["unplaced"])
    assert [row["id"] for row in report["rows"]] == list(IDS)
    assert all(row["value"] == "null" for row in report["rows"])
    assert report["structural_key"] is None
    assert report["meaning_semantics"] is None
    verdicts = {row["id"]: row["verdict"] for row in report["rows"]}
    assert verdicts["semantic_field_id"] == "unsupported"
    assert verdicts["semantic_role_id"] == "unsupported"
    assert verdicts["semantic_object_id"] == "unsupported"
    assert verdicts["gradient_id"] == "missing_dimension"
    assert verdicts["universe_id"] == "missing_dimension"
    assert verdicts["subfield_id"] == "missing_dimension"
    assert "separated" not in verdicts.values()
    labels = [item["difference"] for item in report["unplaced"]]
    assert "speaker against theme" in labels
    assert "query against statement" in labels
    print("structure-id falsification replay passed")


if __name__ == "__main__":
    main()
