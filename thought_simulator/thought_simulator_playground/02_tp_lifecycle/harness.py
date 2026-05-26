"""Deterministic verification harness for 02_tp_lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import traceback

from prototype import EntropyComponents, ThoughtPoint


MODULE_NAME = "02_tp_lifecycle"
ARTIFACT_PATH = Path("tp_lifecycle_harness_artifact.json")


REQ = {
    "creation_identity": {
        "hlr": "HLR-ARCH-08",
        "llr": "LLR-T-DET-01",
        "doc": "thought_simulator_req/10_architecture/08_TS_data_model.md",
        "section": "§3.1",
    },
    "movement_state": {
        "hlr": "HLR-ARCH-07",
        "llr": "LLR-T-OBS-01",
        "doc": "thought_simulator_req/10_architecture/07_TS_state_machine.md",
        "section": "§3, §14",
    },
    "entropy_bounds": {
        "hlr": "HLR-REQ-14",
        "llr": "LLR-T-CON-02",
        "doc": "thought_simulator_req/20_requirements/14_testing_and_validation.md",
        "section": "§8",
    },
    "split_merge_provenance": {
        "hlr": "HLR-ARCH-07",
        "llr": "LLR-T-LVL-02",
        "doc": "thought_simulator_req/10_architecture/07_TS_state_machine.md",
        "section": "§8",
    },
    "determinism": {
        "hlr": "HLR-REQ-14",
        "llr": "LLR-T-DET-01,T-DET-04",
        "doc": "thought_simulator_req/20_requirements/14_testing_and_validation.md",
        "section": "§4",
    },
}


@dataclass
class ScenarioResult:
    name: str
    status: str
    requirement_key: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        req = REQ[self.requirement_key]
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "hlr_ref": req["hlr"],
            "llr_ref": req["llr"],
            "req_doc": req["doc"],
            "req_section": req["section"],
        }


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _emit_requirement(requirement_key: str) -> None:
    req = REQ[requirement_key]
    print(
        f"REQ ATTACHMENT | HLR={req['hlr']} | LLR={req['llr']} | "
        f"DOC={req['doc']} | SECTION={req['section']}"
    )


def scenario_creation_movement_entropy() -> tuple[ScenarioResult, ThoughtPoint]:
    _emit_requirement("creation_identity")
    tp = ThoughtPoint.new(
        basin_id="OB_identity",
        entropy=EntropyComponents(h_rep=1.2, h_pred=0.9, h_struct=0.8),
        embedding=[0.10, 0.20, 0.40],
        created_at_tick=0,
        energy=1.0,
        deterministic_mode=True,
        deterministic_nonce=1,
    )
    _assert(tp.state_counter == 1, "state_counter must start at 1 after creation event")
    _assert(tp.current_basin_id == "OB_identity", "initial basin mismatch")

    _emit_requirement("movement_state")
    start_counter = tp.state_counter
    tp.move_to_basin("RB_relation", tick=1, note="OB -> RB transition")
    _assert(tp.current_basin_id == "RB_relation", "move_to_basin did not update basin")
    _assert(tp.state_counter == start_counter + 1, "move_to_basin did not bump state_counter")

    _emit_requirement("entropy_bounds")
    before = tp.entropy.total
    tp.update_entropy(tick=2, d_rep=-0.4, d_pred=-0.2, d_struct=-0.1)
    _assert(tp.entropy.h_rep >= 0 and tp.entropy.h_pred >= 0 and tp.entropy.h_struct >= 0, "entropy became negative")
    _assert(tp.entropy.total <= before, "expected entropy reduction in scenario")

    return (
        ScenarioResult(
            name="creation_movement_entropy",
            status="PASS",
            requirement_key="movement_state",
            detail="Creation, basin movement, and bounded entropy update succeeded.",
        ),
        tp,
    )


def scenario_tags_split_merge(seed_tp: ThoughtPoint) -> tuple[ScenarioResult, ThoughtPoint, list[ThoughtPoint]]:
    _emit_requirement("split_merge_provenance")
    seed_tp.add_tag("candidate", tick=3)
    _assert("candidate" in seed_tp.tags, "tag add failed")
    seed_tp.remove_tag("candidate", tick=4)
    _assert("candidate" not in seed_tp.tags, "tag removal failed")

    children = seed_tp.split(tick=5, child_count=2)
    _assert(len(children) == 2, "split should return 2 children")
    for child in children:
        _assert(seed_tp.tp_id in child.provenance.parent_ids, "child missing parent provenance")
        _assert(child.current_basin_id == seed_tp.current_basin_id, "child basin mismatch")
    _assert(len(seed_tp.provenance.split_children) == 2, "parent split_children not recorded")

    merged = ThoughtPoint.merge(children, tick=6, basin_id="OB_summary", deterministic_mode=True)
    _assert(merged.current_basin_id == "OB_summary", "merged basin mismatch")
    _assert(sorted(merged.provenance.merge_sources) == sorted([c.tp_id for c in children]), "merge sources provenance mismatch")
    _assert("merged" in merged.tags, "merged tag missing")

    return (
        ScenarioResult(
            name="tags_split_merge_provenance",
            status="PASS",
            requirement_key="split_merge_provenance",
            detail="Tagging, split, merge, and provenance checks succeeded.",
        ),
        merged,
        children,
    )


def scenario_determinism_and_monotonicity() -> ScenarioResult:
    _emit_requirement("determinism")
    tp_one = ThoughtPoint.new(
        basin_id="OB_identity",
        entropy=EntropyComponents(h_rep=1.0, h_pred=1.0, h_struct=1.0),
        embedding=[0.5, 0.25, 0.125],
        created_at_tick=10,
        deterministic_mode=True,
        deterministic_nonce=99,
    )
    tp_two = ThoughtPoint.new(
        basin_id="OB_identity",
        entropy=EntropyComponents(h_rep=1.0, h_pred=1.0, h_struct=1.0),
        embedding=[0.5, 0.25, 0.125],
        created_at_tick=10,
        deterministic_mode=True,
        deterministic_nonce=99,
    )
    _assert(tp_one.tp_id == tp_two.tp_id, "deterministic IDs diverged for identical inputs")

    counters: list[int] = [tp_one.state_counter]
    tp_one.add_tag("deterministic", tick=11)
    counters.append(tp_one.state_counter)
    tp_one.move_to_basin("RB_relation", tick=12, note="test")
    counters.append(tp_one.state_counter)
    tp_one.update_entropy(tick=13, d_rep=-0.05)
    counters.append(tp_one.state_counter)
    _assert(counters == sorted(counters), "state_counter is not monotonic")
    _assert(len(set(counters)) == len(counters), "state_counter repeated values")

    return ScenarioResult(
        name="determinism_and_monotonicity",
        status="PASS",
        requirement_key="determinism",
        detail="Deterministic IDs and strictly monotonic state_counter validated.",
    )


def _write_artifact(results: list[ScenarioResult], tp: ThoughtPoint, merged: ThoughtPoint, children: list[ThoughtPoint]) -> None:
    payload = {
        "module": MODULE_NAME,
        "result": "PASS" if all(r.status == "PASS" for r in results) else "FAIL",
        "scenarios": [r.as_dict() for r in results],
        "objects": {
            "seed_tp": tp.to_dict(),
            "merged_tp": merged.to_dict(),
            "children": [child.to_dict() for child in children],
        },
    }
    ARTIFACT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _print_summary(results: list[ScenarioResult]) -> None:
    print("\n=== Scenario Summary ===")
    for result in results:
        req = REQ[result.requirement_key]
        print(
            f"- {result.name}: {result.status} | HLR={req['hlr']} | "
            f"LLR={req['llr']} | {result.detail}"
        )
    overall = "PASS" if all(result.status == "PASS" for result in results) else "FAIL"
    print(f"OVERALL RESULT: {overall}")
    print(f"ARTIFACT: {ARTIFACT_PATH}")


def main() -> int:
    print("== TP Lifecycle Verification Harness ==")
    print(f"Module: {MODULE_NAME}")
    print("deterministic_mode=True")
    print("\nRequirement IDs emitted during execution:")

    results: list[ScenarioResult] = []
    seed_tp: ThoughtPoint | None = None
    merged_tp: ThoughtPoint | None = None
    children: list[ThoughtPoint] = []

    try:
        scenario_one_result, seed_tp = scenario_creation_movement_entropy()
        results.append(scenario_one_result)

        scenario_two_result, merged_tp, children = scenario_tags_split_merge(seed_tp)
        results.append(scenario_two_result)

        scenario_three_result = scenario_determinism_and_monotonicity()
        results.append(scenario_three_result)

        _write_artifact(results, seed_tp, merged_tp, children)
        _print_summary(results)
        return 0
    except Exception as exc:
        print("\nHarness failure detected.")
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        if seed_tp is not None and merged_tp is not None:
            _write_artifact(results, seed_tp, merged_tp, children)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
