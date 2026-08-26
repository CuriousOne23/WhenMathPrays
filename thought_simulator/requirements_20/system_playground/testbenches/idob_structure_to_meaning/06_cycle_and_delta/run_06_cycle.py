"""Slide 06 — Bounded search with named freeze."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.schema_load import load_yaml
from lib.vector6 import add_scaled, delta_l2, fmt, from_mapping, zeros

def _group_vector(group_id):
    data = load_yaml(ROOT / "02_meaning_groups" / "meaning_groups.slide.yaml")
    for group in data.get("meaning_groups") or []:
        if int(group.get("group_id")) == int(group_id):
            return from_mapping(group.get("group_dimensions"))
    return None

def _envelope(cie_id):
    data = load_yaml(ROOT / "05_cie" / "cie.examples.yaml")
    for env in data.get("envelopes") or []:
        if env.get("cie_id") == cie_id:
            return env
    return None

def run(group_id=1001, cie_id="physical_stance", clip_to_unit=True):
    stab = load_yaml(Path(__file__).parent / "stabilization.slide.yaml")["stabilization"]
    eps_m = float(stab["epsilon_meaning"])
    eps_i = float(stab["epsilon_identity"])
    min_c = int(stab["idob_search_budget_min"])
    max_c = int(stab["idob_search_budget_max"])
    M = _group_vector(group_id)
    env = _envelope(cie_id)
    print("=" * 64)
    print("LESSON 06 — CYCLE AND DELTA")
    print("Watch meaning_delta_h and identity_delta.")
    print("resolution_status is taken from the same predicate that halted.")
    print("=" * 64)
    if M is None or env is None:
        print(f"Missing group or CIE (group_id={group_id}, cie_id={cie_id})")
        return None
    alpha = float(env.get("identity_importance", 0))
    I = from_mapping(env.get("identity_vector"))
    I_prev = zeros()
    print(f"\nstart group_id={group_id} cie_id={cie_id} alpha={alpha}")
    print(f"eps_meaning={eps_m} eps_identity={eps_i} cycles={min_c}..{max_c}")
    print(f"M0: {fmt(M)}")
    status = "budget_exhausted"
    last_dh = last_di = 0.0
    used = 0
    for cycle in range(1, max_c + 1):
        used = cycle
        scale = alpha * (0.5 ** (cycle - 1))
        M_next = add_scaled(M, I, scale, clip=clip_to_unit)
        I_now = from_mapping({k: I[k] * (0.5 ** (cycle - 1)) for k in I})
        dh = delta_l2(M_next, M)
        di = delta_l2(I_now, I_prev)
        print(f"\ncycle {cycle}: scale={scale:.4f}")
        print(f"  M:              {fmt(M_next)}")
        print(f"  meaning_delta_h:{dh:.4f}")
        print(f"  identity_delta: {di:.4f}")
        M, I_prev = M_next, I_now
        last_dh, last_di = dh, di
        if cycle >= min_c and dh < eps_m:
            status = "stable"
            print("  halt: meaning delta below epsilon (stable)")
            break
        if cycle >= min_c and di < eps_i:
            status = "identity_stable"
            print("  halt: identity delta below epsilon (identity_stable)")
            break
        if cycle == max_c:
            status = "budget_exhausted"
            print("  halt: budget_exhausted")
    print(f"\nresolution_status: {status}")
    print(f"cycles used:       {used}")
    print("\nEnd lesson 06.\n")
    return {"M": M, "meaning_delta_h": last_dh, "identity_delta": last_di, "refinement_cycles": used, "resolution_status": status}

def main():
    run()

if __name__ == "__main__":
    main()
