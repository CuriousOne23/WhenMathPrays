"""Slide 07 — Full crossing on official field names."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "04_ranking"))
sys.path.insert(0, str(ROOT / "06_cycle_and_delta"))
from lib.hash_toy import toy_structural_key
from lib.packet import empty_packet, print_packet
from lib.schema_load import load_yaml
import run_04_rank
import run_06_cycle

def run(card_id="S_rock_burst", cie_id="physical_stance", clip_to_unit=True):
    print("=" * 64)
    print("LESSON 07 — FULL IdOB SLIDE")
    print("One crossing: structure bounds candidates; identity moves M; freeze is named.")
    print("=" * 64)
    cards = load_yaml(ROOT / "01_structure" / "structure_card.examples.yaml").get("cards") or []
    card = next((c for c in cards if c.get("card_id") == card_id), None)
    groups = load_yaml(ROOT / "02_meaning_groups" / "meaning_groups.slide.yaml").get("meaning_groups") or []
    mapping = load_yaml(ROOT / "03_map_lookup" / "struct_to_meaning_map.slide.yaml").get("struct_to_meaning_map") or []
    packet = empty_packet()
    packet["card_id"] = card_id
    if card is None:
        packet["resolution_status"] = "time_exhausted"
        print_packet(packet)
        print("\nEnd lesson 07.\n")
        return packet
    key = toy_structural_key(card)
    packet["structural_hash"] = key
    print(f"\nstructure card {card_id}")
    print(f"structural_key {key}")
    print("CIE is not part of that key.")
    row = next((r for r in mapping if r.get("card_id") == card_id), None)
    candidates = list((row or {}).get("meaning_group_candidates") or [])
    packet["candidate_group_ids"] = candidates
    print(f"candidates {candidates}")
    if not candidates:
        print("Empty map: no legal meaning. Status must not pretend stable.")
        packet["resolution_status"] = "budget_exhausted"
        packet["ready_for_ouba"] = False
        print_packet(packet)
        print("\nEnd lesson 07.\n")
        return packet
    order = run_04_rank.run(card_id=card_id)
    packet["final_rank_order"] = order
    selected = order[0]
    packet["selected_group_id"] = selected
    group = next(g for g in groups if int(g["group_id"]) == int(selected))
    print(f"selected group {selected} {group.get('group_name')}")
    result = run_06_cycle.run(group_id=selected, cie_id=cie_id, clip_to_unit=clip_to_unit)
    if result:
        packet["meaning_semantics"] = result["M"]
        packet["meaning_delta_h"] = round(result["meaning_delta_h"], 4)
        packet["identity_delta"] = round(result["identity_delta"], 4)
        packet["refinement_cycles"] = result["refinement_cycles"]
        packet["resolution_status"] = result["resolution_status"]
        packet["ready_for_ouba"] = result["resolution_status"] in ("stable", "identity_stable")
    print_packet(packet)
    print("Truth/belief/OuBA were not computed. This bench stops at IdOB.")
    print("\nEnd lesson 07.\n")
    return packet

def main():
    run()

if __name__ == "__main__":
    main()
