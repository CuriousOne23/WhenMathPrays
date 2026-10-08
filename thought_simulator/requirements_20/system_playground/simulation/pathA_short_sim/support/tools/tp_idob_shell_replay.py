"""The shell copies the sum and leaves crossing fields null."""

from idob.crossing import crossing_from_packet
from pathA_short_simulator import run_pathA_short


def main() -> None:
    plain_tp = run_pathA_short("The sky is blue.")["final_tp"]
    before = list(plain_tp.get("struct_segments") or [])
    plain = crossing_from_packet(plain_tp)
    unknown = crossing_from_packet(run_pathA_short("LLhfds pw Ppen qqoubx&")["final_tp"])
    print("plain M", plain["meaning_semantics"], "ids", plain["structure_ids"])
    print("unknown holes", unknown["connection_witness"]["holes"])
    assert before == list(plain_tp.get("struct_segments") or [])
    assert plain["meaning_semantics"] is None
    assert plain["meaning_delta_h"] is None
    assert plain["cie_id"] is None
    assert plain["final_rank_order"] is None
    assert plain["structure_ids"] is None
    assert plain["semantic_core"]
    assert unknown["connections"] if False else unknown["connection_witness"]["connections"] == []
    assert unknown["connection_witness"]["holes"]
    print("tp.idob shell replay passed")


if __name__ == "__main__":
    main()
