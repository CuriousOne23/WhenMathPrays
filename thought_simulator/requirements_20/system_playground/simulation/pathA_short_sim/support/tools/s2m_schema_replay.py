"""The connection schema and the closed relation list match the definition."""

import json
from pathlib import Path

import yaml


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "idob_schemas/s2m_connection.v1.schema.json").read_text())
    relations = yaml.safe_load((root / "s2m/relations.yaml").read_text())
    required = schema["$defs"]["connection"]["required"]
    status = schema["$defs"]["connection"]["properties"]["status"]["enum"]
    print("required", required)
    print("status", status)
    print("relations", relations["relations"])
    assert required == ["left", "relation", "right", "status"]
    assert status == ["supported", "missing"]
    assert "likelihood" not in schema["properties"]
    assert "ambiguous" not in status
    assert relations["relations"] == [
        "speaker", "reporting", "theme", "state", "location", "copula",
        "action", "patient", "recipient", "relative_subject", "query_focus", "adverb",
    ]
    print("s2m-schema replay passed")


if __name__ == "__main__":
    main()
