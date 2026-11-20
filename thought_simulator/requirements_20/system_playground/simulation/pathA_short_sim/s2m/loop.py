from typing import Any, Dict

from s2m.active_space import resolve_active_space
from s2m.legitimate import legitimate
from s2m.propose import propose
from s2m.record import build_record
from s2m.write import write_meaning_relations


def apply(seed: Dict[str, Any], space_name: str = "default") -> Dict[str, Any]:
    proposals = propose(seed)
    cues = seed.get("selection_cues", [])
    cue_active = isinstance(cues, list) and len(cues) > 0
    active_space = resolve_active_space(space_name) if cue_active else []
    legitimized = legitimate(proposals, active_space, cue_active=cue_active)
    meaning_relations = write_meaning_relations(legitimized)
    return build_record(seed, proposals, meaning_relations, active_space)

