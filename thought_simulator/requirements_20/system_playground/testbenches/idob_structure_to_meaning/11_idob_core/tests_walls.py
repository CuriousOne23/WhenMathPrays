"""Wall tests for idob.py. Run: python tests_walls.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from idob import run_hop


def _ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    return cond


def main():
    failed = 0
    empty = run_hop(card_id="S_unmapped")
    failed += not _ok("empty map has no winner", empty.get("selected_group_id") is None and empty.get("meaning_semantics") is None)
    failed += not _ok("empty map status", empty.get("resolution_status") == "empty_map")

    rock = run_hop(card_id="S_rock_burst", cie_id="physical_stance")
    cands = set(rock.get("candidate_group_ids") or [])
    order = rock.get("final_rank_order") or []
    failed += not _ok("rank subset of map", set(order) <= cands and bool(order))

    a = run_hop(card_id="S_rock_burst", cie_id="physical_stance")
    b = run_hop(card_id="S_rock_burst", cie_id="scientific_stance")
    failed += not _ok("CIE does not change key", a.get("structural_key") == b.get("structural_key") and a.get("structural_key"))

    miss = run_hop(utterance="zzzzq no cue at all", packs_loaded=["base_en"])
    failed += not _ok("09 miss unassigned", miss.get("resolution_status") == "unassigned" and miss.get("structural_key") is None)

    failed += not _ok("next_key not invented", rock.get("next_key") is None)

    r1 = run_hop(card_id="S_rock_burst", cie_id="neutral")
    r2 = run_hop(card_id="S_rock_burst", cie_id="neutral")
    failed += not _ok("replay equal", r1 == r2)

    print("\nfailed:", failed)
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
