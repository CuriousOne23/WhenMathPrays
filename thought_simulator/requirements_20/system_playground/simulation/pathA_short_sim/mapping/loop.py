from typing import Any, Dict, List

from stores.further_utterance import propose as propose_further_utterance
from stores.legitimation_refusal import propose as propose_legitimation_refusal
from stores.linguistic_context import propose as propose_linguistic_context
from stores.social_situational_frame import propose as propose_social_situational_frame
from stores.time_sequence import propose as propose_time_sequence
from stores.world_view import propose as propose_world_view


def collect_proposals(active_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    proposals: List[Dict[str, Any]] = []
    for proposer in (
        propose_further_utterance,
        propose_world_view,
        propose_social_situational_frame,
        propose_linguistic_context,
        propose_legitimation_refusal,
        propose_time_sequence,
    ):
        proposed = proposer(active_context)
        if proposed:
            proposals.extend(proposed)
    return proposals
