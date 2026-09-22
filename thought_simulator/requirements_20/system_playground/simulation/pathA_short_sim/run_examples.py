from pathA_short_simulator import run_pathA_short


def main() -> None:
    # sentence = "The quick brown fox jumps over the lazy dog."
    # sentence = "The rain in Spain stays mainly in the plain."
    sentence = "Why is the sky blue?"
    simulation_result = run_pathA_short(sentence)

    print("=== Final TP ===")
    for k, v in simulation_result["final_tp"].items():
        print(f"{k}: {v}")

    print("\n=== Trace ===")
    bridge_mode_counts = {
        "committed": 0,
        "mixed": 0,
        "legacy": 0,
        "n/a": 0,
    }

    for primitive_trace_entry in simulation_result["trace"]:
        print(f"\n--- {primitive_trace_entry['primitive']} ---")
        print(f"notes: {primitive_trace_entry['notes']}")
        if "bridge_trace" in primitive_trace_entry:
            print("bridge_trace:", primitive_trace_entry["bridge_trace"])
            mode = str(primitive_trace_entry["bridge_trace"].get("mode", "n/a"))
            if mode in bridge_mode_counts:
                bridge_mode_counts[mode] += 1
            else:
                bridge_mode_counts["n/a"] += 1
        # NEW: print token-level relational mapping (Option A)
        if "token_relations" in primitive_trace_entry:
            print("token_relations:", primitive_trace_entry["token_relations"])

        # Batch 6 transition: emit canonical external keys while legacy notes remain.
        primitive_name = primitive_trace_entry["primitive"]
        if primitive_name == "CnOB":
            constraints_matched = primitive_trace_entry.get("constraints_matched", [])
            constraints_unmatched = primitive_trace_entry.get("constraints_unmatched", [])
            constraint_residue = primitive_trace_entry.get("constraint_residue", [])
            print(f"constraints_matched={constraints_matched}")
            print(f"constraints_unmatched={constraints_unmatched}")
            print(f"constraint_residue={constraint_residue}")

        if primitive_name == "SmOB":
            smoothing_operations = primitive_trace_entry.get("smoothing_operations", [])
            semantic_adjacent_cues = primitive_trace_entry.get("semantic_adjacent_cues", [])
            basin_residue = primitive_trace_entry.get("basin_residue", [])
            print(f"smoothing_operations={smoothing_operations}")
            print(f"semantic_adjacent_cues={semantic_adjacent_cues}")
            print(f"basin_residue={basin_residue}")
        # If you want more detail, uncomment:
        # print("input:", step["input"])
        # print("output:", step["output"])

    print("\n=== Simulator Capability Summary ===")
    print("CnOB: constraint matching, residue extraction (implemented)")
    print("SmOB: smoothing operations, semantic-adjacent cues (implemented)")
    print("Routing: minimal IdOB selection (implemented)")
    print("IdOB: agent_action, action_patient, relation_modifier, modifier_resolution")
    print("Not yet implemented: full IdOB family, MCB, provenance envelopes, routing entropy")
    print("This simulator demonstrates relational geometry but is not full Path-A.")
    print("Trace now includes token-level relational mapping for CnOB, SmOB, and IdOB (Option A).")

    print("\n=== Bridge Usage Summary ===")
    print(f"committed: {bridge_mode_counts['committed']}")
    print(f"mixed: {bridge_mode_counts['mixed']}")
    print(f"legacy: {bridge_mode_counts['legacy']}")
    print(f"n/a: {bridge_mode_counts['n/a']}")


if __name__ == "__main__":
    main()

