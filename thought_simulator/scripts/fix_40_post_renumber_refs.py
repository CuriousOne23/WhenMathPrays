#!/usr/bin/env python3
"""Fix known identity-reference corruption after Phase-1 40 renumber."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = frozenset({"archive", "__pycache__", ".git", "node_modules"})
EXTENSIONS = {".md", ".py", ".json", ".yml"}

# Longest-first. Do not replace 40.160_tp (module band is correct).
FIXES: list[tuple[str, str]] = [
    # Corrupted path tokens from substring collisions during bulk replace
    ("40.1100_regulator_prototypes", "40.320_regulator_prototypes"),
    ("40.1600_ob_prototypes", "40.200_ob_prototypes"),
    ("40.1606_ab_sync_prototypes", "40.206_ab_sync_prototypes"),
    ("40.3400_cop_prototypes", "40.340_cop_prototypes"),
    ("40.2600_event_log_prototypes", "40.300_event_log_prototypes"),
    ("40.1200_math_prototypes", "40.330_math_prototypes"),
    ("40.2500_mb_prototypes", "40.350_mb_prototypes"),
    ("40.180_oub_prototypes", "40.140_oub_prototypes"),
    ("40.39_mb_prototypes", "40.350_mb_prototypes"),
    ("40.1606", "40.206"),
    ("40.1600", "40.200"),
    ("40.1100", "40.320"),
    # Process guide shorthand (40.20 band migrated to 40.05 governance)
    ("40.160/30.00", "40.05/30.00"),
    ("40.160 Appendix B", "40.05 Appendix B"),
    ("40.160-aligned", "40.05-aligned"),
    ("40.160 aligned", "40.05 aligned"),
    ("40.160 structural alignment", "40.05 structural alignment"),
    ("40.160 structural", "40.05 structural"),
    ("40.160 pass", "40.05 pass"),
    ("40.160 must not", "40.05 must not"),
    ("40.160 capsule structure", "40.05 capsule structure"),
    ("40.160 evidence standards", "40.05 evidence standards"),
    ("40.160 convention", "40.05 convention"),
    ("per 40.160 +", "per 40.05 +"),
    ("per 40.160)", "per 40.05)"),
    ("per 40.160,", "per 40.05,"),
    ("per 40.160.", "per 40.05."),
    ("per 40.160 ", "per 40.05 "),
    ("(per 40.160)", "(per 40.05)"),
    ("(40.160)", "(40.05)"),
    ("## Phase B delta (40.160)", "## Phase B delta (40.05)"),
    ("Evidence types (40.160)", "Evidence types (40.05)"),
    ("does not replace 40.160", "does not replace 40.05"),
    ("| 40.160, ", "| 40.05, "),
    ("40.160 owner", "40.05 owner"),
    ("40.160 priorities", "40.05 priorities"),
    ("40.160 is responsible", "40.05 is responsible"),
    ("40.160 governance", "40.05 governance"),
    ("40.160 exploratory", "40.05 exploratory"),
    ("40.160 itself", "40.05 itself"),
    ("40.160`-governed", "40.05`-governed"),
    ("`40.160`", "`40.05`"),
    ("[40.160]", "[40.05]"),
    ("40.160 /", "40.05 /"),
    ("40.160,", "40.05,"),
    ("40.160.", "40.05."),
    ("40.160 ", "40.05 "),
    ("40.160\n", "40.05\n"),
    ("(40.160, 30.00", "(40.05, 30.00"),
    ("40.160, 30.00", "40.05, 30.00"),
    ("40.160 / 30.00", "40.05 / 30.00"),
    ("modeled after 40.160).", "modeled after 40.160_tp_lifecycle)."),
    # Historical table in 00.00.42 — restore compression row target
    ("40.50_regulator_prototypes | 40.1100_regulator_prototypes", "40.50_regulator_prototypes | 40.440_regulator_prototypes"),
    # Old RB/TB shorthand bands
    ("40.501/401/106/601/35", "40.190/200/210/230/250"),
    ("40.501/40.200/40.210/40.601/40.250", "40.190/40.200/40.210/40.230/40.250"),
    ("40.200/40.210/40.501", "40.200/40.210/40.190"),
    ("40.501/40.200/40.210/40.601", "40.190/40.200/40.210/40.230"),
    ("40.190, 40.200, 40.210, 40.601, 40.250", "40.190, 40.200, 40.210, 40.230, 40.250"),
    ("Handoffs to 40.190 / 40.240 / 40.210 / 40.601", "Handoffs to 40.190 / 40.240 / 40.210 / 40.230"),
    ("relative to 40.601 (TB)", "relative to 40.230 (TB)"),
    ("Handoffs to 40.601 / 40.170 / 40.150", "Handoffs to 40.230 / 40.170 / 40.150"),
    ("evidence path to 40.601 (TB)", "evidence path to 40.230 (TB)"),
    ("[40.501]", "[40.190]"),
    ("handoff (40.501)", "handoff (40.190)"),
    ("`40.501_*`", "`40.190_*`"),
    ("`40.601_*`", "`40.230_*`"),
    ("`40.501`", "`40.190`"),
    ("40.501,", "40.190,"),
    ("40.501 ", "40.190 "),
    ("40.501/", "40.190/"),
    ("40.501.", "40.190."),
    ('"40.501:', '"40.190:'),
    ('"40.601:', '"40.230:'),
    # Regulator module conflated with 40.50_inb after renumber
    ("This 40.50 capsule is the exploratory verification record (30.50 holds canonical promotion).", "This 40.320 capsule is the exploratory verification record (30.50 holds canonical promotion)."),
    ("40.50 prototype/harness (Phase B)", "40.320 prototype/harness (Phase B)"),
    ("Phase B evidence from 40.50 (", "Phase B evidence from 40.320 ("),
    ("source 40.50/verification_capsule.md (and 40.50/requirements_delta.md + software_description.md)", "source 40.320_regulator_prototypes/verification_capsule.md (and 40.320_regulator_prototypes/requirements_delta.md + software_description.md)"),
    ("CP-reviewed 40.50 software_description", "CP-reviewed 40.320 software_description"),
    ("40.50 software_description (full Phase A per 40.05)", "40.320 software_description (full Phase A per 40.05)"),
    ("Phase B complete in 40.50 (", "Phase B complete in 40.320 ("),
    ("(Full details in the source 40.50/verification_capsule.md", "(Full details in the source 40.320_regulator_prototypes/verification_capsule.md"),
    ("all PASS (see 40.50 for per-scenario", "all PASS (see 40.320 for per-scenario"),
    ("all PASS (see 40.50 capsule for details)", "all PASS (see 40.320 capsule for details)"),
    ("promoted from 40.50 Phase B)", "promoted from 40.320 Phase B)"),
    ("20.150/170/30/40/90 + 20.90_ts_parameter_table (as in 40.50 software_description per CP review)", "20.150/170/30/40/90 + 20.90_ts_parameter_table (as in 40.320 software_description per CP review)"),
    ("Phase B executed in 40.50:", "Phase B executed in 40.320:"),
    ("40.50/ delta and capsule have", "40.320_regulator_prototypes/ delta and capsule have"),
    ("three-flows recorded in source 40.50 docs", "three-flows recorded in source 40.320 docs"),
    ("Phase B execution of 40.50 (", "Phase B execution of 40.320 ("),
    ("Evidence captured in 40.50 capsule/delta/artifact", "Evidence captured in 40.320 capsule/delta/artifact"),
    ("Constructed per 50.05 from 40.39 Phase B", "Constructed per 50.05 from 40.350 Phase B"),
    ("The 40.39_mb_prototypes", "The 40.350_mb_prototypes"),
    ("40.39_mb_prototypes/", "40.350_mb_prototypes/"),
    ("40.39/30.39", "40.350/30.39"),
    ("from 40.39/30.39", "from 40.350/30.39"),
    ("Backward flow from 40.39/30.39", "Backward flow from 40.350/30.39"),
    ("exploratory evidence from 40.39_mb_prototypes", "exploratory evidence from 40.350_mb_prototypes"),
    ("40.340 evidence set", "40.340_cop_prototypes evidence set"),
]


def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if path.name == Path(__file__).name:
            continue
        if any(p in SKIP_DIRS for p in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in FIXES:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT).as_posix())
    print(f"Fixed {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())