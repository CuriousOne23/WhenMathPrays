"""UPI — sole authorized writer of USP rules from clarification_event records."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


_structs = _load_module("structs_prototype", _ROOT / "40.100_core_data_structs_prototypes" / "prototype.py")
_usp_mod = _load_module("usp_prototype", _ROOT / "40.80_usp_prototypes" / "prototype.py")

ClarificationEvent = _structs.ClarificationEvent
UpiCommitRecord = _structs.UpiCommitRecord
USPStore = _usp_mod.USPStore

REASON_INCOMPLETE = "UPI_RSN_001_INCOMPLETE_EVENT"
REASON_PENDING_CAP = "UPI_RSN_002_PENDING_CAP"
REASON_USP_CAP = "UPI_RSN_003_USP_CAP"

DEFAULT_PENDING_CAP = 8
GbEvaluator = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass
class UPI:
    usp: USPStore
    pending_cap: int = DEFAULT_PENDING_CAP
    pending_gb: list[dict[str, Any]] = field(default_factory=list)
    audit_log: list[UpiCommitRecord] = field(default_factory=list)
    _processed_seq: list[int] = field(default_factory=list)

    def process_event(
        self,
        event: ClarificationEvent | dict[str, Any],
        *,
        gb_evaluator: GbEvaluator | None = None,
        gb_decision: str = "approve",
    ) -> UpiCommitRecord:
        if isinstance(event, dict):
            event = ClarificationEvent(
                event_id=event["event_id"],
                integration_seq=event["integration_seq"],
                pattern=event["pattern"],
                expansion=event["expansion"],
                scope=event.get("scope", "conversation"),
                source=event.get("source", "TEST_FIXTURE"),
            )
        try:
            event.validate_complete()
        except Exception:
            record = UpiCommitRecord("REJECTED", None, None, None, [REASON_INCOMPLETE])
            self.audit_log.append(record)
            return record

        if len(self.pending_gb) >= self.pending_cap:
            record = UpiCommitRecord("REJECTED", None, None, None, [REASON_PENDING_CAP])
            self.audit_log.append(record)
            return record

        gb_out: dict[str, Any]
        if gb_evaluator:
            gb_out = gb_evaluator(event.to_dict())
        else:
            gb_out = {"granted": gb_decision == "approve", "gb_reason_code": "GB_TEST_OK" if gb_decision == "approve" else "GB_TEST_VETO"}

        if not gb_out.get("granted", False):
            # gb_reason_code surfaced on record + reason_codes for MB/audit (20.103-010/011)
            veto_code = gb_out.get("gb_reason_code", "GB_VETO")
            record = UpiCommitRecord(
                "GB_VETOED",
                None,
                None,
                veto_code,
                [veto_code],
            )
            self.audit_log.append(record)
            return record

        result = self.usp.apply_commit(
            pattern=event.pattern,
            expansion=event.expansion,
            rule_id=f"rule-{event.event_id}",
            gb_approved=True,
            scope=event.scope,
        )
        if not result.ok:
            reason = result.reason_codes[0] if result.reason_codes else "USP_REJECT"
            record = UpiCommitRecord("REJECTED", None, None, None, [reason])
            self.audit_log.append(record)
            return record

        self._processed_seq.append(event.integration_seq)
        record = UpiCommitRecord(
            "COMMITTED",
            result.usp_version_id,
            result.usp_version_ref,
            gb_out.get("gb_reason_code"),
            ["COMMITTED"],
        )
        self.audit_log.append(record)
        return record

    def process_fifo(self, events: list[ClarificationEvent | dict[str, Any]], **kwargs: Any) -> list[UpiCommitRecord]:
        ordered = sorted(
            events,
            key=lambda e: e.integration_seq if isinstance(e, ClarificationEvent) else e["integration_seq"],
        )
        return [self.process_event(e, **kwargs) for e in ordered]