"""Slide 11 — print one-hop IdOB packet."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from idob import run_hop
from lib.vector6 import fmt


def _print(pkt):
    print(f"\ncard_id:                 {pkt.get('card_id')}")
    print(f"utterance:               {pkt.get('utterance')}")
    print(f"packs_loaded:            {pkt.get('packs_loaded')}")
    print(f"assignment_status:       {pkt.get('assignment_status')}")
    print(f"structural_key:          {pkt.get('structural_key')}")
    print(f"residue_code:            {pkt.get('residue_code')}")
    print(f"candidate_group_ids:     {pkt.get('candidate_group_ids')}")
    print(f"final_rank_order:        {pkt.get('final_rank_order')}")
    print(f"selected_group_id:       {pkt.get('selected_group_id')}")
    print(f"cie_id:                  {pkt.get('cie_id')}")
    M = pkt.get("meaning_semantics")
    Mp = pkt.get("meaning_semantics_prime")
    print(f"meaning_semantics M0:    {fmt(M) if M else None}")
    print(f"meaning_semantics M':    {fmt(Mp) if Mp else None}")
    print(f"meaning_delta_h:         {pkt.get('meaning_delta_h')}")
    print(f"identity_delta:          {pkt.get('identity_delta')}")
    print(f"refinement_cycles:       {pkt.get('refinement_cycles')}")
    print(f"resolution_status:       {pkt.get('resolution_status')}")
    print(f"ready_for_ouba:          {pkt.get('ready_for_ouba')}")
    print(f"expand_target:           {pkt.get('expand_target')}")
    print(f"next_key:                {pkt.get('next_key')}")
    print("key rewritten by CIE:    NO")


def run(card_id="S_rock_burst", utterance=None, packs_loaded=None, cie_id="physical_stance", clip_to_unit=True):
    print("=" * 64)
    print("LESSON 11 — IDOB CORE")
    print("One hop orchestrator. Not RB. Not Path A product IdOB.")
    print("=" * 64)
    if utterance is not None:
        pkt = run_hop(utterance=utterance, packs_loaded=packs_loaded, cie_id=cie_id, clip_to_unit=clip_to_unit)
    else:
        ids = [card_id] if card_id else ["S_rock_burst", "S_deadline_friday", "S_sleepy", "S_unmapped"]
        if card_id:
            ids = [card_id]
        for cid in ids:
            _print(run_hop(card_id=cid, cie_id=cie_id, clip_to_unit=clip_to_unit))
        print("\nEnd lesson 11.\n")
        return
    _print(pkt)
    print("\nEnd lesson 11.\n")


def main():
    run()


if __name__ == "__main__":
    main()
