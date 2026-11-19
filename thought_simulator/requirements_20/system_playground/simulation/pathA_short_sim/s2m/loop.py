from typing import Dict

from s2m.active_space import resolve_active_space
from s2m.legitimate import legitimate
from s2m.propose import propose
from s2m.record import build_record
from s2m.write import write_meaning_relations


def apply(seed: Dict[str, Any], space_name: str = "default") -> Dict[str, Any]:
    active_space = resolve_active_space(space_name)
    proposals = propose(seed)
    legitimized = legitimate(proposals, active_space)
    meaning_relations = write_meaning_relations(legitimized)
    return build_record(seed, meaning_relations, active_space)

