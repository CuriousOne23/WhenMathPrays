"""The loader rejects a family the schema does not name."""

from idob.registry import _ensure_valid_object_schema_shape, _load_schema, SCHEMA_PATH


def main() -> None:
    schema = _load_schema(SCHEMA_PATH)
    bad = {"name": "not_a_card", "schema_ref": "idob_object.v1", "family": "not_a_family"}
    try:
        _ensure_valid_object_schema_shape(bad, schema)
    except ValueError as exc:
        print("rejected", exc)
        assert "not_a_family" in str(exc)
    else:
        raise SystemExit("bad family was accepted")
    print("schema-enum replay passed")


if __name__ == "__main__":
    main()
