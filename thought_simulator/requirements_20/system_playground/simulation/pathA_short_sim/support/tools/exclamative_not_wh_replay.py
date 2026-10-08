"""An exclamation is not a wh-question."""

from pathA_short_simulator import run_pathA_short


def _view(raw: str) -> dict:
    tp = run_pathA_short(raw)["final_tp"]
    packet = tp.get("idob") or {}
    core = packet.get("semantic_core") or {}
    return {
        "roles": list(tp.get("struct_roles") or []),
        "ops": list(packet.get("selected_ops") or []),
        "query_focus": core.get("query_focus", ""),
    }


def main() -> None:
    excl = _view("What a beautiful lamp!")
    what = _view("What is the book?")
    print("excl", excl)
    print("what", what)
    assert "exclamative_force" in excl["ops"], excl
    assert "query_focus" not in excl["ops"], excl
    assert not str(excl["query_focus"]).strip()
    assert "query_focus" in what["ops"], what
    assert what["query_focus"] == "what"
    print("exclamative-not-wh replay passed")


if __name__ == "__main__":
    main()
