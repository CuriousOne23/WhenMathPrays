"""Wall tests for idob.py. Run: python tests_walls.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from idob import process, run_hop
from lib.vector6 import zeros


def _ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    return cond


def main():
    failed = 0
    empty = run_hop(card_id="S_unmapped")
    failed += not _ok("empty map has no winner", empty.get("selected_group_id") is None and empty.get("meaning_semantics") is None)
    failed += not _ok("empty map status", empty.get("resolution_status") == "empty_map")
    failed += not _ok("empty map residual", (empty.get("identity_residual") or {}).get("pattern") == "empty_map")

    rock = run_hop(card_id="S_rock_burst", cie_id="physical_stance")
    cands = set(rock.get("candidate_group_ids") or [])
    order = rock.get("final_rank_order") or []
    failed += not _ok("rank subset of map", set(order) <= cands and bool(order))
    failed += not _ok("first pass flag", rock.get("first_meaning_cycle") is True)
    failed += not _ok("before is zeros", rock.get("meaning_semantics_before") == zeros())
    failed += not _ok("rock leftover residual", (rock.get("identity_residual") or {}).get("pattern") == "leftover")
    failed += not _ok("rock not path_b_eligible", rock.get("path_b_eligible") is False)
    failed += not _ok("ready_for_ouba on birth", rock.get("ready_for_ouba") is True)
    failed += not _ok("hold formation", rock.get("hold_geometry") == "formation")
    failed += not _ok("routing flag false", rock.get("routing_filter_mutated") is False)

    a = run_hop(card_id="S_rock_burst", cie_id="physical_stance")
    b = run_hop(card_id="S_rock_burst", cie_id="scientific_stance")
    failed += not _ok("CIE does not change key", a.get("structural_key") == b.get("structural_key") and a.get("structural_key"))

    prior = run_hop(card_id="S_deadline_friday", cie_id="neutral", prior_M=a.get("meaning_semantics_prime"))
    failed += not _ok("prior_M not first cycle", prior.get("first_meaning_cycle") is False)

    miss = run_hop(utterance="zzzzq no cue at all", packs_loaded=["base_en"])
    failed += not _ok("09 miss unassigned", miss.get("resolution_status") == "unassigned" and miss.get("structural_key") is None)

    failed += not _ok("next_key not invented", rock.get("next_key") is None)

    r1 = run_hop(card_id="S_rock_burst", cie_id="neutral")
    r2 = run_hop(card_id="S_rock_burst", cie_id="neutral")
    failed += not _ok("replay equal", r1 == r2)

    tp = {"process": {"routing_filter": {"keep": True}}, "card_id": "S_sleepy"}
    out = process(tp, cie_id="neutral")
    failed += not _ok("process keeps routing_filter", out.get("process", {}).get("routing_filter") == {"keep": True})
    failed += not _ok("process write-boundary", out.get("idob", {}).get("routing_filter_mutated") is False)
    failed += not _ok("sleepy eligible", out.get("idob", {}).get("path_b_eligible") is True)

    print("\nfailed:", failed)
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
