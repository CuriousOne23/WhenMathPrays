from pathA_short_simulator import run_pathA_short


def main() -> None:
    sentence = "The quick brown fox jumps over the lazy dog."
    result = run_pathA_short(sentence)

    print("=== Final TP ===")
    for k, v in result["final_tp"].items():
        print(f"{k}: {v}")

    print("\n=== Trace ===")
    for step in result["trace"]:
        print(f"\n--- {step['primitive']} ---")
        print(f"notes: {step['notes']}")
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


if __name__ == "__main__":
    main()

