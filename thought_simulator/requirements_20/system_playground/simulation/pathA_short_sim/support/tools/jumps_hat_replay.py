"""Replay the jumps hat. A locative dog is not a patient."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    return {
        "roles": list(tp.get("struct_roles") or []),
        "cues": list(tp.get("semantic_adjacent_cues") or []),
        "core": packet.get("semantic_core") or {},
        "ops": list(packet.get("selected_ops") or []),
    }


def main() -> None:
    fox = _view("The quick brown fox jumps over the lazy dog.")
    plain = _view("The sky is blue.")
    print("fox", fox["roles"], fox["core"].get("action"), fox["cues"], fox["ops"])
    print("plain", plain["ops"])
    assert "action" in fox["roles"], fox
    assert fox["core"].get("action") == "jumps", fox
    assert "action_clause" in fox["cues"], fox
    assert "agent_action" in fox["ops"], fox
    assert fox["core"].get("patient", "") == "", fox
    assert "agent_action" not in plain["ops"]
    print("jumps-hat replay passed")


if __name__ == "__main__":
    main()
