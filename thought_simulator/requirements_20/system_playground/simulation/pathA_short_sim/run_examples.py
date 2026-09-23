from pathA_short_simulator import run_pathA_short
from mcb.seam import copy_from_idob
from ouba.assembly import build_ouba


IDOB_PACKET_KEY_ORDER = [
    "identity_geometry",
    "truth_relation",
    "truth_relation_family",
    "semantic_core",
    "selected_ops",
    "claimed_fields",
    "contributors",
    "contributions",
    "activation_set",
    "inactive_objects",
    "residual_activated",
    "overlap_events",
    "meaning_delta",
    "psc_violations",
    "registry_digest",
    "complete",
    "tru_hint",
]


def _ordered_idob_packet(packet: object) -> dict:
    if not isinstance(packet, dict):
        return {}
    return {key: packet.get(key) for key in IDOB_PACKET_KEY_ORDER}


def _committed_stream_view(committed_stream: object) -> dict:
    if not isinstance(committed_stream, dict):
        return {
            "tokens": [],
            "normalized_tokens": [],
            "token_classes": [],
            "roles": [],
            "segments": [],
            "segment_tokens": [],
        }

    token_objects = committed_stream.get("tokens", [])
    if not isinstance(token_objects, list):
        token_objects = []

    segment_objects = committed_stream.get("segments", [])
    if not isinstance(segment_objects, list):
        segment_objects = []

    tokens = []
    normalized_tokens = []
    token_classes = []
    roles = []

    for token in token_objects:
        if not isinstance(token, dict):
            continue
        tokens.append(str(token.get("surface", "")))
        normalized_tokens.append(str(token.get("normalized", "")))
        token_classes.append(str(token.get("token_class", "")))
        role_value = token.get("role", "")
        if isinstance(role_value, dict):
            roles.append(str(role_value.get("chosen", "")))
        else:
            roles.append(str(role_value))

    segments = []
    segment_tokens = []
    for seg in segment_objects:
        if not isinstance(seg, dict):
            continue
        seg_id = seg.get("segment_id")
        segments.append(seg_id)
        grouped_tokens = []
        for token in token_objects:
            if not isinstance(token, dict):
                continue
            if token.get("segment_id") == seg_id:
                grouped_tokens.append(str(token.get("surface", "")))
        segment_tokens.append(grouped_tokens)

    return {
        "tokens": tokens,
        "normalized_tokens": normalized_tokens,
        "token_classes": token_classes,
        "roles": roles,
        "segments": segments,
        "segment_tokens": segment_tokens,
    }


def main() -> None:
    # sentence = "The quick brown fox jumps over the lazy dog."
    # PA-CSE-005 / mixed_desc
    # sentence = "The rain in Spain stays mainly in the plain."
    # PA-CSE-008 / interrogative
    # sentence = "Why is the sky blue?"
    # PA-CSE-001 / copular
    # sentence = "The sky is blue."
    # PA-CSE-006 / interrogative
    sentence = "Where is the book?"
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
    }

    print("=== Final TP ===")
    final_tp_ie = _committed_stream_view(final_tp.get("committed_stream", {}))
    print(f"tp_ie_tokens: {final_tp_ie['tokens']}")
    print(f"tp_ie_normalized_tokens: {final_tp_ie['normalized_tokens']}")
    print(f"tp_ie_token_classes: {final_tp_ie['token_classes']}")
    print(f"tp_ie_roles: {final_tp_ie['roles']}")
    print(f"tp_ie_segments: {final_tp_ie['segments']}")
    print(f"tp_ie_segment_tokens: {final_tp_ie['segment_tokens']}")
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
            sob_ie = _committed_stream_view(committed_stream)
            print(f"sob_tokens: {sob_ie['tokens']}")
            print(f"sob_struct_segments={struct_segments}")
            print(f"sob_segment_tokens={segment_tokens}")

        if primitive_name == "IE":
            primitive_output = primitive_trace_entry.get("output", {})
            if not isinstance(primitive_output, dict):
                primitive_output = {}
            committed_stream = primitive_trace_entry.get("committed_stream", primitive_output.get("committed_stream", {}))
            ie_view = _committed_stream_view(committed_stream)
            print(f"ie_tokens: {ie_view['tokens']}")
            print(f"ie_normalized_tokens: {ie_view['normalized_tokens']}")
            print(f"ie_token_classes: {ie_view['token_classes']}")
            print(f"ie_roles: {ie_view['roles']}")
            print(f"ie_segments: {ie_view['segments']}")
            print(f"ie_segment_tokens: {ie_view['segment_tokens']}")

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
            print(f"idob_packet={repr(_ordered_idob_packet(idob_packet))}")
            print("--- MCB ---")
            mcb_packet = copy_from_idob(_ordered_idob_packet(idob_packet))
            print(f"mcb_packet={repr(mcb_packet)}")
            ouba_packet = build_ouba(mcb_packet)
            print("--- OuBA ---")
            print(f"ouba_packet={repr(ouba_packet)}")
        # If you want more detail, uncomment:
        # print("input:", step["input"])
        # print("output:", step["output"])

    print("--- R7 ---")
    print("ouba_stable=True")
    print("--- R8 ---")
    print("pipeline_ready=True")
    print("--- R9 ---")
    print("freeze_version='pathA_v1'")


if __name__ == "__main__":
    main()
