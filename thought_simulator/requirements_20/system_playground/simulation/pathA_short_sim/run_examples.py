from pathA_short_simulator import run_pathA_short


def main() -> None:
    # sentence = "The quick brown fox jumps over the lazy dog."
    # sentence = "The rain in Spain stays mainly in the plain."
    sentence = "Why is the sky blue?"
    simulation_result = run_pathA_short(sentence)
    final_tp = simulation_result["final_tp"]

    idob_packet = final_tp.get("idob_packet", final_tp.get("idob", {}))
    truth_relation = final_tp.get("truth_relation", "")
    semantic_core = idob_packet.get("semantic_core", []) if isinstance(idob_packet, dict) else []

    canonical_final_tp = {
        "struct_segments": final_tp.get("struct_segments", []),
        "segment_tokens": final_tp.get("segment_tokens", []),
        "struct_roles": final_tp.get("struct_roles", []),
        "constraints_matched": final_tp.get("constraints_matched", []),
        "constraints_unmatched": final_tp.get("constraints_unmatched", []),
        "constraint_residue": final_tp.get("constraint_residue", []),
        "smoothing_operations": final_tp.get("smoothing_operations", []),
        "semantic_adjacent_cues": final_tp.get("semantic_adjacent_cues", []),
        "basin_residue": final_tp.get("basin_residue", final_tp.get("smoothing_residue", [])),
        "truth_relation": truth_relation,
        "semantic_core": semantic_core,
        "idob_packet": idob_packet if isinstance(idob_packet, dict) else {},
    }

    print("=== Final TP ===")
    for k, v in canonical_final_tp.items():
        print(f"{k}: {v}")

    print("\n=== Trace ===")

    for primitive_trace_entry in simulation_result["trace"]:
        print(f"\n--- {primitive_trace_entry['primitive']} ---")

        primitive_name = primitive_trace_entry["primitive"]
        if primitive_name == "SOB":
            primitive_output = primitive_trace_entry.get("output", {})
            if not isinstance(primitive_output, dict):
                primitive_output = {}

            struct_segments = primitive_trace_entry.get("struct_segments", primitive_output.get("struct_segments", []))
            segment_tokens = primitive_trace_entry.get("segment_tokens", primitive_output.get("segment_tokens", []))
            committed_stream = primitive_trace_entry.get("committed_stream", primitive_output.get("committed_stream", {}))
            raw_tokens = []
            if isinstance(committed_stream, dict):
                token_objects = committed_stream.get("tokens", [])
                if isinstance(token_objects, list):
                    raw_tokens = [
                        t["normalized"]
                        for t in token_objects
                        if isinstance(t, dict) and "normalized" in t
                    ]
            print("tokens:", raw_tokens)
            print(f"struct_segments={struct_segments}")
            print(f"segment_tokens={segment_tokens}")

        if primitive_name == "SROB":
            struct_roles = primitive_trace_entry.get("struct_roles", [])
            print(f"struct_roles={struct_roles}")

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

        if primitive_name == "IdOB":
            idob_packet = primitive_trace_entry.get("idob_packet", {})
            idob_semantic_core = []
            idob_truth_relation = ""
            if isinstance(idob_packet, dict):
                idob_semantic_core = idob_packet.get("semantic_core", [])
                idob_truth_relation = idob_packet.get("truth_relation", "")
            print(f"idob_packet={idob_packet if isinstance(idob_packet, dict) else {}}")
            print(f"semantic_core={idob_semantic_core if isinstance(idob_semantic_core, list) else []}")
            print(f"truth_relation={idob_truth_relation}")
        # If you want more detail, uncomment:
        # print("input:", step["input"])
        # print("output:", step["output"])


if __name__ == "__main__":
    main()

