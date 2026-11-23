from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple


def _obligation_key(obligation: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        str(obligation.get("source_item_id", "")),
        str(obligation.get("obligation_type", "")),
        str(obligation.get("identity_key", "")),
    )


def _find_classification(item_id: str, classifications: List[Dict[str, Any]]) -> str:
    for entry in classifications:
        if entry.get("item_id") == item_id:
            return str(entry.get("classification", "unresolved"))
    return "unresolved"


def compute_obligations(
    items: List[Dict[str, Any]],
    classifications: List[Dict[str, Any]],
    dependencies: List[Dict[str, Any]],
    discovered: Dict[str, Any],
) -> List[Dict[str, Any]]:
    obligations: List[Dict[str, Any]] = []
    licensed_extensions = discovered.get("licensed_extensions", {})
    licensed_pairs: Set[Tuple[str, str, str]] = set()
    if isinstance(licensed_extensions, dict):
        for value in licensed_extensions.values():
            if isinstance(value, list):
                for triplet in value:
                    if isinstance(triplet, (tuple, list)) and len(triplet) == 3:
                        licensed_pairs.add((str(triplet[0]), str(triplet[1]), str(triplet[2])))

    for item in items:
        item_id = item["item_id"]
        resource_class = item["resource_class"]
        identity = item["identity"]
        classification = _find_classification(item_id, classifications)
        if classification == "already_defined":
            continue

        if resource_class == "seed":
            obligations.append(
                {
                    "source_item_id": item_id,
                    "resource_class": resource_class,
                    "obligation_type": "seed_generalization_unresolved",
                    "identity_key": identity.get("seed_key", "seed"),
                    "derived_surface": "historical_unresolved",
                    "requires_qualification": False,
                }
            )
            continue

        if resource_class == "dictionary_entry":
            scope = identity["scope"]
            marker = identity["marker"]
            major = identity["major"]
            obligations.append(
                {
                    "source_item_id": item_id,
                    "resource_class": resource_class,
                    "obligation_type": "dictionary_mapping_expansion",
                    "identity_key": f"{scope}:{marker}:{major}",
                    "derived_surface": "category_cue_relation",
                    "requires_qualification": True,
                }
            )
            continue

        if resource_class == "association":
            endpoint = identity["endpoint"]
            relation = identity["relation"]
            target = identity["to"]
            major = identity["major"]
            subcategory = identity.get("subcategory", "")
            relation_identity = f"{endpoint}:{relation}:{target}:{major}:{subcategory}"
            obligations.append(
                {
                    "source_item_id": item_id,
                    "resource_class": resource_class,
                    "obligation_type": "association_expansion",
                    "identity_key": relation_identity,
                    "derived_surface": "candidate",
                    "requires_qualification": True,
                }
            )
            obligations.append(
                {
                    "source_item_id": item_id,
                    "resource_class": "candidate",
                    "obligation_type": "candidate_reachability",
                    "identity_key": relation_identity,
                    "candidate": {
                        "from": endpoint,
                        "relation": relation,
                        "to": target,
                        "major": major,
                        "subcategory": subcategory,
                    },
                    "licensed_scaffold_observation": {
                        "tuple_present_in_licensed_extensions": (endpoint, relation, target) in licensed_pairs,
                        "note": "bounded scaffold observation only; no generalized licensing rule inferred",
                    },
                    "derived_surface": "candidate",
                    "requires_qualification": True,
                }
            )
            continue

        if resource_class == "major":
            major = identity["major"]
            obligations.append(
                {
                    "source_item_id": item_id,
                    "resource_class": resource_class,
                    "obligation_type": "major_eligibility_change",
                    "identity_key": major,
                    "derived_surface": "reference_dimension",
                    "requires_qualification": True,
                }
            )

    # Remove accidental duplicates while preserving order.
    deduped: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str, str]] = set()
    for obligation in obligations:
        key = _obligation_key(obligation)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(obligation)
    return deduped

