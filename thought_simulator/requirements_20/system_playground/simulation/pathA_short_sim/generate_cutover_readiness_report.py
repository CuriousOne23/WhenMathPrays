import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from pathA_short_simulator import PRIMITIVES, run_pathA_short


EXAMPLE_SENTENCES: List[str] = [
    "The quick brown fox jumps over the lazy dog.",
    "The rain in Spain stays mainly in the plain.",
    "The sky is blue.",
    "Paris is a city.",
    "The book is on the table.",
    "The rain stays in the plain.",
    "Where is the book?",
    "Is the book on the table?",
    "Why is the sky blue?",
    "Why does the rain in Spain stay mainly in the plain?",
    "Where is the book that is on the table?",
    "Why is the sky that is blue bright?",
]


def _default_mode_counts() -> Dict[str, int]:
    return {
        "committed": 0,
        "mixed": 0,
        "legacy": 0,
        "n/a": 0,
    }


def _pct(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((count / total) * 100.0, 2)


def generate_report() -> Dict[str, object]:
    primitive_names = [fn.__name__ for fn in PRIMITIVES]

    per_primitive_counts: Dict[str, Dict[str, int]] = {
        name: _default_mode_counts() for name in primitive_names
    }
    overall_counts = _default_mode_counts()
    sentence_summaries: List[Dict[str, object]] = []

    for sentence in EXAMPLE_SENTENCES:
        result = run_pathA_short(sentence)
        trace = result["trace"]
        sentence_counts = _default_mode_counts()

        for step in trace:
            primitive = str(step.get("primitive", ""))
            bridge = step.get("bridge_trace", {}) or {}
            mode = str(bridge.get("mode", "n/a"))
            if mode not in sentence_counts:
                mode = "n/a"

            sentence_counts[mode] += 1
            overall_counts[mode] += 1
            if primitive in per_primitive_counts:
                per_primitive_counts[primitive][mode] += 1

        sentence_summaries.append(
            {
                "sentence": sentence,
                "counts": sentence_counts,
                "committed_or_mixed_steps": sentence_counts["committed"] + sentence_counts["mixed"],
                "legacy_steps": sentence_counts["legacy"],
            }
        )

    per_primitive_percentages: Dict[str, Dict[str, float]] = {}
    for primitive, counts in per_primitive_counts.items():
        total = sum(counts.values())
        per_primitive_percentages[primitive] = {
            "committed": _pct(counts["committed"], total),
            "mixed": _pct(counts["mixed"], total),
            "legacy": _pct(counts["legacy"], total),
            "n/a": _pct(counts["n/a"], total),
        }

    overall_total = sum(overall_counts.values())
    overall_percentages = {
        "committed": _pct(overall_counts["committed"], overall_total),
        "mixed": _pct(overall_counts["mixed"], overall_total),
        "legacy": _pct(overall_counts["legacy"], overall_total),
        "n/a": _pct(overall_counts["n/a"], overall_total),
    }

    readiness = {
        "legacy_present": overall_counts["legacy"] > 0,
        "sob_fully_committed": per_primitive_counts.get("SOB", {}).get("mixed", 0) == 0 and per_primitive_counts.get("SOB", {}).get("legacy", 0) == 0,
        "srob_fully_committed": per_primitive_counts.get("SROB", {}).get("mixed", 0) == 0 and per_primitive_counts.get("SROB", {}).get("legacy", 0) == 0,
        "intake_fully_committed": all(
            per_primitive_counts.get(p, {}).get("committed", 0) == len(EXAMPLE_SENTENCES)
            for p in ("InB", "IIInB", "IE")
        ),
    }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sentence_count": len(EXAMPLE_SENTENCES),
        "primitive_count": len(primitive_names),
        "example_sentences": EXAMPLE_SENTENCES,
        "overall": {
            "counts": overall_counts,
            "percentages": overall_percentages,
            "total_primitive_executions": overall_total,
        },
        "per_primitive": {
            "counts": per_primitive_counts,
            "percentages": per_primitive_percentages,
        },
        "per_sentence": sentence_summaries,
        "readiness": readiness,
    }


def to_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Cutover Readiness Report")
    lines.append("")
    lines.append(f"Generated: {report['generated_at_utc']}")
    lines.append(f"Sentences analyzed: {report['sentence_count']}")
    lines.append(f"Primitives per run: {report['primitive_count']}")
    lines.append("")

    overall = report["overall"]
    overall_counts = overall["counts"]
    overall_pct = overall["percentages"]
    lines.append("## Overall Bridge Mode Usage")
    lines.append("")
    lines.append("| Mode | Count | Percent |")
    lines.append("|---|---:|---:|")
    for mode in ("committed", "mixed", "legacy", "n/a"):
        lines.append(f"| {mode} | {overall_counts[mode]} | {overall_pct[mode]}% |")
    lines.append("")

    lines.append("## Per Primitive Usage")
    lines.append("")
    lines.append("| Primitive | committed | mixed | legacy | n/a |")
    lines.append("|---|---:|---:|---:|---:|")
    p_counts = report["per_primitive"]["counts"]
    for primitive in p_counts:
        c = p_counts[primitive]
        lines.append(f"| {primitive} | {c['committed']} | {c['mixed']} | {c['legacy']} | {c['n/a']} |")
    lines.append("")

    lines.append("## Readiness Flags")
    lines.append("")
    readiness = report["readiness"]
    for k in ("legacy_present", "sob_fully_committed", "srob_fully_committed", "intake_fully_committed"):
        lines.append(f"- {k}: {readiness[k]}")
    lines.append("")

    lines.append("## Sentence Set")
    lines.append("")
    for idx, sentence in enumerate(report["example_sentences"], start=1):
        lines.append(f"{idx}. {sentence}")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    report = generate_report()
    base_dir = Path(__file__).resolve().parent
    report_json_path = base_dir / "cutover_readiness_report.json"
    report_md_path = base_dir / "notes" / "cutover_readiness_report.md"

    report_json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report_md_path.write_text(to_markdown(report), encoding="utf-8")

    print(f"Wrote JSON report: {report_json_path}")
    print(f"Wrote Markdown report: {report_md_path}")
    print("Overall counts:", report["overall"]["counts"])


if __name__ == "__main__":
    main()
