from typing import Any, Dict

from s2m.loop import apply as apply_loop


def apply_meaning(tp: Any, seed: Dict[str, Any]) -> Dict[str, Any]:
    """Additive meaning transfer from the seed trail."""
    _ = tp
    if not isinstance(seed, dict):
        return {
            "meaning_relations": [],
            "active_space": [],
            "story_id": "s2m-story-001",
            "extendable": True,
        }
    return apply_loop(seed)

