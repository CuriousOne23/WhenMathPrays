"""Toy structural key. Deterministic. Meaning-blind. Not the production TS hash."""


def toy_structural_key(ids):
    if isinstance(ids, dict):
        ordered = (
            ids.get("semantic_field_id", ids.get("field")),
            ids.get("semantic_role_id", ids.get("role")),
            ids.get("semantic_object_id", ids.get("obj", ids.get("object"))),
            ids.get("gradient_id", ids.get("gradient")),
            ids.get("universe_id", ids.get("universe")),
            ids.get("subfield_id", ids.get("subfield")),
        )
    else:
        ordered = tuple(ids)
    return "SK|" + "|".join(str(x) for x in ordered)
