"""Residual is always on. Modifier and mixed stay off ordinary sentences."""

from pathA_short_simulator import run_pathA_short


def _active(raw: str) -> list:
    tp = run_pathA_short(raw)["final_tp"]
    return list((tp.get("idob") or {}).get("activation_set") or [])


def main() -> None:
    plain = _active("The sky is blue.")
    unknown = _active("LLhfds pw Ppen qqoubx&")
    print("plain", plain)
    print("unknown", unknown)
    assert "residual_identity" in plain
    assert "modifier_resolution" not in plain
    assert "mixed_descriptive" not in plain
    assert unknown == ["residual_identity"], unknown
    print("activation-tree-3 replay passed")


if __name__ == "__main__":
    main()
