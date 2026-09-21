from pathA_short_simulator import run_pathA_short


def main() -> None:
    # sentence = "The quick brown fox jumps over the lazy dog."
    # sentence = "The rain in Spain stays mainly in the plain."
    sentence = "Why is the sky blue?"
    result = run_pathA_short(sentence)

    print("=== Final TP ===")
    for k, v in result["final_tp"].items():
        print(f"{k}: {v}")

    print("\n=== Trace ===")
    bridge_mode_counts = {
        "committed": 0,
        "mixed": 0,
        "legacy": 0,
        "n/a": 0,
    }

    for step in result["trace"]:
        print(f"\n--- {step['primitive']} ---")
        print(f"notes: {step['notes']}")
        if "bridge_trace" in step:
            print("bridge_trace:", step["bridge_trace"])
            mode = str(step["bridge_trace"].get("mode", "n/a"))
            if mode in bridge_mode_counts:
                bridge_mode_counts[mode] += 1
            else:
                bridge_mode_counts["n/a"] += 1
        # NEW: print token-level relational mapping (Option A)
        if "token_relations" in step:
            print("token_relations:", step["token_relations"])
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

